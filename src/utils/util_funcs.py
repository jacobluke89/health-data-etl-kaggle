from random import choices
from typing import List, Tuple, Dict

from pyspark.sql import DataFrame
from faker import Faker
from pyspark.sql.functions import sum

from src.constants.type_constants import DepartmentTypes


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


def create_doctor_names() -> List:
    """
    Generate a list of doctor names.

    Returns:
        list: A list of names prefixed with 'Dr.'.
    """

    return [generate_name(salutation="Dr.") for _ in range(50)]


def generate_name( salutation=None, initials_count=3) -> str:
    """
    Generate a name with optional salutation and specific count of initials.

    Args:
        salutation (str, optional): Prefix for the name, e.g., 'Dr.'.
        initials_count (int, optional): Specifies the number of initials to generate.

    Returns:
        str: A generated name with or without initials and salutation.
    """
    fake = Faker()
    if initials_count is None:
        initials_count = choices([1, 2, 3], weights=[1, 0.5, 0.2], k=1)[0]
    initials = ' '.join([f"{fake.random_uppercase_letter()}." for _ in range(initials_count)])
    surname = fake.last_name()
    if salutation:
        return f"{salutation} {fake.first_name()} {surname}"
    else:
        return f"{initials} {surname}"


def create_doctor_names_for_all_specialties() -> Dict:
    doctor_names_by_specialty = {}
    for subtype in DepartmentTypes:
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
