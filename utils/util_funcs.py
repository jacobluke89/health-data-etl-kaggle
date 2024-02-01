from pyspark.sql import DataFrame
from pyspark.sql.functions import floor, datediff, current_date, col, to_date


def get_row_count(df: DataFrame):
    """
    Returns the number of rows in a DataFrame.

    Parameters:
    df (DataFrame): A PySpark DataFrame.

    """
    print(df.count())
    return df.count()

def display_df(spark_df: DataFrame):
    pandas_df = spark_df.toPandas()
    display(pandas_df)
