from utils.util_funcs import create_doctor_names_for_all_specialties
from .type_constants import (SubAdmissionTypes,
                             StayTypeCombinations,
                             ConditionsOrDiagnosis,
                             ConditionTests,
                             AdmissionTypes)

doctor_names_all_specialties = create_doctor_names_for_all_specialties()


def base_structure(sub_admission_type, stay_type):
    stay_types_dict = {
        'all': StayTypeCombinations.ALL_TYPES.value,
        'in': StayTypeCombinations.INPATIENT.value,
        'out': StayTypeCombinations.OUTPATIENT.value,
        'day': StayTypeCombinations.DAY_PATIENT.value,
        'day_out': StayTypeCombinations.DAY_PATIENT_OUTPATIENT.value,
        'day_in': StayTypeCombinations.INPATIENT_DAY_PATIENT.value,
        'in_out': StayTypeCombinations.INPATIENT_OUTPATIENT.value
    }

    conditions = ConditionsOrDiagnosis[sub_admission_type.name].value if sub_admission_type.name in ConditionsOrDiagnosis.__members__ else ["No conditions"]
    tests = ConditionTests[sub_admission_type.name].value if sub_admission_type.name in ConditionTests.__members__ else ["No tests"]

    return {
        'stay_types': stay_types_dict[stay_type],
        'conditions': conditions,
        'tests': tests,
        'doctors': doctor_names_all_specialties[sub_admission_type.name]
    }


admission_mapping = {
    AdmissionTypes.EMERGENCY: {
        SubAdmissionTypes.INJURY_RTC: base_structure(SubAdmissionTypes.INJURY_RTC, 'day_in'),
        SubAdmissionTypes.SELF_INFLICTED: base_structure(SubAdmissionTypes.SELF_INFLICTED, "in"),
        SubAdmissionTypes.CARDIOLOGY: base_structure(SubAdmissionTypes.CARDIOLOGY, "day_in"),
        SubAdmissionTypes.NEUROLOGY: base_structure(SubAdmissionTypes.NEUROLOGY, "all"),
        SubAdmissionTypes.GASTROENTEROLOGY: base_structure(SubAdmissionTypes.GASTROENTEROLOGY, "all"),
        SubAdmissionTypes.RESPIRATORY: base_structure(SubAdmissionTypes.RESPIRATORY, 'all'),
        SubAdmissionTypes.INFECTIOUS_DISEASES: base_structure(SubAdmissionTypes.INFECTIOUS_DISEASES, "day_in"),
        SubAdmissionTypes.MATERNITY: base_structure(SubAdmissionTypes.MATERNITY, 'all'),
        SubAdmissionTypes.PSYCHIATRIC: base_structure(SubAdmissionTypes.PSYCHIATRIC, 'all'),
        SubAdmissionTypes.ORTHOPEDICS: base_structure(SubAdmissionTypes.ORTHOPEDICS, 'all')
    },
    AdmissionTypes.GP_REFERRAL: {
        SubAdmissionTypes.PSYCHIATRIC: base_structure(SubAdmissionTypes.PSYCHIATRIC, 'all'),
        SubAdmissionTypes.ORTHOPEDICS: base_structure(SubAdmissionTypes.ORTHOPEDICS, 'out'),
        SubAdmissionTypes.GASTROENTEROLOGY: base_structure(SubAdmissionTypes.GASTROENTEROLOGY, 'all'),
        SubAdmissionTypes.ENDOCRINOLOGY: base_structure(SubAdmissionTypes.ENDOCRINOLOGY, 'out'),
        SubAdmissionTypes.DERMATOLOGY: base_structure(SubAdmissionTypes.DERMATOLOGY, 'out'),
        SubAdmissionTypes.MATERNITY: base_structure(SubAdmissionTypes.MATERNITY, 'all'),
        SubAdmissionTypes.GERIATRICS: base_structure(SubAdmissionTypes.GERIATRICS, 'in_out'),
        SubAdmissionTypes.ONCOLOGY: base_structure(SubAdmissionTypes.ONCOLOGY, 'all')
    },
    AdmissionTypes.HOSPITAL_REFERRAL: {
        SubAdmissionTypes.CARDIOLOGY: base_structure(SubAdmissionTypes.CARDIOLOGY, "all"),
        SubAdmissionTypes.NEPHROLOGY: base_structure(SubAdmissionTypes.NEPHROLOGY, "all"),
        SubAdmissionTypes.NEUROLOGY: base_structure(SubAdmissionTypes.NEUROLOGY, "all"),
        SubAdmissionTypes.ONCOLOGY: base_structure(SubAdmissionTypes.ONCOLOGY, "all"),
        SubAdmissionTypes.HEMATOLOGY: base_structure(SubAdmissionTypes.HEMATOLOGY, "all"),
        SubAdmissionTypes.UROLOGY: base_structure(SubAdmissionTypes.UROLOGY, "all"),
        SubAdmissionTypes.GASTROINTESTINAL_DISORDERS: base_structure(SubAdmissionTypes.GASTROINTESTINAL_DISORDERS, "all"),
        SubAdmissionTypes.RESPIRATORY: base_structure(SubAdmissionTypes.RESPIRATORY, 'all'),
        SubAdmissionTypes.MUSCULOSKELETAL: base_structure(SubAdmissionTypes.MUSCULOSKELETAL, 'all'),
        SubAdmissionTypes.OTORHINOLARYNGOLOGY_ENT: base_structure(SubAdmissionTypes.OTORHINOLARYNGOLOGY_ENT, 'all'),
    },
    AdmissionTypes.SELF_REFERRAL: {
        SubAdmissionTypes.PSYCHIATRIC: base_structure(SubAdmissionTypes.PSYCHIATRIC, 'out'),
        SubAdmissionTypes.DERMATOLOGY: base_structure(SubAdmissionTypes.DERMATOLOGY, 'out'),
        SubAdmissionTypes.ORTHOPEDICS: base_structure(SubAdmissionTypes.ORTHOPEDICS, 'out'),
        SubAdmissionTypes.GASTROENTEROLOGY: base_structure(SubAdmissionTypes.GASTROENTEROLOGY, 'out'),
        SubAdmissionTypes.OPHTHALMOLOGY: base_structure(SubAdmissionTypes.OPHTHALMOLOGY, 'out'),
        SubAdmissionTypes.ENDOCRINOLOGY: base_structure(SubAdmissionTypes.ENDOCRINOLOGY, 'out'),
    },
    AdmissionTypes.ELECTIVE: {
        SubAdmissionTypes.MATERNITY: base_structure(SubAdmissionTypes.MATERNITY, 'all'),
    }
}
