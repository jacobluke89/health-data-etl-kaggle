import random
from pprint import pprint
from typing import List, Union, Tuple

from IPython.core.display_functions import display
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, count
from faker import Faker

from constants.condition_probabilities import condition_age_probability_dict


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


def display_df(spark_df: DataFrame, num_rows: int = 20, select_rows: List = None):
    if select_rows:
        spark_df = spark_df.select(select_rows)
    pandas_df = spark_df.toPandas()
    display(pandas_df.head(num_rows))


def get_column_names(df: DataFrame):
    column_names = df.columns
    print(column_names)


def remove_data(df_driver: DataFrame, df_anti: DataFrame, condition_1: Union[bool, col], condition_2: Union[bool, col]):
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


"""
udf function 

takes age column sub_level_admission and list of conditions 

choose a condition from the list of conditions 

check if given age they can have that condition 

While True:
    if they can then given their age they should increase 
    / decrease the probability of that condition
    
    else they should be reassigned another sub_level_admission 
    
    once valid sub_level_admission exit while loop 
    
return the condition column


"""


# def choose_condition(age, sub_level_admission, conditions_list):
#     while True:
#         chosen_condition = random.choice(conditions_list)
#         age_prob_list = condition_age_probability_dict[sub_level_admission][chosen_condition]
#
#         for (age_min, age_max), prob in age_prob_list:
#             if age_min <= age <= age_max:
#                 if random.random() < prob:
#                     return chosen_condition
#                 break  # Exit the for-loop if age is within a boundary but condition is not chosen
#


    # example age range weights
age_ranges_weights = [
    ((0, 10), 0.1),
    ((11, 17), 0.3),
    ((18, 25), 0.5),
    ((25, 34), 1),
    ((35, 44), 2),
    ((45, 59), 2.7),
    ((45, 54), 2.8),
    ((55, 64), 3.15),
    ((65, 75), 3.4),
    ((76, 80), 3.7)
]


def calculate_weighted_probabilities(target_average: float = 0.125,
                                     age_ranges: List[Tuple[Tuple[int, int], int]] = None) -> List[Tuple[Tuple[int, int], int]]:
    if age_ranges is None:
        age_ranges = age_ranges_weights
    total_weight = sum(age_range[1] for age_range in age_ranges)

    total_probability = target_average * len(age_ranges)

    weighted_probabilities = []

    for age_range, weight in age_ranges:
        # Calculate each age range's share of the total probability
        probability = round((weight / total_weight) * total_probability, 5)
        weighted_probabilities.append((age_range, probability))

    return weighted_probabilities


if __name__ == '__main__':
    pprint(calculate_weighted_probabilities(0.45))
