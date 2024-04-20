from pyspark.errors import AnalysisException
from pyspark.pandas import DataFrame

from spark_instance import spark
from constants.database_constants import properties, POSTGRES_URL

def read_postgres_table(table_name: str):
    return spark.read.jdbc(url=POSTGRES_URL, table=table_name, properties=properties)

def write_postgres_table(df: DataFrame, table_name: str, mode: str = "overwrite"):
    try:
        # Ensure 'df' is a DataFrame and 'mode' is one of the allowed modes
        # if not isinstance(df, DataFrame):
        #     raise ValueError("df must be a DataFrame")
        if mode not in ["overwrite", "append", "ignore", "error", "errorifexists"]:
            raise ValueError("Invalid write mode specified")

        df.write.jdbc(url=POSTGRES_URL, table=table_name, mode=mode, properties=properties)
    except AnalysisException as e:
        print(f"Could not write table: {e}")
    except Exception as e:
        print(f"There was an error writing table: {e}")
