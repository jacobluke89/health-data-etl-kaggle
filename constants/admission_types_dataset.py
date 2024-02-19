from enum import Enum, auto


class StayTypeCombinations(Enum):
    INPATIENT = ("Inpatient",)
    DAY_PATIENT = ("Day Patient",)
    OUTPATIENT = ("Outpatient",)
    INPATIENT_DAY_PATIENT = ("Inpatient", "Day Patient")
    INPATIENT_OUTPATIENT = ("Inpatient", "Outpatient")
    DAY_PATIENT_OUTPATIENT = ("Day Patient", "Outpatient")
    ALL_TYPES = ("Inpatient", "Day Patient", "Outpatient")

class AdmissionTypes(Enum):
    EMERGENCY = auto()
    GP_REFERRAL = auto()
    HOSPITAL_REFERRAL = auto()
    SELF_REFERRAL = auto()
    ELECTIVE = auto()

class SubAdmissionTypes(Enum):
    MATERNITY = auto()
    PSYCHIATRIC = auto()
    INJURY_RTC = auto()
    SELF_INFLICTED = auto()
    CANCER = auto()
    NEUROLOGY = auto()
    CARDIOLOGY = auto()
    ORTHOPEDICS = auto()
    PEDIATRICS = auto()
    GASTROENTEROLOGY = auto()
    HEMATOLOGY = auto()
    GASTROINTESTINAL_DISORDERS = auto()
    MUSCULOSKELETAL = auto()
    RESPIRATORY = auto()
    NEPHROLOGY = auto()
    ENDOCRINOLOGY = auto()
    DERMATOLOGY = auto()
    ONCOLOGY = auto()
    OPHTHALMOLOGY = auto()
    UROLOGY = auto()
    OTORHINOLARYNGOLOGY_ENT = auto()
    GERIATRICS = auto()
    OBSTETRICS = auto()
    INFECTIOUS_DISEASES = auto()


class Conditions(Enum):
    INJURY_RTC = [
        "Whiplash",
        "Concussions",
        "Contusions (bruises)",
        "Lacerations",
        "Abrasions",
        "Fractures",
        "Sprains",
        "Strains",
        "Dislocations",
        "Rib Fractures",
        "Internal Bleeding",
        "Pneumothorax (collapsed lung)",
        "Spinal Cord Injuries",
        "Traumatic Brain Injuries (TBIs)",
        "Crush Injuries",
        "Amputations",
        "Psychological Trauma",
        "Burn Injuries",
        "Skull Fractures",
        "Pelvic Fractures",
        "Facial Fractures",
        "Hematomas",
        "Organ Damage",
        "Cervical Spine Injuries",
        "Thoracic Spine Injuries",
        "Lumbar Spine Injuries",
        "Tendon Injuries",
        "Nerve Damage",
        "Eye Injuries",
        "Dental Injuries",
        "Post-Traumatic Arthritis",
        "Compartment Syndrome",
        "Soft Tissue Injuries",
        "Seat Belt Injuries",
        "Airbag Injuries",
        "Lower Extremity Injuries",
        "Upper Extremity Injuries",
        "Drowning or Near-Drowning Incidents",
        "Hypothermia or Frostbite",
        "Heatstroke",
        "Acoustic Trauma",
        "Stress Fractures",
        "Bursitis"
    ],
    INFECTIOUS_DISEASES = [
        "Influenza",
        "Urinary Tract Infections (UTIs)",
        "HIV/AIDS",
        "Hepatitis",
        "Tuberculosis",
        "Malaria",
        "COVID-19",
        "Strep Throat",
        "Herpes Simplex Virus"
    ],
    CARDIAC = [
        "Hypertension (High Blood Pressure)",
        "Coronary Artery Disease",
        "Heart Attack",
        "Heart Failure",
        "Arrhythmias",
        "Peripheral Artery Disease",
        "Stroke",
        "Aneurysms",
        "Venous Thromboembolism"
    ],
    RESPIRATORY = [
        "Asthma",
        "Chronic Obstructive Pulmonary Disease (COPD)",
        "Pneumonia",
        "Bronchitis",
        "Sinusitis",
        "Allergic Rhinitis",
        "Pulmonary Embolism",
        "Lung Cancer",
        "Cystic Fibrosis",
        "Sleep Apnea"
    ],
    GASTROINTESTINAL_DISORDERS = [
        "Gastroesophageal Reflux Disease (GERD)",
        "Peptic Ulcer Disease",
        "Irritable Bowel Syndrome (IBS)",
        "Crohn's Disease",
        "Ulcerative Colitis",
        "Gallstones",
        "Hepatitis",
        "Cirrhosis",
        "Pancreatitis",
        "Celiac Disease"
    ],
    NEUROLOGICAL = [
        "Migraines",
        "Epilepsy",
        "Parkinson's Disease",
        "Alzheimer's Disease",
        "Multiple Sclerosis",
        "Stroke",
        "Peripheral Neuropathy",
        "Bell's Palsy",
        "Sciatica",
        "Concussion"
    ],
    PSYCHIATRIC = [
        "Depression",
        "Anxiety Disorders",
        "Bipolar Disorder",
        "Schizophrenia",
        "Post-Traumatic Stress Disorder (PTSD)",
        "Obsessive-Compulsive Disorder (OCD)",
        "Eating Disorders (Anorexia, Bulimia)",
        "Attention Deficit Hyperactivity Disorder (ADHD)",
        "Autism Spectrum Disorder",
        "Insomnia"
    ],
    ORTHOPEDICS = [
        "Osteoarthritis",
        "Rheumatoid Arthritis",
        "Osteoporosis",
        "Fractures",
        "Anterior Cruciate Ligament (ACL) Injuries",
        "Meniscus Tears",
        "Rotator Cuff Tears",
        "Carpal Tunnel Syndrome",
        "Spinal Disc Herniation",
        "Scoliosis"
    ],
    MUSCULOSKELETAL = [
        "Low Back Pain",
        "Tendinitis",
        "Bursitis",
        "Fibromyalgia",
        "Gout",
        "Ankylosing Spondylitis",
        "Plantar Fasciitis",
        "Repetitive Strain Injury (RSI)",
        "Lupus",
        "Polymyalgia Rheumatica"
    ],
    DERMATOLOGY = [
        "Acne",
        "Eczema",
        "Psoriasis",
        "Dermatitis",
        "Skin Cancer",
        "Rosacea",
        "Hives (Urticaria)",
        "Impetigo",
        "Cellulitis",
        "Shingles (Herpes Zoster)"
    ],
    HEMATOLOGIC = [
        "Anemia",
        "Hemophilia",
        "Leukemia",
        "Lymphoma",
        "Sickle Cell Disease",
        "Deep Vein Thrombosis (DVT)",
        "Iron Deficiency Anemia",
        "Thrombocytopenia",
        "Hemochromatosis",
        "Polycythemia Vera"
    ],
    UROLOGICAL = [
        "Urinary Tract Infections (UTIs)",
        "Kidney Stones",
        "Erectile Dysfunction",
        "Prostate Enlargement (Benign Prostatic Hyperplasia)",
        "Bladder Infections",
        "Chronic Kidney Disease",
        "Urinary Incontinence",
        "Prostatitis",
        "Overactive Bladder",
        "Kidney Failure"
    ],
    OTORHINOLARYNGOLOGY_ENT = [
        "Otitis Media (Middle Ear Infection)",
        "Otitis Externa (Swimmer's Ear)",
        "Sinusitis",
        "Tonsillitis",
        "Laryngitis",
        "Meniere's Disease",
        "Tinnitus",
        "Hearing Loss",
        "Pharyngitis",
        "Rhinitis"
    ],
    ONCOLOGY = [
        "Breast Cancer",
        "Lung Cancer",
        "Prostate Cancer",
        "Colorectal Cancer",
        "Melanoma",
        "Leukemia",
        "Lymphoma",
        "Pancreatic Cancer",
        "Ovarian Cancer",
        "Bladder Cancer"
    ],
    OPHTHALMOLOGY = [
     "Refractive Errors",
     "Cataracts",
     "Glaucoma",
     "Age-related Macular Degeneration (AMD)",
     "Diabetic Retinopathy",
     "Dry Eye Syndrome",
     "Conjunctivitis",
     "Retinal Detachment",
     "Uveitis",
     "Keratitis"
    ],
    MATERNITY = [
        "Labour and Delivery",
        "Scheduled Caesarean Section",
        "Induction of Labour",
        "Preterm Labour",
        "Pre-eclampsia/Eclampsia",
        "Gestational Diabetes Monitoring",
        "Antepartum Haemorrhage",
        "Pregnancy-induced Hypertension",
        "Ruptured Membranes without Contractions",
        "Postpartum Complications"
    ],
    OBSTETRICS = [
        "Menstrual Disorders",
        "Polycystic Ovary Syndrome (PCOS)",
        "Premature Ovarian Insufficiency (POI)",
        "Endometriosis",
        "Congenital Reproductive Anomalies",
        "Turner Syndrome",
        "Gynecological Tumors",
        "Breast Disorders",
        "Vulvovaginitis",
        "Precocious Puberty"
    ],
    GASTROENTEROLOGY = [
        "Gastro-oesophageal Reflux Disease (GORD)",
        "Irritable Bowel Syndrome (IBS)",
        "Inflammatory Bowel Disease (IBD) - including Crohn's Disease and Ulcerative Colitis",
        "Coeliac Disease",
        "Peptic Ulcers",
        "Gallstones",
        "Chronic Liver Disease - including Hepatitis and Cirrhosis",
        "Pancreatitis",
        "Gastroenteritis",
        "Diverticular Disease"
    ],
    ENDOCRINOLOGY = [
        "Diabetes Mellitus - Type 1 and Type 2",
        "Thyroid Disorders - including Hypothyroidism and Hyperthyroidism",
        "Addison's Disease",
        "Cushing's Syndrome",
        "Polycystic Ovary Syndrome (PCOS)",
        "Osteoporosis",
        "Pituitary Disorders",
        "Hyperlipidaemia",
        "Gout",
        "Metabolic Syndrome"
    ],
    NEPHROLOGY = [
        "Chronic Kidney Disease (CKD)",
        "Acute Kidney Injury (AKI)",
        "Glomerulonephritis",
        "Polycystic Kidney Disease",
        "Kidney Stones",
        "Urinary Tract Infections (UTIs)",
        "Nephrotic Syndrome",
        "Renal Artery Stenosis",
        "Haemodialysis-related Amyloidosis",
        "Hyperkalaemia"
    ]



STAY_TYPES = "stay_types"
CONDITIONS_CONST = "conditions"

admission_mapping = {
    AdmissionTypes.EMERGENCY: {
        SubAdmissionTypes.INJURY_RTC: {
            STAY_TYPES: StayTypeCombinations.INPATIENT_DAY_PATIENT.value,
            CONDITIONS_CONST: Conditions.INJURY_RTC.value
        },
        SubAdmissionTypes.SELF_INFLICTED: {
            STAY_TYPES: StayTypeCombinations.INPATIENT.value
        },
        SubAdmissionTypes.CARDIOLOGY: {
            STAY_TYPES: StayTypeCombinations.INPATIENT_DAY_PATIENT.value,
            CONDITIONS_CONST: Conditions.CARDIAC.value
        },
        SubAdmissionTypes.NEUROLOGY: {
           STAY_TYPES: StayTypeCombinations.ALL_TYPES.value,
           CONDITIONS_CONST: Conditions.NEUROLOGICAL.value
        },
        SubAdmissionTypes.GASTROENTEROLOGY: {
            STAY_TYPES: StayTypeCombinations.ALL_TYPES.value,
            CONDITIONS_CONST: Conditions.GASTROENTEROLOGY.value
        },
        SubAdmissionTypes.RESPIRATORY: {
            STAY_TYPES: StayTypeCombinations.ALL_TYPES.value,
            CONDITIONS_CONST: Conditions.RESPIRATORY.value
        },
        SubAdmissionTypes.INFECTIOUS_DISEASES: {
            STAY_TYPES: StayTypeCombinations.INPATIENT_DAY_PATIENT.value,
            CONDITIONS_CONST: Conditions.INFECTIOUS_DISEASES.value
        },
        SubAdmissionTypes.MATERNITY: {
            STAY_TYPES: StayTypeCombinations.ALL_TYPES.value,
            CONDITIONS_CONST: Conditions.MATERNITY.value
        },
        SubAdmissionTypes.PSYCHIATRIC: {
            STAY_TYPES: StayTypeCombinations.ALL_TYPES.value,
            CONDITIONS_CONST: Conditions.PSYCHIATRIC.value
        },
        SubAdmissionTypes.ORTHOPEDICS: {
            STAY_TYPES: StayTypeCombinations.ALL_TYPES.value,
            CONDITIONS_CONST: Conditions.ORTHOPEDICS.value
        }
    },
    AdmissionTypes.GP_REFERRAL: {
        SubAdmissionTypes.PSYCHIATRIC: {
            STAY_TYPES: StayTypeCombinations.ALL_TYPES.value,
            CONDITIONS_CONST: Conditions.PSYCHIATRIC.value
        },
        SubAdmissionTypes.ORTHOPEDICS: {
            STAY_TYPES: StayTypeCombinations.OUTPATIENT.value,
            CONDITIONS_CONST: Conditions.ORTHOPEDICS.value
        },
        SubAdmissionTypes.GASTROENTEROLOGY: {
            STAY_TYPES: StayTypeCombinations.ALL_TYPES.value,
            CONDITIONS_CONST: Conditions.GASTROENTEROLOGY.value
        },
        SubAdmissionTypes.ENDOCRINOLOGY: {
            STAY_TYPES: StayTypeCombinations.OUTPATIENT.value,
            CONDITIONS_CONST: Conditions.ENDOCRINOLOGY.value
        },
        SubAdmissionTypes.DERMATOLOGY: {
            STAY_TYPES: StayTypeCombinations.OUTPATIENT.value,
            CONDITIONS_CONST: Conditions.DERMATOLOGY.value
        },
        SubAdmissionTypes.MATERNITY: {
            STAY_TYPES: StayTypeCombinations.ALL_TYPES.value,
            CONDITIONS_CONST: Conditions.MATERNITY.value
        },
        SubAdmissionTypes.GERIATRICS: {
            STAY_TYPES: StayTypeCombinations.INPATIENT_OUTPATIENT.value
        }
    },
    AdmissionTypes.HOSPITAL_REFERRAL: {
        SubAdmissionTypes.CARDIOLOGY: {
            STAY_TYPES: StayTypeCombinations.INPATIENT_DAY_PATIENT.value,
            CONDITIONS_CONST: Conditions.CARDIAC.value
        },
        SubAdmissionTypes.NEPHROLOGY: {
            STAY_TYPES: StayTypeCombinations.ALL_TYPES.value, 
            CONDITIONS_CONST: Conditions.NEPHROLOGY.value
        },
        SubAdmissionTypes.NEUROLOGY: {
            STAY_TYPES: StayTypeCombinations.ALL_TYPES.value,
            CONDITIONS_CONST: Conditions.NEUROLOGICAL.value
        },
        SubAdmissionTypes.ONCOLOGY: {
            STAY_TYPES: StayTypeCombinations.ALL_TYPES.value,
            CONDITIONS_CONST: Conditions.ONCOLOGY.value
        },
        SubAdmissionTypes.HEMATOLOGY: {
            STAY_TYPES: StayTypeCombinations.ALL_TYPES.value,
            CONDITIONS_CONST: Conditions.HEMATOLOGIC.value
        },
        SubAdmissionTypes.UROLOGY: {
            STAY_TYPES: StayTypeCombinations.ALL_TYPES.value,
            CONDITIONS_CONST: Conditions.UROLOGICAL.value
        },
        SubAdmissionTypes.GASTROINTESTINAL_DISORDERS: {
            STAY_TYPES: StayTypeCombinations.ALL_TYPES.value,
            CONDITIONS_CONST: Conditions.GASTROINTESTINAL_DISORDERS.value
        },
        SubAdmissionTypes.RESPIRATORY: {
            STAY_TYPES: StayTypeCombinations.ALL_TYPES.value,
            CONDITIONS_CONST: Conditions.RESPIRATORY.value
        },
        SubAdmissionTypes.MUSCULOSKELETAL: {
            STAY_TYPES: StayTypeCombinations.ALL_TYPES.value,
            CONDITIONS_CONST: Conditions.MUSCULOSKELETAL.value
        },
        SubAdmissionTypes.OTORHINOLARYNGOLOGY_ENT: {
            STAY_TYPES: StayTypeCombinations.ALL_TYPES.value,
            CONDITIONS_CONST: Conditions.OTORHINOLARYNGOLOGY_ENT.value
        }
    },
    AdmissionTypes.SELF_REFERRAL: {
        SubAdmissionTypes.PSYCHIATRIC: {
            STAY_TYPES: StayTypeCombinations.OUTPATIENT.value,
            CONDITIONS_CONST: Conditions.PSYCHIATRIC.value
        },
        SubAdmissionTypes.DERMATOLOGY: {
            STAY_TYPES: StayTypeCombinations.OUTPATIENT.value,
            CONDITIONS_CONST: Conditions.DERMATOLOGY.value
        },
        SubAdmissionTypes.ORTHOPEDICS: {
            STAY_TYPES: StayTypeCombinations.OUTPATIENT.value,
            CONDITIONS_CONST: Conditions.ORTHOPEDICS.value
        },
        SubAdmissionTypes.GASTROENTEROLOGY: {
            STAY_TYPES: StayTypeCombinations.OUTPATIENT.value,
            CONDITIONS_CONST: Conditions.GASTROENTEROLOGY.value
        },
        SubAdmissionTypes.OPHTHALMOLOGY: {
            STAY_TYPES: StayTypeCombinations.OUTPATIENT.value,
            CONDITIONS_CONST: Conditions.OPHTHALMOLOGY.value
        },
        SubAdmissionTypes.ENDOCRINOLOGY: {
            STAY_TYPES: StayTypeCombinations.OUTPATIENT.value,
            CONDITIONS_CONST: Conditions.ENDOCRINOLOGY.value
        },
    },
    AdmissionTypes.ELECTIVE: {
        SubAdmissionTypes.MATERNITY: {
            STAY_TYPES: StayTypeCombinations.ALL_TYPES.value,
            CONDITIONS_CONST: Conditions.MATERNITY.value
        },
    }
}
