from pyspark import SparkConf

from data_generator.constants import POSTGRES_JAR_PATH, SPARK_EXEC_MEMORY, SPARK_DRIVER_MEMORY, SPARK_CORES
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
         .config("spark.driver.memory", SPARK_DRIVER_MEMORY)
         .config("spark.executor.memory", SPARK_EXEC_MEMORY)
         .config("spark.executor.cores", SPARK_CORES)
         .getOrCreate())
