from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType

def create_table(spark: SparkSession,
                 database: str,
                 table_name: str,
                 schema: StructType =
                 None, write_format: str = "parquet"):
    """
    This function creates a table if it does not exist.
    Args:
        spark (SparkSession):  The SparkSession
        database (str): The database we're creating a table for
        table_name (str): The table name
        schema (StructType): The tables schema
        write_format (str): The write format, default parquet format
    """
    table_exist = spark.catalog.tableExists(table_name, database)
    if not table_exist:
        df = spark.createDataFrame([], schema)
        df.write.format(write_format).saveAsTable(f"{database}.{table_name}")
        print(f"created table {database}.{table_name}")
    print(f"table already exists, {database}.{table_name}")

def modify_table(df: DataFrame, database: str, table_name: str, mode="append", write_format: str = "parquet"):
    """

    Args:
        df:
        database:
        table_name:
        mode:
        write_format:

    Returns:

    """
    df.write.mode(mode).format(write_format).saveAsTable(f"{database}.{table_name}")
