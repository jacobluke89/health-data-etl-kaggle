# import random
# from datetime import datetime
# from typing import Any, Tuple
#
# from pyspark.sql.functions import udf
# from pyspark.sql.types import StringType, StructType, StructField
#
# from constants.admission_types_tests_dataset import admission_mapping, admission_tests
#
#
# class DataTypeCols:
#     ADMISSION = "ADMISSION_TYPE"
#     SUB_ADMISSION = "SUB_ADMISSION_TYPE"
#     STAY = "STAY_TYPE"
#     TESTS = "TESTS_SUGGESTED"
#
#
# class AdmissionProcessor:
#
#     @staticmethod
#     def _select_random_tests(sub_admission_type):
#         tests = admission_tests.get(sub_admission_type, [])
#         number_of_tests = random.randint(1, len(tests))
#         return random.sample(tests, number_of_tests)
#
#     @staticmethod
#     def _select_sub_admission(sub_admission_dict, exclude_types=None):
#         if exclude_types is None:
#             exclude_types = []
#         valid_admissions = [admission for admission in sub_admission_dict.keys() if admission not in exclude_types]
#         return random.choice(valid_admissions) if valid_admissions else None
#
#     @staticmethod
#     def _check_geriatric_age(p_age: int, admission: str) -> str | None:
#         if admission == "geriatrics" and p_age < 65:
#             return None
#         return admission
#
#     @classmethod
#     def create_new_admission_data(cls, gender: str, dob: str) -> tuple[str | Any, str, Any, Any]:
#         female_only = ["maternity", "obstetrics"]
#         today = datetime.now()
#         dob_date = datetime.strptime(dob, "%Y%m%d")
#         age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
#         ped_case = "pediatric_" if age < 18 else ''
#
#         selected_new_admission_type = random.choice(list(admission_mapping.keys()))
#         sub_admission_dict = admission_mapping[selected_new_admission_type]
#
#         exclude_types = female_only if gender.lower() == "male" else []
#         selected_sub_admission_type = None
#
#         while selected_sub_admission_type is None:
#             temp_type = cls._select_sub_admission(sub_admission_dict, exclude_types)
#             selected_sub_admission_type = cls._check_geriatric_age(age, temp_type)
#             if gender.lower() == 'female' and selected_sub_admission_type in female_only and age < 16:
#                 selected_sub_admission_type = None
#
#         selected_stay_type = random.choice(list(sub_admission_dict[selected_sub_admission_type]))
#         selected_tests = cls._select_random_tests(selected_sub_admission_type)
#
#         return (ped_case + selected_new_admission_type,
#                 ped_case + selected_sub_admission_type,
#                 selected_stay_type,
#                 selected_tests)
#
#
# new_data_schema = StructType([
#     StructField(DataTypeCols.ADMISSION, StringType(), False),
#     StructField(DataTypeCols.SUB_ADMISSION, StringType(), False),
#     StructField(DataTypeCols.STAY, StringType(), False),
#     StructField(DataTypeCols.TESTS, StringType(), False)
#
# ])
#
# @udf(new_data_schema)
# def create_new_admission_data(gender: str, dob: str) -> Tuple[str | Any, str, Any, Any]:
#     return AdmissionProcessor.create_new_admission_data(gender, dob)
