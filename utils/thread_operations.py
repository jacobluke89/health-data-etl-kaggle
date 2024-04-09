from functools import reduce
from typing import Type, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import spark_partition_id


class TaskWrapper:
    def __init__(self, spark, task_class, *args, **kwargs):
        """

        Args:
            spark (SparkSession): The SparkSession
            task_class: The class that's going to be run.
            *args: The args associated with class.
            **kwargs: The kwargs associated with class, if any.
        """
        self.task = task_class(spark, *args, **kwargs)

    def runner(self) -> Any:
        """
        Calls the task runner function
        Returns:
            Any: returns Any type, right now DataFrame
        """
        return self.task.runner()


def process_partition(spark: SparkSession,
                      partition_id: int,
                      class_to_run: Type,
                      df: DataFrame,
                      *args,
                      **kwargs) -> DataFrame:
    """
    This processes the partition result of the spark_partition process result from the TaskWrapper.runner()
    Args:
        spark (SparkSession): The SparkSession
        partition_id (int): The partition id to filter against the df
        class_to_run (Type): The class to run
        df (DataFrame): The partitioned df 
        *args: The args associated with class.
        **kwargs: The kwargs associated with class, if any.
    Returns:
        Dataframe: The Dataframe result. 
    """
    # Filter the DataFrame for this partition's data
    partition_df = df.filter(spark_partition_id() == partition_id)

    # Update class instantiation with *args and **kwargs
    task = TaskWrapper(spark, class_to_run, partition_df, *args[1:], **kwargs)

    result_df = task.runner()
    return result_df


def run_multithreaded_processing(spark: SparkSession,
                                 class_to_run: Type,
                                 num_partitions: int,
                                 df: DataFrame,
                                 *args,
                                 **kwargs) -> DataFrame:
    """
    Runs the Threaded Processing Process
    Args:
        spark (SparkSession): The SparkSession
        class_to_run (Type): The class to run
        num_partitions (int): total number of partitions to iterate over 
        df (DataFrame): The partitioned df 
        *args: The args associated with class.
        **kwargs: The kwargs associated with class, if any.
    Returns:
       DataFrame: The unionised DataFrame
    """
    partitioned_dfs = []

    with ThreadPoolExecutor(max_workers=num_partitions) as executor:
        futures = [
            executor.submit(process_partition, spark, i, class_to_run, df, *args, **kwargs)
            for i in range(num_partitions)
        ]

        for future in as_completed(futures):
            result_df = future.result()
            partitioned_dfs.append(result_df)

    if partitioned_dfs:
        final_df = reduce(DataFrame.unionByName, partitioned_dfs)
        return final_df
    return spark.createDataFrame([], args[0].schema)


def runner(spark: SparkSession,
           class_to_run: Type,
           *args,
           **kwargs) -> DataFrame:
    """
    Args:
        spark (SparkSession): The SparkSession
        class_to_run (Type): The class to run
        *args: The args associated with class.
        **kwargs: The kwargs associated with class, if any.
    Returns:
        DataFrame: The returned DataFrame from the class to run.
    """
    df = args[0]  # Assuming the first positional argument is always the DataFrame
    total_rows = df.count()
    rows_per_partition = 100
    num_partitions = total_rows // rows_per_partition + (1 if total_rows % rows_per_partition else 0)
    df = df.repartition(num_partitions)
    return run_multithreaded_processing(spark, class_to_run, num_partitions, df, *args, **kwargs)
