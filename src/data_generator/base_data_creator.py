from typing import List, Dict

import numpy as np
from pyspark.sql import DataFrame, SparkSession

from utils.statistcs.statistical_functions import normalise_population_density, oversample_ages, create_rows_rdd
from .config import country_data_dict
from .csv_data_processor import CSVDataProcessor


class BaseDataCreator:
    """
        This class creates a distributed age using a csv file which should contain an age distribution
        from 0 to 100+, where 100+ is represented by 100 in the csv file.  This then is used to create
        an age distribution from that given file. The data is obtained from population.un.org
        Args:
            spark (SparkSession): The SparkSession
            country (str): The country we're going to create the base data for from the config.py
            dataset_size (int): the size of the dataset at the end of the process. default 10000
        Returns:
            DataFrame: A dataframe of age distributions.
            Columns contain:
            - Age (int): The age of the individual.
            - DOB (str): The date of birth of the individual.
            - Blood_type (str): The blood type of the individual.
            - Gender (str): The gender of the individual.
            - Name (str): The name of the individual.
            - Ethnicity (str): The ethnic background of the individual.
            - is_female (bool): A flag indicating whether the individual is female.
            - is_pediatric (bool): A flag indicating whether the individual is considered pediatric (under 18 years old).
            - is_geriatric (bool): A flag indicating whether the individual is considered geriatric (over 65 years old).
            - unique_id (str): A unique identifier for the individual.
    """

    def __init__(self, spark: SparkSession, country: str, dataset_size: int = 10000):
        self.ethnicity_dict = None
        self.postcode_dict = None
        self._spark = spark
        self.country = country
        self.country_data_dict = country_data_dict[country]
        self.dataset_size = dataset_size

    @staticmethod
    def normalise_data(df: DataFrame, required_columns: List) -> Dict:
        """
        Normalise the data in a DataFrame based on the values in two specified columns.

        This method takes a  DataFrame and a list of two column names. It extracts the key-value pairs from the
        specified columns and returns a dictionary with the keys and their normalised values, expressed as a percentage
        of the total sum of all values.

        Args:
            df (DataFrame): The Spark DataFrame containing the data to be normalised.
            required_columns (List): A list containing the names of the two columns to be used for normalization.
                                     The first column is treated as the key, and the second as the value.

        Returns:
            Dict: A dictionary where the keys are the values from the first column, and the values are the normalised
                  percentages of the total sum of the second column.

        """
        data_collected = df.rdd.map(lambda row: (row[required_columns[0]], row[required_columns[1]])).collect()
        dict_from_df = dict(data_collected)
        total_population = sum(dict_from_df.values())
        return {key: (value / total_population) * 100 for key, value in dict_from_df.items()}

    def get_normalised_data_dict(self, file_type: str) -> Dict:
        """
        Obtains the normalised data from the given function and checks the csv files for the given files
        against the config
        Args:
            file_type (str): e.g. ethnicity or population distribution.
        Returns:
            Dict: A dictionary where the keys are the values from the first column, and the values are the normalised
                  percentages of the total sum of the second column.
        """
        # TODO add check for file types here some countries may not have population distribution data
        config = self.country_data_dict[file_type]
        data_processor_ethnicity = CSVDataProcessor(self._spark, config["file_path"])
        df = data_processor_ethnicity.runner()
        required_columns = config["columns"]
        if not all(col in df.columns for col in required_columns):
            raise ValueError("Required columns are missing in the data")
        return self.normalise_data(df, required_columns)

    def adjust_postcode_weights(self) -> Dict | None:
        """
        Adjusts postcode weights by setting zero weights to the lower quartile of the non-zero weights
        and scales the non-zero weights so that the total sums to 100.

        Returns:
            Dict: Adjusted postcode weights where all weights sum to 100.
        """
        postcode_weights = self.get_normalised_data_dict("population_distribution")

        non_zero_weights = [weight for weight in postcode_weights.values() if weight > 0]
        if not non_zero_weights:
            print("No non-zero weights found in the data.")
            return
        # arbitrarily chose 10 here, this does need more thought.
        lower_quartile = np.percentile(non_zero_weights, 10)

        # Count zero weights and calculate the total weight to allocate to them
        zero_count = sum(1 for weight in postcode_weights.values() if weight == 0)
        total_allocated_to_zeros = lower_quartile * zero_count

        # Scale the non-zero weights to ensure the total sums to 100
        scale_factor = (100 - total_allocated_to_zeros) / sum(non_zero_weights)

        # Set zero weights to the lower quartile and adjust non-zero weights
        adjusted_weights = {}
        for postcode, weight in postcode_weights.items():
            if weight == 0:
                adjusted_weights[postcode] = lower_quartile
            else:
                adjusted_weights[postcode] = weight * scale_factor

        return adjusted_weights

    def runner(self):
        """
        Runs the base data creation
        Returns:
            A Dataframe with the defined columns as suggested at the top of this file.
        """
        # TODO add to base data tables postcode distribution calculation
        self.postcode_dict = self.adjust_postcode_weights()
        self.ethnicity_dict = self.get_normalised_data_dict("ethnicity")
        data_processor_age = CSVDataProcessor(self._spark, self.country_data_dict["age_data"]["file_path"])
        csv_age_sq_df = data_processor_age.runner()
        normalised_df = normalise_population_density(csv_age_sq_df)
        sample_rdd = oversample_ages(normalised_df, self.dataset_size)
        row_rdd = create_rows_rdd(sample_rdd, self.ethnicity_dict)
        sample_df = self._spark.createDataFrame(row_rdd)
        return sample_df.limit(self.dataset_size)
