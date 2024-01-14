from pyspark.shell import spark
from pyspark.sql import DataFrame


def get_row_count(df: DataFrame):
    """
    Returns the number of rows in a DataFrame.

    Parameters:
    df (DataFrame): A PySpark DataFrame.

    """
    print(df.count())

