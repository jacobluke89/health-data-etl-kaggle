from pyspark import SparkConf

from src.constants.database_constants import SPARK_JAR_PATH, SPARK_WAREHOUSE
from pyspark.sql import SparkSession

conf = SparkConf()
conf.set("spark.default.parallelism", "8")
conf.set("spark.sql.shuffle.partitions", "8")
conf.set("hive.stats.jdbc.timeout", "30")  # Timeout in seconds
conf.set("hive.stats.retries.wait", "300")  # Wait time in milliseconds
conf.set("hive.root.logger", "WARN,console")
conf.set("hive.metastore.schema.version", "2.3.0")
conf.get("spark.sql.warehouse.dir")
conf.get("hive.metastore.uris")

spark = (SparkSession.builder.appName("Healthcare-Dataset")
         .master("local[6]")
         .config("spark.master", "local")
         .config("spark.sql.adaptive.enabled", "true")
         .config("spark.jars", SPARK_JAR_PATH)  # Adjust this to include the path to the Hive JDBC jar
         .config("spark.driver.extraClassPath", SPARK_JAR_PATH)  # Ensure the driver is aware of the JDBC jar
         .config("spark.executor.extraClassPath", SPARK_JAR_PATH)  # Ensure the executors are aware of the JDBC jar
         .config("spark.sql.debug.maxToStringFields", 10000000)
         .config("spark.sql.warehouse.dir", SPARK_WAREHOUSE)
         .config("spark.driver.memory", "6g")
         .config("spark.executor.memory", "6g")
         .config("spark.executor.cores", "4")
         .enableHiveSupport()
         .getOrCreate()
         )
