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

def display_df(spark_df: DataFrame):
    pandas_df = spark_df.toPandas()
    display(pandas_df)
