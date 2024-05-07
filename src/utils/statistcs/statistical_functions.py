import math
from typing import Dict

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, lit, sum

from src.data_generator.csv_data_processor import CSVDataProcessor
from src.utils.column_creator_functions import create_rows_rdd


def create_distributed_age_df(spark: SparkSession, file_path: str, ethnicity_dict: Dict, dataset_size: int = 10000) -> DataFrame:
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

    data_processor_age = CSVDataProcessor(spark, file_path)

    csv_age_sq_df = data_processor_age.runner()

    normalised_df = normalise_population_density(csv_age_sq_df)
    sampled_rdd = oversample_ages(normalised_df, dataset_size)

    row_rdd = create_rows_rdd(sampled_rdd, ethnicity_dict)

    sampled_df = spark.createDataFrame(row_rdd)

    return sampled_df.limit(dataset_size)


def normalise_population_density(csv_age_sq_df: DataFrame) -> DataFrame:
    """
    Calculates and normalises the population density to use as sampling weights.
    Args:
        csv_age_sq_df (DataFrame): the csv data frame contain the individual ages and populations for those ages.
    Returns:
        DataFrame: A DataFrame that includes the original columns of csv_age_sq_df, with the addition of:
                   - 'density': The raw density value of each age group as a fraction of the total population.
                   - 'normalized_density': The density normalised so that the sum of all densities equals 1.
                   - 'weight': A column identical to 'normalised_density', provided for clarity and ease of use in sampling functions where a weight parameter might be expected.

    Example:
        Suppose csv_age_sq_df contains the following rows:
            +-----+----------------+
            | age | population_total |
            +-----+----------------+
            |  10 |      100       |
            |  20 |      300       |
            +-----+----------------+

        The returned DataFrame after normalisation would look like this:
            +-----+----------------+--------+-------------------+--------+
            | age | population_total | density | normalised_density | weight |
            +-----+----------------+--------+-------------------+--------+
            |  10 |      100       |  0.25  |       0.333       |  0.333  |
            |  20 |      300       |  0.75  |       0.667       |  0.667  |
            +-----+----------------+--------+-------------------+--------+
        Here, the total population is 400, making the raw densities 0.25 and 0.75. These are normalised to sum to 1.
    """
    total_population = csv_age_sq_df.select(sum("population_total")).collect()[0][0]
    density_df = csv_age_sq_df.withColumn("density", col("population_total") / lit(total_population))

    # Normalising the density to make sure it sums to 1 (suitable for probability usage)
    total_density = density_df.select(sum("density")).collect()[0][0]
    normalized_density_df = density_df.withColumn("normalised_density", col("density") / lit(total_density))

    return normalized_density_df.withColumn("weight", col("normalised_density"))


def oversample_ages(normalised_df: DataFrame, dataset_size: int, oversample_factor: float = 1.1) -> DataFrame:
    """
    Performs weighted sampling on a DataFrame based on normalized density to generate the desired dataset size.
    Args:
        normalised_df (DataFrame): The normalised DataFrame.
        dataset_size (int): The size of the dataset.
        oversample_factor (float): The multiplication factor of the over sample.
    """
    oversample_num = int(dataset_size * oversample_factor)

    # Simply sample with replacement based on the fraction needed
    fraction = oversample_num / normalised_df.count()

    sampled_dataframe = normalised_df.sample(
        withReplacement=True,
        fraction=fraction,
        seed=42  # For reproducibility
    )

    return sampled_dataframe.limit(oversample_num)

def calculate_weighted_sd(df: DataFrame, avg_age: float = 40.2) -> float:
    """
    This function calculates the weighted standard deviation of the given dataset and average
    Args:
        df (DataFrame): containing the age and total population for that given cohort.
        avg_age (float): The average age of the dataset, default is 40.2, for the United Kingdom (UK).
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
