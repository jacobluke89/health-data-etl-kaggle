from pyspark.sql import SparkSession

from data_generator.csv_data_processor import CSVDataProcessor

if __name__ == '__main__':

    spark = SparkSession.builder.appName("ETL").getOrCreate()

    csv_reader = CSVDataProcessor(spark, "data/healthcare_dataset.csv")

    df = csv_reader.run()

    df.show()
