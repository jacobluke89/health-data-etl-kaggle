from spark_instance import spark
from utils.read_write import read_postgres_table

if __name__ == '__main__':

    _spark = spark

    df = read_postgres_table("dob_age_raw_data")
