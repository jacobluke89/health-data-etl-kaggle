import json
from pprint import pprint
from typing import List, Union, Tuple

import numpy as np
from IPython.core.display_functions import display
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, count, when, collect_list, struct
from faker import Faker

from constants.type_constants import SubAdmissionTypes


def find_probability_for_age_gender(age: int,
                                    condition_probabilities: Tuple[Tuple[int, int], float]) -> float | int:
    """
    This function returns probability based on age and a given condition probability list.
    Args:
        age: The age we will be comparing to
        condition_probabilities: The list of conditional probabilities

    Returns:
        int: the probability, if 0 returns, edge case, should be investigated.

    """
    (age_min, age_max), prob = condition_probabilities
    if age_min <= age <= age_max:
        return prob
    return 0


def filter_female_conditions(df):
    """
    Filters out entries from a DataFrame based on gender and age criteria:
    - Excludes female-only conditions (MATERNITY, OBSTETRICS) for non-female subjects.
    - Applies age restrictions specifically for MATERNITY-related entries.
    - Filter pediatric patients who cannot be pregnant (based on legal age in the UK, 16)
      No assumption made an individual cannot choose to get pregnant before this age.
      upper age bound defined  here: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4822427/#:~:text=Menopause%20typically%20occurs%20between%2045,reproducing%20many%20years%20before%20menopause.
      between 45 and 55 upper bounding will be 50.
      # TODO Possibility to include outliers in a new func in the future.
    Args:
        df (DataFrame): The input DataFrame with condition and demographic data.

    Returns:
        DataFrame: The filtered DataFrame.
    """

    female_only = [SubAdmissionTypes.MATERNITY.name,
                   SubAdmissionTypes.OBSTETRICS.name]  # TODO Obstetrics needs sorting still.

    filtered_df = df.filter((~(col("top_level_admission").isin(female_only))) & (~col("is_female")))

    filtered_df = filtered_df.withColumn("Age_Filter",
                                         when((col("top_level_admission") == SubAdmissionTypes.MATERNITY.name) &
                                              ((col("Age") < 16) | (col("Age") > 50)),
                                              False).otherwise(True))

    # Filter rows based on the Age_Filter col
    filtered_df = filtered_df.filter(col("Age_Filter")).drop("Age_Filter")

    return filtered_df.filter(
        (~col("is_female") & (col("condition_gender") != "female")) |
        (col("condition_gender").isNull()) | col("is_female")
    )


def filter_geriatric_conditions(df: DataFrame) -> DataFrame:
    """
    This function filters all GERIATRIC submission types
    Args:
        df (DataFrame): The unfiltered dataframe

    Returns:
        df (DataFrame): The filtered dataframe
    """
    return df.filter(~(col("sub_level_admission") == SubAdmissionTypes.GERIATRICS.name) & ~col("is_geriatric"))


def choose_condition_for_patient(probability_df: DataFrame,
                                 driver_df: DataFrame
                                 ) -> str | None:
    """

    Args:

    Returns:
        A condition that will be assigned to the patient or None if issues found.
    """

    df_joined = driver_df.crossJoin(probability_df)

    df = df_joined.filter((col("age") >= col("age_min")) & (col("age") <= col("age_max")))

    df = filter_female_conditions(df)
    df = filter_geriatric_conditions(df)

    df = df.orderBy(col("unique_id"))
    print(df.count())
    conditions_probabilities = []
    df_transformed = df.withColumn("probability_entry",
                                   struct(col("age_min"), col("age_max"), col("probability")))
    df_transformed = df_transformed.withColumn("row_info",
                                               struct(col("Age"), col("condition"), col("is_pediatric"),
                                                      col("unique_id"), col("top_level_admission")))
    df_aggregated = df_transformed.groupBy("unique_id").agg(
        collect_list("probability_entry").alias("probability_entries"),
        collect_list("row_info").alias("row_infos")
    )
    for row in df_aggregated.toLocalIterator():
        unique_id = row["unique_id"]
        probability_entries = [((entry.age_min, entry.age_max), entry.probability) for entry in
                               row["probability_entries"]]
        row_infos = [(entry.Age, entry.condition, entry.is_pediatric, entry.unique_id, entry.top_level_admission) for
                     entry in row["row_infos"]]
        assert len(probability_entries) == len(row_infos), f"Mismatch in lengths for {unique_id}"

        for entry in probability_entries:
            assert isinstance(entry, tuple) and len(
                entry) == 2, f"Invalid entry structure in probability_entries for {unique_id}"
            assert isinstance(entry[0], tuple) and len(
                entry[0]) == 2, f"Invalid age range structure in probability_entries for {unique_id}"
            assert isinstance(entry[1], float), f"Probability is not a float for {unique_id}"

        for info in row_infos:
            assert isinstance(info, tuple) and len(info) == 5, f"Invalid entry structure in row_infos for {unique_id}"

        for probability_info, patient_info in list(zip(probability_entries, row_infos)):
            age_prob = probability_info
            age, condition, is_pediatric, unique_id, top_level_admission = patient_info

            prob = find_probability_for_age_gender(age, age_prob)
            if prob > 0:
                condition_label = f"pediatric_{condition}" if is_pediatric else condition
            else:
                condition_label = "pediatric no condition for patient edge case" if is_pediatric else "no condition for patient edge case"
                prob = 0
            conditions_probabilities.append((f"{unique_id}_{top_level_admission}", condition_label, prob))
    print("before write")
    with open('output_list.txt', 'w') as f:
        f.write(json.dumps(conditions_probabilities))
    # print(conditions_probabilities)
    raise Exception()
    # If no condition is applicable based on age, return None or handle as appropriate
    if not conditions_probabilities:
        return None

    # Sort the conditions by probability for easier handling (optional)
    conditions_probabilities.sort(key=lambda x: x[1], reverse=True)

    # Use cumulative probabilities to select a condition
    total_prob = sum(prob for _, prob in conditions_probabilities)
    random_prob = np.random.uniform(0, total_prob)
    cumulative_prob = 0
    for condition, prob in conditions_probabilities:
        cumulative_prob += prob
        if random_prob < cumulative_prob:
            return condition

    return None


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
                                     age_ranges: List[Tuple[Tuple[int, int], int]] = None) -> list[
    Tuple[tuple[int, int], float]]:
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

if __name__ == '__main__':
    probs = reverse_engineer_weights(new_probabilities, overall_avg_example)
    pprint(probs)
