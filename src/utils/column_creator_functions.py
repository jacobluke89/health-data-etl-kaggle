import re
import uuid
from datetime import timedelta, datetime
from functools import partial
from random import choices, randint
from typing import Tuple, Dict

from faker import Faker
import pinyin
from faker.providers import BaseProvider
from pyspark import Row, RDD
from pyspark.sql import DataFrame
from transliterate import translit, get_available_language_codes
import random


def choose_ethnicity(ethnicity_dict: Dict) -> str:
    """
    This function randomly chooses an ethnicity based originate csv
    Returns:
       str: an ethnicity
    """
    types = list(ethnicity_dict.keys())
    weights = list(ethnicity_dict.values())
    return choices(types, weights=weights, k=1)[0]


def create_rows_rdd(sample_df: DataFrame, ethnicity_dict: Dict) -> RDD:
    """
    Converts a DataFrame to an RDD and applies a transformation to each row to enrich the data.

    This function takes a DataFrame, converts it to an RDD, and then applies a mapping operation using
    the `create_individual_row` function to each row. The purpose is to process and transform each row of the DataFrame
    according to the logic defined in `create_individual_row` function.

    Args:
        sample_df (DataFrame): A Spark DataFrame containing rows of data that need to be transformed.
        Requires the 'age' col.

    Returns:
        RDD: Returns an RDD where each row has been transformed using the `create_individual_row` function,
        typically including enriched demographic and healthcare data.
    """
    sample_rdd = sample_df.rdd
    create_row_func = partial(create_individual_row, ethnicity_dict=ethnicity_dict)
    # Use a single map transformation to process each row
    return sample_rdd.map(create_row_func)


def create_individual_row(row: Row, ethnicity_dict: Dict) -> Row:
    """
    Processes an input row from a DataFrame and enriches it with additional demographic and healthcare-related attributes.
    This function assumes the presence of an 'age' column in the input row.
    Args:
        row (Row): A Spark Row object that must contain the "age" field.
        ethnicity_dict (Dict): The Dictionary of ethnicities distributed for the country.

    Returns:
        Row: A new Spark Row object with the following structure:
            - Age (int): The age of the individual.
            - DOB (str): The date of birth of the individual.
            - Blood_type (str): The blood type of the individual.
            - Gender (str): The gender of the individual.
            - Name (str): The name of the individual.
            - Ethnicity (str): The ethnic background of the individual.
            - is_female (bool): A flag indicating whether the individual is female.
            - is_pediatric (bool): A flag indicating whether the individual is considered pediatric (under 18 years old).
            - is_geriatric (bool): A flag indicating whether the individual is considered geriatric (over 65 years old).
            - unique_id (str): A unique identifier for the individual.
    """
    age = row['age']
    ethnicity = choose_ethnicity(ethnicity_dict)
    gender = random_gender_chooser("uk")
    name = generate_name(ethnicity)
    dob = dob_creator(age)

    return Row(
        Age=int(age),
        DOB=dob,
        Blood_type=choose_blood_type(),
        Gender=gender,
        Name=name,
        Ethnicity=ethnicity,
        is_female=check_gender_is_female(gender),
        is_pediatric=check_patient_is_pediatric(age),
        is_geriatric=check_patient_is_geriatric(age),
        unique_id=create_unique_id(name, dob)
    )


class UrduSurnameProvider(BaseProvider):
    @staticmethod
    def urdu_surname():
        surnames = ['خان', 'حسین', 'ملک', 'رضا', 'شیخ', 'احمد', 'علی', 'قریشی', 'صدیقی',
                    'چوہدری', 'اقبال', 'جمال', 'فاروق', 'رحمٰن', 'بٹ', 'عثمان', 'حیدر',
                    'نور', 'شاہ', 'اعظم', 'سلیم', 'آصف', 'جاوید', 'مجید', 'ناصر']
        return random.choice(surnames)


locales = {
    "Indian": Faker('en_IN'),
    "Black African": Faker('en_US'),
    "Black Caribbean": Faker('en_US'),
    "Chinese": Faker('zh_CN'),
    "Pakistani": Faker('en_GB'),
    "White English": Faker('en_GB'),
    "White Scottish": Faker('en_GB'),
    "White Irish": Faker('en_IE'),
    "White other": Faker('en_GB'),
    "Arab": Faker('ar_AA'),
    "Gypsy Or Irish Traveller": [Faker('en_GB'), Faker('en_IE')],
    "Roma": Faker('en_GB'),
    "Bangladeshi": Faker('bn_BD'),
    "Mixed": [Faker('en_US'), Faker('en_IN'), Faker('en_GB')],
    "Mixed White/Asian": [Faker('en_GB'), Faker('en_IN')],
    "Mixed White/Black African": [Faker('en_GB'), Faker('en_US')],
    "Mixed White/Black Caribbean": [Faker('en_GB'), Faker('en_US')],
    "Mixed other": [Faker('en_IN'), Faker('en_GB')],
    "Mixed or multiple ethnic groups": [Faker('en_US'), Faker('en_IN'), Faker('en_GB'), Faker('ar_AA')],
    "Any Other": [Faker('en_US'), Faker('en_IN'), Faker('en_GB')]
}


def convert_chinese_to_english(name: str) -> str:
    pinyin_name = pinyin.get(name, format="strip", delimiter=" ").split(' ')
    pinyin_initials = pinyin.get_initial(name, delimiter=". ").split(' ')
    return ' '.join(pinyin_initials[:-1] + pinyin_name[-1:])


def transliterate_text(text, language):
    language_codes = {
        "Bangladeshi": "bn",  # Bengali
        "Arab": "ar",  # Arabic
        "Pakistani": "ur"  # Urdu
    }
    if language in language_codes:
        lang_code = language_codes[language]
        # Check if the language is supported
        if lang_code in get_available_language_codes():
            return translit(text, reversed=True)
    return text


def handle_name(fake: Faker, transform=None):
    name = fake.name()
    return transform(name) if transform else name


def generate_name(ethnicity=None, salutation=None) -> str:
    """
    Generate a name with optional salutation and specific count of initials.

    Args:
        ethnicity:  (str: optional): The ethnicity of the individual.
        salutation (str, optional): Prefix for the name, e.g., 'Dr.'.

    Returns:
        str: A generated name with or without initials and salutation.
    """
    entry = locales.get(ethnicity)
    if isinstance(entry, list):
        fake = random.choice(entry)
    elif isinstance(entry, Faker):
        fake = entry
    else:
        raise ValueError("Invalid ethnicity specified ", ethnicity)
    if isinstance(fake, Tuple):
        fake, transform = random.choice(entry)
        name = handle_name(fake, transform)
        return name

    if ethnicity == "Pakistani":
        fake.add_provider(UrduSurnameProvider)
    initials_count = choices([1, 2, 3], weights=[1, 0.4, 0.1], k=1)[0]
    initials = ' '.join(fake.random_uppercase_letter() + '.' for _ in range(initials_count))
    surname = fake.urdu_surname() if ethnicity == "Pakistani" else fake.last_name()
    if ethnicity == "Chinese":
        return convert_chinese_to_english(fake.name())
    if ethnicity in ["Bangladeshi", "Arab", "Pakistani"]:
        return transliterate_text(f"{initials} {surname}", ethnicity)
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
        str: DOB, given the age.
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
    return f"{clean_name(name)}|{dob}{uuid.uuid4()}"

