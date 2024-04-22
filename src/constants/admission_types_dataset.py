from ..utils.util_funcs import create_doctor_names_for_all_specialties
from .type_constants import (DepartmentTypes,
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
        DepartmentTypes.INJURY_RTC: base_structure(DepartmentTypes.INJURY_RTC, 'day_in'),
        DepartmentTypes.SELF_INFLICTED: base_structure(DepartmentTypes.SELF_INFLICTED, "in"),
        DepartmentTypes.CARDIOLOGY: base_structure(DepartmentTypes.CARDIOLOGY, "day_in"),
        DepartmentTypes.NEUROLOGY: base_structure(DepartmentTypes.NEUROLOGY, "all"),
        DepartmentTypes.GASTROENTEROLOGY: base_structure(DepartmentTypes.GASTROENTEROLOGY, "all"),
        DepartmentTypes.RESPIRATORY: base_structure(DepartmentTypes.RESPIRATORY, 'all'),
        DepartmentTypes.INFECTIOUS_DISEASES: base_structure(DepartmentTypes.INFECTIOUS_DISEASES, "day_in"),
        DepartmentTypes.MATERNITY: base_structure(DepartmentTypes.MATERNITY, 'all'),
        DepartmentTypes.PSYCHIATRIC: base_structure(DepartmentTypes.PSYCHIATRIC, 'all'),
        DepartmentTypes.ORTHOPEDICS: base_structure(DepartmentTypes.ORTHOPEDICS, 'all')
    },
    AdmissionTypes.GP_REFERRAL: {
        DepartmentTypes.PSYCHIATRIC: base_structure(DepartmentTypes.PSYCHIATRIC, 'all'),
        DepartmentTypes.ORTHOPEDICS: base_structure(DepartmentTypes.ORTHOPEDICS, 'out'),
        DepartmentTypes.GASTROENTEROLOGY: base_structure(DepartmentTypes.GASTROENTEROLOGY, 'all'),
        DepartmentTypes.ENDOCRINOLOGY: base_structure(DepartmentTypes.ENDOCRINOLOGY, 'out'),
        DepartmentTypes.DERMATOLOGY: base_structure(DepartmentTypes.DERMATOLOGY, 'out'),
        DepartmentTypes.MATERNITY: base_structure(DepartmentTypes.MATERNITY, 'all'),
        DepartmentTypes.GERIATRICS: base_structure(DepartmentTypes.GERIATRICS, 'in_out'),
        DepartmentTypes.ONCOLOGY: base_structure(DepartmentTypes.ONCOLOGY, 'all')
    },
    AdmissionTypes.HOSPITAL_REFERRAL: {
        DepartmentTypes.CARDIOLOGY: base_structure(DepartmentTypes.CARDIOLOGY, "all"),
        DepartmentTypes.NEPHROLOGY: base_structure(DepartmentTypes.NEPHROLOGY, "all"),
        DepartmentTypes.NEUROLOGY: base_structure(DepartmentTypes.NEUROLOGY, "all"),
        DepartmentTypes.ONCOLOGY: base_structure(DepartmentTypes.ONCOLOGY, "all"),
        DepartmentTypes.HEMATOLOGY: base_structure(DepartmentTypes.HEMATOLOGY, "all"),
        DepartmentTypes.UROLOGY: base_structure(DepartmentTypes.UROLOGY, "all"),
        DepartmentTypes.GASTROINTESTINAL_DISORDERS: base_structure(DepartmentTypes.GASTROINTESTINAL_DISORDERS, "all"),
        DepartmentTypes.RESPIRATORY: base_structure(DepartmentTypes.RESPIRATORY, 'all'),
        DepartmentTypes.MUSCULOSKELETAL: base_structure(DepartmentTypes.MUSCULOSKELETAL, 'all'),
        DepartmentTypes.OTORHINOLARYNGOLOGY_ENT: base_structure(DepartmentTypes.OTORHINOLARYNGOLOGY_ENT, 'all'),
    },
    AdmissionTypes.SELF_REFERRAL: {
        DepartmentTypes.PSYCHIATRIC: base_structure(DepartmentTypes.PSYCHIATRIC, 'out'),
        DepartmentTypes.DERMATOLOGY: base_structure(DepartmentTypes.DERMATOLOGY, 'out'),
        DepartmentTypes.ORTHOPEDICS: base_structure(DepartmentTypes.ORTHOPEDICS, 'out'),
        DepartmentTypes.GASTROENTEROLOGY: base_structure(DepartmentTypes.GASTROENTEROLOGY, 'out'),
        DepartmentTypes.OPHTHALMOLOGY: base_structure(DepartmentTypes.OPHTHALMOLOGY, 'out'),
        DepartmentTypes.ENDOCRINOLOGY: base_structure(DepartmentTypes.ENDOCRINOLOGY, 'out'),
    },
    AdmissionTypes.ELECTIVE: {
        DepartmentTypes.MATERNITY: base_structure(DepartmentTypes.MATERNITY, 'all'),
    }
}
