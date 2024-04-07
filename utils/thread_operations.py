from utils.conditions_creator import ConditionsCreator

from concurrent.futures import ThreadPoolExecutor, as_completed
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import spark_partition_id
from typing import Type
from functools import reduce

class TaskWrapper:
    def __init__(self, spark, task_class, *args, **kwargs):
        self.task = task_class(spark, *args, **kwargs)

    def runner(self):
        return self.task.runner()


def process_partition(spark: SparkSession,
                      partition_id: int,
                      class_to_run: Type,
                      df: DataFrame,
                      *args,
                      **kwargs) -> DataFrame:
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
    else:
        return spark.createDataFrame([], args[0].schema)

def thread_runner(spark: SparkSession,
                  class_to_run: Type,
                  *args,
                  **kwargs) -> DataFrame:
    df = args[0]  # Assuming the first positional argument is always the DataFrame
    total_rows = df.count()
    rows_per_partition = 100
    num_partitions = total_rows // rows_per_partition + (1 if total_rows % rows_per_partition else 0)
    df = df.repartition(num_partitions)
    return run_multithreaded_processing(spark, class_to_run, num_partitions, df, *args, **kwargs)
