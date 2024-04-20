from pyspark import SparkConf

from constants.database_constants import POSTGRES_JAR_PATH
from pyspark.sql import SparkSession

conf = SparkConf()
conf.set("spark.default.parallelism", "200")
conf.set("spark.sql.shuffle.partitions", "200")

spark = (SparkSession.builder.appName("ETL")
         .master("local[*]")
         .config("spark.master", "local")
         .config("spark.sql.adaptive.enabled", "true")
         .config("spark.jars", POSTGRES_JAR_PATH)
         .config("spark.sql.debug.maxToStringFields", 10000000)
         .config("spark.driver.memory", "8g")
         .config("spark.executor.memory", "8g")
         .config("spark.executor.cores", "4")
         .getOrCreate()
         )

