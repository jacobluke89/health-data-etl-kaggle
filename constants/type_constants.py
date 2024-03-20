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
    ELECTIVE = auto()
    EMERGENCY = auto()
    GP_REFERRAL = auto()
    HOSPITAL_REFERRAL = auto()
    SELF_REFERRAL = auto()


class SubAdmissionTypes(Enum):
    CANCER = auto()
    CARDIOLOGY = auto()
    DERMATOLOGY = auto()
    ENDOCRINOLOGY = auto()
    GASTROENTEROLOGY = auto()
    GASTROINTESTINAL_DISORDERS = auto()
    GERIATRICS = auto()
    HEMATOLOGY = auto()
    INFECTIOUS_DISEASES = auto()
    INJURY_RTC = auto()
    MATERNITY = auto()
    MUSCULOSKELETAL = auto()
    NEPHROLOGY = auto()
    NEUROLOGY = auto()
    OBSTETRICS = auto()
    ONCOLOGY = auto()
    OPHTHALMOLOGY = auto()
    ORTHOPEDICS = auto()
    OTORHINOLARYNGOLOGY_ENT = auto()
    PEDIATRICS = auto()
    PSYCHIATRIC = auto()
    RESPIRATORY = auto()
    SELF_INFLICTED = auto()
    UROLOGY = auto()


class ConditionsOrDiagnosis(Enum):
    CANCER = [
        "Breast Cancer",
        "Lung Cancer",
        "Colorectal Cancer",
        "Prostate Cancer",
        "Stomach (Gastric) Cancer",
        "Liver Cancer",
        "Cervical Cancer",
        "Thyroid Cancer",
        "Bladder Cancer",
        "Non-Hodgkin Lymphoma",
        "Kidney (Renal) Cancer",
        "Pancreatic Cancer",
        "Leukemia",
        "Ovarian Cancer",
        "Esophageal Cancer",
        "Melanoma of Skin",
        "Brain and Nervous System Cancers",
        "Endometrial (Uterine) Cancer",
        "Head and Neck Cancers",
        "Testicular Cancer"
    ]
    CARDIOLOGY = [
        "Hypertension (High Blood Pressure)",
        "Coronary Artery Disease",
        "Heart Attack",
        "Heart Failure",
        "Arrhythmias",
        "Peripheral Artery Disease",
        "Stroke",
        "Aneurysms",
        "Venous Thromboembolism"
    ]
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
    ]
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
    ]
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
    ]
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
    ]
    GERIATRICS = []
    HEMATOLOGY = [
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    NEUROLOGY = [
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]

    SELF_INFLICTED = [
        "Lacerations or cuts",
        "Overdose",
        "Burning",
        "Self-hitting",
        "Piercing the skin",
        "Head banging",
        "Bone breaking",
        "Hair pulling (Trichotillomania)",
        "Skin picking (Dermatillomania)",
        "Ingesting harmful substances"
    ]
    UROLOGY = []


class ConditionTests(Enum):
    MATERNITY = ["Ultrasound", "Blood tests", "Glucose tolerance test", "Amniocentesis"]
    PSYCHIATRIC = ["Psychological evaluation", "Blood tests", "Brain imaging (MRI, CT scans)",
                   "Electroencephalogram (EEG)"]
    INJURY_RTC = ["X-rays", "CT scans", "MRI", "Ultrasound", "Blood tests"]
    SELF_INFLICTED = ["Psychological assessment", "X-rays (for physical injuries)", "Blood tests",
                      "Toxicology screening"]
    CANCER = [
        "Imaging Tests - Mammography",
        "Imaging Tests - Low-dose computed tomography (LDCT)",
        "Imaging Tests - Ultrasound",
        "Imaging Tests - MRI",
        "Laboratory Tests - Blood Tests",
        "Laboratory Tests - Urine Tests",
        "Laboratory Tests - Stool Tests",
        "Tissue Biopsy",
        "Endoscopic Examinations - Colonoscopy and Sigmoidoscopy",
        "Endoscopic Examinations - Upper Endoscopy",
        "Genetic Tests",
        "Pap Smear and HPV Testing",
        "Dermatological Examinations",
        "Barium Enema",
        "Bone Scans",
        "Digital Rectal Exam (DRE)"
    ]
    NEUROLOGY = ["MRI or CT scans of the brain", "Electroencephalogram (EEG)", "Lumbar puncture",
                 "Nerve conduction studies", "Blood tests"]
    CARDIOLOGY = ["ECG", "Echocardiogram", "Stress tests", "Cardiac catheterization", "Blood tests"]
    ORTHOPEDICS = ["X-rays", "MRI", "CT scans", "Bone scans", "Blood tests"]
    PEDIATRICS = ["Blood tests", "Urine tests", "X-rays", "Ultrasound", "MRI", "Developmental screening tests"]
    GASTROENTEROLOGY = ["Endoscopy", "Colonoscopy", "Blood tests", "Stool tests", "Abdominal ultrasound", "CT scan"]
    RESPIRATORY = ["Pulmonary function tests", "Chest X-ray", "CT scan", "Bronchoscopy"]
    NEPHROLOGY = ["Blood tests (renal function tests)", "Urine tests", "Ultrasound of the kidneys", "Biopsy"]
    ENDOCRINOLOGY = ["Blood tests (hormone levels)", "Thyroid function tests", "Bone density tests"]
    DERMATOLOGY = ["Skin biopsy", "Patch tests", "Skin scrapings", "Blood tests"]
    ONCOLOGY = ["Biopsies", "MRI", "Ultrasound", "Blood tests", "Imaging CT", "Imaging MRI", "Imaging PET scans",
                "X-rays", "Biopsy", "CT scans"]
    OPHTHALMOLOGY = ["Eye exam", "Tonometry (eye pressure test)", "Retinal imaging", "Visual field test"]
    OTORHINOLARYNGOLOGY_ENT = ["Hearing tests", "Endoscopy of the ear/nose/throat", "Imaging CT", "Imaging MRI"]
    GERIATRICS = ["Comprehensive geriatric assessment", "Blood tests", "Bone density scans", "Cognitive tests"]
    OBSTETRICS = ["Ultrasound", "Blood tests", "Glucose tolerance test", "Amniocentesis", "Cervical screening"]
    INFECTIOUS_DISEASES = ["Blood cultures", "PCR tests", "Antibody tests", "chest X-ray", "Lumbar puncture"]
    HEMATOLOGY = ["Full Blood Count (FBC)", "Coagulation Profile", "Bone Marrow Biopsy", "Haemoglobin Electrophoresis",
                  "Erythrocyte Sedimentation Rate (ESR)", "Serum Ferritin", "Blood Film", "Immunophenotyping",
                  "Cytogenetic Testing", "Molecular Genetic Tests"]
    MUSCULOSKELETAL = ["X-rays", "MRI Scan", "CT Scan", "Bone Scan", "Dual-energy X-ray Absorptiometry (DEXA) Scan",
                       "Electromyography (EMG)", "Nerve Conduction Studies", "Ultrasound", "Arthroscopy",
                       "Blood Tests for Rheumatoid Factor & Anti-CCP"]
    UROLOGY = ["Urinalysis", "Blood Tests for Kidney Function", "Ultrasound of the Kidneys and Bladder", "Cystoscopy",
               "Urodynamic Testing", "Prostate-Specific Antigen (PSA) Test", "CT Urogram", "MRI of the Pelvis",
               "Intravenous Pyelogram (IVP)", "Renal Biopsy"]


non_elective_conditions = [
    'Acute Hemorrhagic Stroke',
    'Acute Kidney Injury (AKI)',
    'Acute Liver Failure',
    'Acute Myocardial Infarction',
    'Acute Pancreatitis',
    'Acute Respiratory Distress Syndrome (ARDS)',
    'Anaphylaxis',
    'Appendicitis',
    'Asthma',
    'COPD Exacerbation',
    'Chronic Obstructive Pulmonary Disease (COPD)',
    'Concussion',
    'Deep Vein Thrombosis (DVT)',
    'Diabetic Ketoacidosis',
    'Ectopic Pregnancy',
    'Fractures',
    'Glomerulonephritis',
    'Heart Attack',
    'Intestinal Obstruction',
    'Meningitis',
    'Pneumonia',
    'Pre-eclampsia/Eclampsia',
    'Pulmonary Embolism',
    'Ruptured Aortic Aneurysm',
    'Septicemia',
    'Severe Asthma Attack',
    'Severe Burns',
    'Severe Sepsis or Septic Shock',
    'Severe or Complicated UTIs',
    'Sickle Cell Crisis',
    'Stroke',
    'Traumatic Brain Injuries (TBIs)',
    'Urinary Tract Infections (UTIs)'
]
