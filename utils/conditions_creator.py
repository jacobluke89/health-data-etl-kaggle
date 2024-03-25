from collections import defaultdict
from typing import Tuple

import numpy as np
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, when, collect_list, struct, udf
from pyspark.sql.types import BooleanType

from constants.type_constants import SubAdmissionTypes


class ConditionsCreator:

    def __init__(self, spark: SparkSession, driver_df: DataFrame, probability_df: DataFrame):
        self._spark = spark
        self.driver_df = driver_df
        self.probability_df = probability_df
        self.check_age_probability = udf(ConditionsCreator.check_age_probability, BooleanType())

    @staticmethod
    def _find_probability_for_age_gender(age: int,
                                         condition_probabilities: Tuple[Tuple[int, int], float]) -> float | int:
        """
        This function returns probability based on age and a given condition probability list.
        Args:
            age: The age we will be comparing to
            condition_probabilities: The list of conditional probabilities
    
        Returns:
            int: the probability, if 0 returns, edge case, should be investigated.
        """
        (age_min, age_max), prob = condition_probabilities
        if age_min <= age <= age_max:
            return prob
        return 0

    @staticmethod
    def _filter_female_conditions(f_df: DataFrame) -> DataFrame:
        """
        Filters out entries from a DataFrame based on gender and age criteria:
        - Excludes female-only conditions (MATERNITY, OBSTETRICS) for non-female subjects.
        - Applies age restrictions specifically for MATERNITY-related entries.
        - Filter pediatric patients who cannot be pregnant (based on legal age in the UK, 16)
          No assumption made an individual cannot choose to get pregnant before this age.
          upper age bound defined  here: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4822427/#:~:text=Menopause%20typically%20occurs%20between%2045,reproducing%20many%20years%20before%20menopause.
          between 45 and 55 upper bounding will be 50.
          # TODO Possibility to include outliers in a new func in the future.
        Args:
            f_df (DataFrame): The input DataFrame with condition and demographic data.
    
        Returns:
            DataFrame: The filtered DataFrame.
        """

        female_only = [SubAdmissionTypes.MATERNITY.name,
                       SubAdmissionTypes.OBSTETRICS.name]  # TODO Obstetrics needs sorting still.

        filtered_df = f_df.filter((~(col("top_level_admission").isin(female_only))) & (~col("is_female")))

        filtered_df = filtered_df.withColumn("Age_Filter",
                                             when((col("top_level_admission") == SubAdmissionTypes.MATERNITY.name) &
                                                  ((col("Age") < 16) | (col("Age") > 50)),
                                                  False).otherwise(True))

        # Filter rows based on the Age_Filter col
        filtered_df = filtered_df.filter(col("Age_Filter")).drop("Age_Filter")

        return filtered_df.filter(
            (~col("is_female") & (col("condition_gender") != "female")) |
            (col("condition_gender").isNull()) | col("is_female")
        )

    @staticmethod
    def _filter_geriatric_conditions(g_df: DataFrame) -> DataFrame:
        """
        This function filters all GERIATRIC submission types
        Args:
            g_df (DataFrame): The unfiltered dataframe
    
        Returns:
            DataFrame: The filtered dataframe
        """
        return g_df.filter(~(col("sub_level_admission") == SubAdmissionTypes.GERIATRICS.name) & ~col("is_geriatric"))

    @staticmethod
    def check_age_probability(age: float, age_min: float, age_max: float, probability: float) -> bool:
        """
        udf function which returns a boolean True if the age is with in the age bracket and probability is above 0.
        Args:
            age (float) : The age of the patient.
            age_min (float) :  The minimum age of the patient defined within the probability bracket 
            age_max (float) :  The maximum age of the patient defined within the probability bracket. 
            probability (float) : The probability of the patient having the condition
        Returns:
            boolean: True or False 
        """
        if probability > 0 and age_min <= age <= age_max:
            return True
        else:
            return False

    def _filter_df(self, df_joined: DataFrame) -> DataFrame:
        df_filtered = df_joined.filter((col("age") >= col("age_min")) & (col("age") <= col("age_max")))

        df_filtered_female = self._filter_female_conditions(df_filtered)
        df_filtered_geriatric = self._filter_geriatric_conditions(df_filtered_female)

        df_ordered = df_filtered_geriatric.orderBy(col("unique_id"))

        check_age_probability_udf = self.check_age_probability

        df_checked_probability = df_ordered.withColumn("valid_probability",
                                                       check_age_probability_udf("Age", "age_min", "age_max",
                                                                                 "probability"))

        return (df_checked_probability.withColumn("probability_entry",
                                                  when(col("valid_probability"),
                                                       struct(col("age_min"), col("age_max"),
                                                              col("probability"))
                                                       )
                                                  ).withColumn("row_info",
                                                               when(col("valid_probability"),
                                                                    struct(
                                                                        col("Age"),
                                                                        col("condition"),
                                                                        col("is_pediatric"),
                                                                        col("unique_id"),
                                                                        col("stay_types"),
                                                                        col("condition_admission_type"),
                                                                        col("top_level_admission")
                                                                    )
                                                                    )
                                                               ).filter(col("valid_probability"))
                )

    @staticmethod
    def _aggregate_data(transformed_df: DataFrame) -> DataFrame:
        return transformed_df.groupBy("unique_id").agg(
            collect_list("probability_entry").alias("probability_entries"),
            collect_list("row_info").alias("row_infos"))

    def _choose_conditions_for_patients(self) -> DataFrame:
        """
        This function chooses a condition for a patient based on the age and looking at the condition_age_probability_dict
        Returns:
            A condition that will be assigned to the patient or None if issues found.
        """
        df_joined = self.driver_df.join(self.probability_df,
                                        self.driver_df.admission_type == self.probability_df.condition_admission_type,
                                        how="inner")

        df_transformed = self._filter_df(df_joined)

        df_aggregated = self._aggregate_data(df_transformed)

        conditions_probabilities = []
        patients_conditions = defaultdict(list)
        for row in df_aggregated.toLocalIterator():
            unique_id = row["unique_id"]
            probability_entries = [((entry.age_min, entry.age_max), entry.probability) for entry in
                                   row["probability_entries"]]
            row_infos = [(entry.Age, entry.condition, entry.is_pediatric, entry.unique_id, entry.stay_types, entry.condition_admission_type,
                          entry.top_level_admission) for entry in row["row_infos"]]
            for probability_info, patient_info in zip(probability_entries, row_infos):
                age, condition, is_pediatric, unique_id, stay_types, condition_admission_type, top_level_admission = patient_info
                age_prob = probability_info

                prob = self._find_probability_for_age_gender(age, age_prob)
                if prob > 0:
                    condition_label = f"pediatric_{condition}" if is_pediatric else condition
                else:
                    condition_label = "pediatric no condition for patient edge case" if is_pediatric else "no condition for patient edge case"
                    prob = 0

                conditions_probabilities.append(
                    (f"{unique_id}_{top_level_admission}_{condition_admission_type}", condition_label, prob))
                patient_name = unique_id.split('_')[0]
                patients_conditions[patient_name].append((unique_id, stay_types, top_level_admission, condition_label, prob))

        # Sort the conditions by probability for easier handling (optional)
        conditions_probabilities.sort(key=lambda x: x[1], reverse=True)
        # Step 2: Select a condition for each patient
        chosen_conditions_list = []
        for patient, conditions in patients_conditions.items():
            total_prob = sum(prob for _, _, prob in conditions_probabilities)
            condition_selected = False
            while not condition_selected:
                random_prob = np.random.uniform(0, total_prob)
                cumulative_prob = 0
                for uniq_id, stay_types, top_level, condition, prob in conditions:
                    cumulative_prob += prob
                    if random_prob < cumulative_prob:
                        chosen_conditions_list.append((uniq_id, stay_types, top_level, condition))
                        condition_selected = True
                        break  # Stop after selecting one condition for the current patient
        return self._spark.createDataFrame(chosen_conditions_list,
                                           ("unique_id", "stay_types", "chosen_top_level_admission", "chosen_condition"))

    def runner(self):
        return self._choose_conditions_for_patients()
