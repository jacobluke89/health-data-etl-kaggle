from collections import defaultdict
from typing import Tuple, List, Any

import numpy as np
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, when, collect_list, struct, broadcast
from pyspark.sql.types import StructType, StructField, StringType

from constants.type_constants import SubAdmissionTypes


class ConditionsCreator:

    def __init__(self, spark: SparkSession, driver_df: DataFrame, probability_df: DataFrame, enum_df: DataFrame):
        self._spark = spark
        self.driver_df = driver_df
        self.probability_df = probability_df
        self.enum_df = enum_df

    @staticmethod
    def _find_probability_for_age_gender(age: int,
                                         condition_probabilities: Tuple[Tuple[int, int], float]) -> float | int:
        """
        This function returns probability based on age and a given condition probability.
        Args:
            age (int): The age we will be comparing to
            condition_probabilities (Tuple[Tuple[int, int], float]): The Tuple of conditional probability

        Returns:
            int: the probability, if 0 returns, edge case, should be investigated.
        """
        (age_min, age_max), prob = condition_probabilities
        if age_min <= age <= age_max:
            return prob
        return 0

    @staticmethod
    def _filter_conditions(f_df: DataFrame) -> DataFrame:
        """
        Filters out entries from a DataFrame based on gender and age criteria:
        - Excludes female-only conditions (MATERNITY, OBSTETRICS) for non-female subjects.
        - Applies age restrictions specifically for MATERNITY-related entries.
        - Filter pediatric patients who cannot be pregnant (based on legal age in the UK, 16)
          No assumption made an individual cannot choose to get pregnant before this age.
          upper age bound defined  here: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4822427/#:~:text=Menopause%20typically%20occurs%20between%2045,reproducing%20many%20years%20before%20menopause.
          between 45 and 55 upper bounding will be 50.
        - Includes conditions with no gender specified or conditions applicable to females
          # TODO Possibility to include outliers in a new func in the future.
        Args:
            f_df (DataFrame): The input DataFrame with condition and demographic data.

        Returns:
            DataFrame: The filtered DataFrame.
        """

        female_only = [SubAdmissionTypes.MATERNITY.name,
                       SubAdmissionTypes.OBSTETRICS.name]  # TODO Obstetrics needs sorting still.
        female_only_conditions = ["Cervical Cancer",
                                  "Ovarian Cancer",
                                  "Polycystic Ovary Syndrome (PCOS)"]
        male_only_conditions = ["Prostate Cancer",
                                "Testicular Cancer"]
        return f_df.filter(
            # Exclude male patients with female-only conditions
            (~(col("top_level_admission").isin(female_only)) & (~col("is_female"))) |
            # Include all female patients but apply age filter for specific conditions and remove male only conditions
            (col("is_female")
             & ~((col("top_level_admission") == SubAdmissionTypes.MATERNITY.name) &
                 ((col("Age") < 16) | (col("Age") > 50)))
             | col("condition").isin(male_only_conditions)
             ) |
            # Filter female conditions from male patients
            (~col("is_female") & col("condition").isin(female_only_conditions)) |
            # Filter for geriatric conditions
            (~((col("sub_level_admission") == SubAdmissionTypes.GERIATRICS.name) & ~col("is_geriatric"))) |
            # Include conditions with no gender specified or conditions applicable to females
            (col("condition_gender").isNull()) |
            (col("is_female") & (col("condition_gender") != "female"))
        )

    def _filter_df(self, df_joined: DataFrame) -> DataFrame:
        """
        This function is the driver for filtering the df prior to data aggregation.
        Args:
            df_joined (DataFrame): The unfiltered dataframe
        Returns:
            DataFrame: The filtered data.
        """
        filter_condition = (col("age") >= col("age_min")) & (col("age") <= col("age_max"))
        df_filtered = df_joined.filter(filter_condition)

        df_filtered_conditions = self._filter_conditions(df_filtered)

        return (df_filtered_conditions.withColumn("probability_entry",
                                                  when(filter_condition,
                                                       struct(col("age_min"), col("age_max"),
                                                              col("probability"))
                                                       )
                                                  ).withColumn("row_info",
                                                               when(filter_condition,
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
                                                               )
                ).orderBy(col("unique_id"))

    @staticmethod
    def _aggregate_data(transformed_df: DataFrame) -> DataFrame:
        """
        This function aggregates the data grouping by the unique_id
        Args:
            transformed_df (DataFrame): the "un-aggregated" Data
        Returns:
            DataFrame: The aggregated data
        """
        return transformed_df.groupBy("unique_id").agg(
            collect_list("probability_entry").alias("probability_entries"),
            collect_list("row_info").alias("row_infos"))

    def _iterate_aggregate_data(self, aggregated_df: DataFrame) \
            -> Tuple[List[Tuple[str, str | Any, float | int]], defaultdict[Any, list]]:
        """
        This function loops over the aggregated data and unpacks the probability entries and row infos for each
        patient.  Then finds the probability for that gender and appends accordingly
        Args:
            aggregated_df: containing the probability entries and row infos

        Returns:
            Tuple[List[Tuple[str, str | Any, float | int]], default-dict[Any, list]]
        """
        conditions_probabilities = []
        patients_conditions = defaultdict(list)

        for row in aggregated_df.toLocalIterator():
            probability_entries = [((entry.age_min, entry.age_max), entry.probability) for entry in
                                   row["probability_entries"]]
            row_infos = [(entry.Age, entry.condition, entry.is_pediatric, entry.unique_id, entry.stay_types,
                          entry.condition_admission_type,
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
                patients_conditions[patient_name].append(
                    (unique_id, stay_types, condition_admission_type, top_level_admission, condition_label, prob))
        conditions_probabilities.sort(key=lambda x: x[1], reverse=True)
        return conditions_probabilities, patients_conditions

    def _choose_conditions_for_patients(self) -> DataFrame:
        """
        This function chooses a condition for a patient based on the age and looking at the 
        condition_age_probability_dict
        Returns:
            Dataframe: Returns a condition for each patient that will be assigned to them.
        """
        # no point in joining on to probabilities that are 0 
        self.probability_df = self.probability_df.filter(col("probability") != 0)
        df_enum_cross = self.driver_df.crossJoin(self.enum_df)
        df_joined = df_enum_cross.join(broadcast(self.probability_df),
                                       df_enum_cross.admission_type == self.probability_df.condition_admission_type,
                                       how="inner")

        df_transformed = self._filter_df(df_joined)

        df_transformed = df_transformed.repartition(4, "unique_id")

        df_aggregated = self._aggregate_data(df_transformed)
        conditions_probabilities, patients_conditions = self._iterate_aggregate_data(df_aggregated)

        chosen_conditions_list = []
        for patient, conditions in patients_conditions.items():
            total_prob = sum(prob for _, _, prob in conditions_probabilities)
            condition_selected = False
            while not condition_selected:
                random_prob = np.random.uniform(0, total_prob)
                cumulative_prob = 0
                for uniq_id, stay_types, submission_type, top_level, condition, prob in conditions:
                    if "no condition for patient edge case" in condition:
                        chosen_conditions_list.append((uniq_id, stay_types, submission_type, top_level, condition))
                    cumulative_prob += prob
                    if random_prob < cumulative_prob:
                        chosen_conditions_list.append((uniq_id, stay_types, submission_type, top_level, condition))
                        condition_selected = True
                        break  # Stop after selecting one condition for the current patient
        return self._spark.createDataFrame(chosen_conditions_list,
                                           StructType([
                                               StructField("unique_id", StringType()),
                                               StructField("stay_types", StringType()),
                                               StructField("submission_type", StringType()),
                                               StructField("chosen_top_level_admission", StringType()),
                                               StructField("chosen_condition", StringType())
                                           ])
                                           )

    def runner(self) -> DataFrame:
        """
        Runner function for this class.
        Returns:
            DataFrame : A DataFrame of chosen conditions, as defined in the schema in this return function call:
            see self._choose_conditions_for_patients()
        """
        return self._choose_conditions_for_patients()
