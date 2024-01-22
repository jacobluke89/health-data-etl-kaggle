import random
from datetime import datetime
from pyspark.shell import spark
from pyspark.sql import DataFrame
from constants.admission_types_tests_dataset import new_admission_types, sub_admission_types, stay_type, admission_tests
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType


def get_row_count(df: DataFrame):
    """
    Returns the number of rows in a DataFrame.

    Parameters:
    df (DataFrame): A PySpark DataFrame.

    """
    print(df.count())

@udf(StringType())
def generate_dob():
    start_year = 1925
    end_year = 2015

    # Generate random year, month, and day
    year = random.randint(start_year, end_year)
    month = random.randint(1, 12)

    # Check for leap year if month is February
    if month == 2:
        if (year % 400 == 0) or ((year % 100 != 0) and (year % 4 == 0)):
            day = random.randint(1, 29)
        else:
            day = random.randint(1, 28)
    elif month in [4, 6, 9, 11]:
        day = random.randint(1, 30)
    else:
        day = random.randint(1, 31)

    # date as YYYYMMDD
    dob = datetime(year, month, day).strftime("%Y%m%d")
    return dob

def create_new_admission_data():
    admission = random.randint(0, len(new_admission_types))
    print(admission)
    print(new_admission_types[admission])