from data_generator.constants import POSTGRES_JAR_PATH
from pyspark.sql import SparkSession

spark = (SparkSession.builder.appName("ETL")
         .config("spark.master", "local")
         .master("local[*]")
         .config("spark.jars", POSTGRES_JAR_PATH)
         .config("spark.sql.debug.maxToStringFields", 10000000)
         .config("spark.driver.memory", "8g")
         .getOrCreate()
         )
