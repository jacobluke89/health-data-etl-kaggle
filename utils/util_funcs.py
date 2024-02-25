from typing import List, Union

from IPython.core.display_functions import display
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, count
from faker import Faker

def get_row_count(df: DataFrame, verbose=False):
    """
    Returns the number of rows in a DataFrame.

    Parameters:
    df (DataFrame): A PySpark DataFrame.
    verbose (bool): to print the number of rows.
    """
    if verbose:
        print(df.count())
    return df.count()

def display_df(spark_df: DataFrame,  num_rows: int = 20, select_rows: List = None):
    if select_rows:
        spark_df = spark_df.select(select_rows)
    pandas_df = spark_df.toPandas()
    display(pandas_df.head(num_rows))

def get_column_names(df: DataFrame):
    column_names = df.columns
    print(column_names)

def remove_data(df_driver: DataFrame, df_anti: DataFrame, condition_1: Union[bool, col], condition_2: Union[bool,col]):
    result_df = df_driver.join(df_anti,
                               on=['sub_level_admission', 'DOB'],
                               how='left_anti')

    assert result_df.where(condition_1 & condition_2).count() == 0
    return result_df


def verify_ranking(_df: DataFrame, ranked_df: DataFrame):
    joined_df = _df.alias("df").join(
        ranked_df.alias("ranked"),

        (col("df.unique_id") == col("ranked.unique_id")),
        "inner"
    )

    verification_df = joined_df.select(
        col("df.unique_id")
    ).distinct().groupBy("unique_id").agg(
        count("unique_id").alias("unique_id_count")
    )

    # Check if any name has a mismatch in the count of unique IDs
    mismatch_count = verification_df.filter("unique_id_count > 1").count()

    # Assert that there are no mismatches
    assert mismatch_count == 0, f"There are names with mismatched unique ID counts. mismatch_count: {mismatch_count}"

def verify_ranking_counts(_df: DataFrame, ranked_df: DataFrame, names: list, unique_ids: list):
    for name, unique_id in zip(names, unique_ids):
        # Define filter conditions
        name_condition = col("name") == name
        unique_id_condition = col("unique_id") == unique_id
        stay_name_condition = col("stay_name").like(f"{name}_%")

        df_filtered_count = (_df
                             .filter(name_condition & unique_id_condition & stay_name_condition)
                             .count())

        ranked_df_filtered_count = (ranked_df
                                    .filter(name_condition & unique_id_condition & stay_name_condition)
                                    .count())

        # Assert that the counts are equal for each name-unique_id pair
        assert df_filtered_count == ranked_df_filtered_count, f"The number of matching rows for {name} with unique ID {unique_id} should be the same in both DataFrames."


def create_doctor_names():
    fake = Faker()
    return [f"Dr. {fake.first_name()} {fake.last_name()}" for _ in range(50)]

