import re
from datetime import timedelta, datetime
from random import choices, randint
from faker import Faker

fake = Faker()

def generate_name(salutation=None) -> str:
    """
    Generate a name with optional salutation and specific count of initials.

    Args:
        salutation (str, optional): Prefix for the name, e.g., 'Dr.'.

    Returns:
        str: A generated name with or without initials and salutation.
    """

    initials_count = choices([1, 2, 3], weights=[1, 0.4, 0.1], k=1)[0]
    initials = ' '.join(fake.random_uppercase_letter() + '.' for _ in range(initials_count))
    surname = fake.last_name()
    if salutation:
        return f"{salutation} {fake.first_name()} {surname}"
    return f"{initials} {surname}"


population_weights = {
    "uk": {"male": 48, "female": 52},
    # Add more countries as needed
}


def random_gender_chooser(country: str) -> str:
    """
    This function will generate a random gender for a row
    It will weight it accordance with the country passed in.
    Data for this can be found at population.un.org
    Args:
        country (str): the chosen country e.g. uk, used to obtain population weights from
        the population_weights dictionary
    Returns:
        str: given gender, Male or Female
    """

    if country in population_weights:
        weights = population_weights[country]
        return choices(["Male", "Female"], weights=[weights["male"], weights["female"]], k=1)[0]
    else:
        print(f"Country, {country} not in the weights dictionary, default 50 / 50 split.")
        return choices(["Male", "Female"], weights=[50, 50], k=1)[0]


blood_type_distribution = {
    "O+": 35,
    "O-": 13,
    "A+": 30,
    "A-": 8,
    "B+": 8,
    "B-": 2,
    "AB+": 2,
    "AB-": 1
}

def choose_blood_type():
    """
    This function randomly chooses a blood type based on the blood type
    distribution, this information was found at
    https://www.blood.co.uk/why-give-blood/blood-types/
    therefore is uk specific, further, it does not consider ethnicity.

    Returns:
       str: a blood type
    """
    types = list(blood_type_distribution.keys())
    weights = list(blood_type_distribution.values())
    return choices(types, weights=weights, k=1)[0]

def dob_creator(age: int) -> str:
    """
    This function creates a random DOB given someone's age.
    Args:
        age (int): age of a given individual.
    Returns:
        str: DOB.
    """
    birth_date = datetime.now().date() - timedelta(days=age * 365 + randint(0, 364))
    return birth_date.strftime('%Y-%m-%d')

def check_gender_is_female(gender: str) -> bool:
    """
    Check if the gender string corresponds to 'female'.

    Args:
        gender (str): Gender string to check

    Returns:
        bool: True if gender is 'female', False otherwise
    """
    return gender.lower() == 'female'


def check_patient_is_pediatric(age: int) -> bool:
    """
    Check if the age string corresponds to a patient being a pediatric patient.

    Args:
        age (int): The age of the patient

    Returns:
        bool: True if gender is a 'pediatric' patient, False otherwise
    """
    return age < 18


def check_patient_is_geriatric(age: int) -> bool:
    """
    Check if the age string corresponds to a patient being a geriatric patient.

    Args:
        age (int): The age of the patient

    Returns:
        bool: True if gender is a 'geriatric' patient, False otherwise
    """
    return age >= 65


def clean_name(name: str) -> str:
    """
    This function takes in a Name e.g. J. L. Smith and returns J_L_SMITH
    Args:
        name (str):
    Returns:
        str: the concatenated name with underscores
    """
    return re.sub(r"\s+", "_", re.sub(r"\.", "", name))

def create_unique_id(name: str, dob: str) -> str:
    """
    Creates a unique ID by concatenating the cleaned name with the date of birth.
    Args:
        name (str): The name data from the RDD
        dob (str): The dob data from the RDD

    Returns:
        str: a unique id e.g. J_L_Smith_1988-12-12
    """
    return f"{clean_name(name)}|{dob}"
