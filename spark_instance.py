
from data_generator.constants import POSTGRES_JAR_PATH
from pyspark.sql import SparkSession

spark = (SparkSession.builder.appName("ETL")
         .config("spark.master", "local")
             .config("spark.jars", POSTGRES_JAR_PATH)
         .getOrCreate()
         )
