new_admission_types = ["emergency", "gp_referral", "hospital_referral", "self_referral", "elective"]
sub_admission_types = [
    "maternity", "mental", "injury_rtc", "self_inflicted", "cancer",
    "neurology", "cardiology", "orthopedics", "pediatrics", "gastroenterology",
    "pulmonology", "nephrology", "endocrinology", "dermatology", "oncology",
    "ophthalmology", "otorhinolaryngology_ENT", "geriatrics", "obstetrics", "infectious_diseases"
]

admission_mapping = {
    "emergency": {
        "injury_rtc": {"inpatient", "day_patient"},
        "self_inflicted": {"inpatient"},
        "cardiology": {"inpatient", "day_patient"},
        "neurology": {"inpatient"},
        "pulmonology": {"inpatient", "day_patient"},
        "infectious_diseases": {"inpatient", "outpatient"}
    },
    "gp_referral": {
        "mental": {"outpatient", "inpatient"},
        "orthopedics": {"day_patient", "inpatient"},
        "gastroenterology": {"outpatient", "day_patient"},
        "endocrinology": {"outpatient"},
        "dermatology": {"outpatient"},
        "geriatrics": {"inpatient", "outpatient"}
    },
    "hospital_referral": {
        "nephrology": {"inpatient"},
        "cardiology": {"inpatient", "day_patient"},
        "neurology": {"inpatient"},
        "oncology": {"inpatient", "day_patient"},
        "otorhinolaryngology_ENT": {"inpatient", "day_patient"}
    },
    "self_referral": {
        "mental": {"outpatient"},
        "dermatology": {"outpatient"},
        "orthopedics": {"day_patient"},
        "gastroenterology": {"outpatient"},
        "endocrinology": {"outpatient"},
        "oncology": {"inpatient", "day_patient", "outpatient"}
    },
    "elective": {
        "maternity": {"inpatient", "day_patient"},
        "orthopedics": {"inpatient", "day_patient"},
        "obstetrics": {"inpatient"},
        "ophthalmology": {"day_patient", "outpatient"},
        "geriatrics": {"inpatient", "outpatient"}
    }
}


stay_type = ["outpatient", "inpatient", "day_patient"]

admission_tests = {
    "maternity": ["Ultrasound", "Blood tests", "Glucose tolerance test", "Amniocentesis"],
    "mental": ["Psychological evaluation", "Blood tests", "Brain imaging (MRI, CT scans)", "Electroencephalogram (EEG)"],
    "injury_rtc": ["X-rays", "CT scans", "MRI", "Ultrasound", "Blood tests"],
    "self_inflicted": ["Psychological assessment", "X-rays (for physical injuries)", "Blood tests", "Toxicology screening"],
    "cancer": ["Biopsy", "Blood tests", "MRI", "CT scans", "PET scans", "X-rays", "Ultrasound"],
    "neurology": ["MRI or CT scans of the brain", "Electroencephalogram (EEG)", "Lumbar puncture", "Nerve conduction studies", "Blood tests"],
    "cardiology": ["ECG", "Echocardiogram", "Stress tests", "Cardiac catheterization", "Blood tests"],
    "orthopedics": ["X-rays", "MRI", "CT scans", "Bone scans", "Blood tests"],
    "pediatrics": ["Blood tests", "Urine tests", "X-rays", "Ultrasound", "MRI", "Developmental screening tests"],
    "gastroenterology": ["Endoscopy", "Colonoscopy", "Blood tests", "Stool tests", "Abdominal ultrasound", "CT scan"],
    "pulmonology": ["Pulmonary function tests", "Chest X-ray", "CT scan", "Bronchoscopy"],
    "nephrology": ["Blood tests (renal function tests)", "Urine tests", "Ultrasound of the kidneys", "Biopsy"],
    "endocrinology": ["Blood tests (hormone levels)", "Thyroid function tests", "Bone density tests"],
    "dermatology": ["Skin biopsy", "Patch tests", "Skin scrapings", "Blood tests"],
    "oncology": ["Biopsies", "MRI", "Ultrasound", "Blood tests", "Imaging CT", "Imaging MRI", "Imaging PET scans", "X-rays", "Biopsy", "CT scans"],
    "ophthalmology": ["Eye exam", "Tonometry (eye pressure test)", "Retinal imaging", "Visual field test"],
    "otorhinolaryngology_ENT": ["Hearing tests", "Endoscopy of the ear/nose/throat", "Imaging CT", "Imaging MRI)"],
    "geriatrics": ["Comprehensive geriatric assessment", "Blood tests", "Bone density scans", "Cognitive tests"],
    "obstetrics": ["Ultrasound", "Blood tests", "Glucose tolerance test", "Amniocentesis", "Cervical screening"],
    "infectious_diseases": ["Blood cultures", "PCR tests", "Antibody tests", "chest X-ray", "Lumbar puncture"]
}