from pprint import pprint
from random import choices
from typing import List, Union, Tuple

from IPython.core.display_functions import display
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, count
from faker import Faker

from constants.type_constants import SubAdmissionTypes


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
    return [create_fake_name("Dr.") for _ in range(50)]

def create_fake_name(salutation=None):
    fake = Faker()
    initials = ' '.join([f"{fake.random_uppercase_letter()}." for _ in
                         range(choices([1, 2, 3], weights=[1, 0.5, 0.2], k=1)[0])])
    if salutation is not None:
        return f"{salutation}{fake.first_name()} {fake.last_name()}"
    else:
        return f"{initials} {fake.last_name()}"


def create_doctor_names_for_all_specialties():
    doctor_names_by_specialty = {}
    for subtype in SubAdmissionTypes:
        doctor_names_by_specialty[subtype.name] = create_doctor_names()
    return doctor_names_by_specialty


age_ranges_weights = [
    ((0, 10), .000),
    ((11, 17), .00),
    ((18, 25), .3),
    ((25, 34), .5),
    ((35, 44), .9),
    ((45, 59), 1.9),
    ((45, 54), 3.9),
    ((55, 64), 5.8),
    ((65, 75), 6.1),
    ((76, 80), 7.1)
]


def calculate_weighted_probabilities(target_average: float,
                                     age_ranges: List[Tuple[Tuple[int, int], int]] = None) -> list[Tuple[tuple[int, int], float]]:
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


def reverse_engineer_weights(given_probabilities: List[Tuple[Tuple[int, int], float]],
                             target_average: float) -> List[Tuple[Tuple[int, int], float]]:
    """
    Calculates the weights for each age range based on given probabilities and a target average.

    Args:
        given_probabilities: A list of tuples, each containing an age range and its associated probability.
        target_average: The target average probability across all age ranges.

    Returns:
        A list of tuples, each containing an age range and its calculated weight.
    """
    # Calculate the total probability based on the target average and the number of given probabilities
    total_probability = target_average * len(given_probabilities)

    # Assume initial total weight as the sum of given probabilities (as a starting point)
    initial_total_weight = sum(prob for _, prob in given_probabilities)

    # Calculate initial weights based on the given probabilities
    original_weights = []
    for age_range, given_probability in given_probabilities:
        if total_probability > 0:
            weight = (given_probability / total_probability) * initial_total_weight
        else:
            weight = 0
        original_weights.append((age_range, weight))

    # Adjust the weights proportionally
    adjustment_factor = sum(weight for _, weight in original_weights) / initial_total_weight
    adjusted_weights = [(age_range, round(weight / adjustment_factor, 5)) for age_range, weight in original_weights]

    return adjusted_weights


# Example usage with the new set of probabilities and an overall average
new_probabilities = [((0, 10), 0.0),
                     ((11, 17), 0.00023),
                     ((18, 25), 0.00026),
                     ((25, 34), 0.00291),
                     ((35, 44), 0.00581),
                     ((45, 59), 0.00872),
                     ((45, 54), 0.01163),
                     ((55, 64), 0.02616),
                     ((65, 75), 0.02906),
                     ((76, 80), 0.05522)]
overall_avg_example = 0.014

# if __name__ == '__main__':
#     probs = reverse_engineer_weights(new_probabilities, overall_avg_example)
#     pprint(probs)
