import math

from pyspark import RDD
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, lit, rand, sum
from pyspark.sql import Row

from data_generator.csv_data_processor import CSVDataProcessor


def create_distributed_age_df(spark: SparkSession, file_path: str, dataset_size: int = 10000) -> DataFrame:
    """
    This function creates a distributed age using a csv file which should contain an age distribution
    from 0 to 100+, where 100+ is represented by 100 in the csv file.  This then is used to create
    an age distribution from that given file. The data is obtained from population.un.org
    Args:
        spark (SparkSession): The SparkSession
        file_path (str): path where the csv is stored, the column required is "Population Total" renamed from "Value"
        dataset_size (int): the size of the dataset at the end of the process.
    Returns:
        DataFrame: A dataframe of age distributions.
    """
    csv_age_file_file = CSVDataProcessor(spark, file_path)

    csv_age_sq_df = csv_age_file_file.runner()

    new_csv_age_sq_df = normalise_population_density(csv_age_sq_df)

    sampled_rdd = oversample_ages(new_csv_age_sq_df, dataset_size)

    row_rdd = sampled_rdd.map(lambda age: Row(Age=age))
    sampled_df = spark.createDataFrame(row_rdd)

    return sampled_df.orderBy(rand()).limit(dataset_size)


def normalise_population_density(csv_age_sq_df: DataFrame) -> DataFrame:
    """
    normalises the population density of a DataFrame.

    This function calculates the sum of  total population from the 'population_total' column and creates a
    new column 'density' by dividing each population value by sum of the total population. It then normalises
    these density values so that their sum equals 1, creating a 'normalised_density' column.

    Args:
        csv_age_sq_df (DataFrame): A Spark DataFrame with at least a 'population_total' column.
    Returns:
        DataFrame: The input DataFrame augmented with a 'normalised_density' column.
    """
    # Calculate the total population and add density column
    total_population = csv_age_sq_df.select(sum("population_total")).collect()[0][0]
    csv_age_sq_df = csv_age_sq_df.withColumn("density", col("population_total") / lit(total_population))

    # normalise the density to ensure it sums to 1
    total_density = csv_age_sq_df.select(sum("density")).collect()[0][0]
    return csv_age_sq_df.withColumn("normalised_density", col("density") / lit(total_density))


def oversample_ages(dataframe: DataFrame, dataset_size: int, oversample_factor: float = 1.1) -> RDD:
    """
    Over samples the 'age' field in the DataFrame based on the normalised density. This done so, we can guarantee
    the returned rows in the  dataset, due to system rounding errors, there's possibility that if you do not
    over sample you are like to reduce your dataset size.

    This function converts a DataFrame to a Resilient Distributed Dataset (RDD) and applies a transformation that
    replicates each 'age' entry a number of times determined by the product of the
    'normalised_density' and an oversampling number. The oversampling number is calculated
    as the product of the dataset size and an oversampling factor.

    Args:
        dataframe (DataFrame): The Spark DataFrame containing the 'age' and 'normalised_density' columns.
        dataset_size (int): The total size of the dataset used to calculate the oversample number.
        oversample_factor (float): The factor used to scale the dataset size to get the oversample number (default 1.1).

    Returns:
        RDD: An RDD where each 'age' is replicated according to its 'normalised_density' times the oversample number.
    """
    oversample_num = int(dataset_size * oversample_factor)
    return dataframe.rdd.flatMap(
        lambda row: [row['age']] * int(row['normalised_density'] * oversample_num)
    )


def calculate_weighted_sd(df: DataFrame, avg_age: float = 40.2) -> float:
    """
    This function calculates the weighted standard deviation of the given dataset and average
    Args:
        df (DataFrame): containing the age and total population for that given cohort.
        avg_age (float): The average age of the dataset, default is 40.2, for the uk.
    Returns:
        float: The weighted standard deviation
    """
    csv_age_sq_df = df.withColumn("weighted_squared_diff",
                                     lit((col("age") - avg_age) ** 2 * col("population_total")))

    # Sum up the weighted squared differences and the total population
    total_weighted_squared_diff = csv_age_sq_df.select(sum("weighted_squared_diff")).collect()[0][0]
    total_population = csv_age_sq_df.select(sum("population_total")).collect()[0][0]

    # Calculate the weighted variance
    weighted_variance = total_weighted_squared_diff / total_population

    # Calculate the weighted standard deviation
    return math.sqrt(weighted_variance)
