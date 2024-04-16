from random import choices

import numpy as np
import pandas as pd
from faker import Faker
from pyspark.sql.pandas.functions import pandas_udf
from pyspark.sql.types import DateType, StringType

from spark_instance import spark
from utils.util_funcs import generate_name


@pandas_udf(DateType())
def create_random_dob_pandas_udf(ages: pd.Series) -> pd.Series:
    today = pd.Timestamp('today').normalize()

    preliminary_dobs = today - pd.to_timedelta(ages * 365, unit='d')
    random_days = np.random.randint(0, 365, size=len(ages))
    # Calculate the final DOB
    final_dobs = preliminary_dobs - pd.to_timedelta(random_days, unit='d')
    return final_dobs


@pandas_udf(StringType())
def create_fake_name_udf(size: pd.Series) -> pd.Series:
    """
    Generate a series of fake names based on the size of the input series.

    Args:
        size (pd.Series): Series whose length determines the number of names to generate.

    Returns:
        pd.Series: A series of generated names.
    """
    fake = Faker()
    names = [generate_name(fake) for _ in range(len(size))]
    return pd.Series(names)


population_weights = {
    "uk": {"male": 48, "female": 52},
    # Add more countries as needed
}

broad_weights = spark.sparkContext.broadcast(population_weights)

@pandas_udf(StringType())
def random_gender_pd_udf(cntry: pd.Series) -> pd.Series:
    """
    This function will generate a random gender for a row
    It will weight it accordance with the country passed in.
    Data for this can be found at population.un.org
    Args:
        cntry: the chosen country e.g. uk, used to obtain population weights from
        the population_weights dictionary
    Returns:
        a given gender, Male or Female
    """
    weights_dict = broad_weights.value

    def get_gender(country):
        if country in weights_dict:
            weights = weights_dict[country]
            return choices(["Male", "Female"], weights=[weights["male"], weights["female"]], k=1)[0]
        else:
            print(f"Country, {country} not in the weights dictionary")
            return choices(["Male", "Female"], weights=[50, 50], k=1)[0]

    return cntry.apply(get_gender)


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

@pandas_udf(StringType())
def choose_blood_type_udf(dummy: pd.Series) -> pd.Series:
    """
    This function randomly chooses a blood type based on the blood type
    distribution, this information was found at
    https://www.blood.co.uk/why-give-blood/blood-types/
    therefore is uk specific
    Args:
        dummy: required to apply the lambda
    Returns:
        a blood type
    """
    types = list(blood_type_distribution.keys())
    weights = list(blood_type_distribution.values())
    return dummy.apply(lambda x: choices(types, weights=weights, k=1)[0])
