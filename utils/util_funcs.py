from typing import List

from IPython.core.display_functions import display
from pyspark.sql import DataFrame


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

def display_df(spark_df: DataFrame,  num_rows: int = 20, select_rows: List = None):
    if select_rows:
        spark_df = spark_df.select(select_rows)
    pandas_df = spark_df.toPandas()
    display(pandas_df.head(num_rows))

def get_column_names(df: DataFrame):
    column_names = df.columns
    print(column_names)

