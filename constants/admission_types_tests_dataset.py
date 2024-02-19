from pprint import pprint

new_admission_types = ["emergency", "gp_referral", "hospital_referral", "self_referral", "elective"]
sub_admission_types = [
    "maternity", "mental", "injury_rtc", "self_inflicted", "cancer",
    "neurology", "cardiology", "orthopedics", "pediatrics", "gastroenterology",
    "pulmonology", "nephrology", "endocrinology", "dermatology", "oncology",
    "ophthalmology", "otorhinolaryngology_ENT", "geriatrics", "obstetrics", "infectious_diseases"
]

conditions = {
    "injury_rtc": [
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
    "infectious_diseases": [
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
    "cardiac": [
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
    "respiratory": [
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
    "digestive_system": [
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
    "endocrine_metabolic": [
        "Diabetes Mellitus",
        "Thyroid Disorders (Hypothyroidism, Hyperthyroidism)",
        "Osteoporosis",
        "Obesity",
        "Metabolic Syndrome",
        "Addison's Disease",
        "Cushing's Syndrome",
        "Gout",
        "Polycystic Ovary Syndrome (PCOS)",
        "Hyperlipidemia"
    ],
    "neurological": [
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
    "psychiatric": [
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
    "orthopedics": [
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
    "musculoskeletal": [
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
    "dermatology": [
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
    "hematologic": [
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
    "urological": [
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
    "eye_vision": [
        "Refractive Errors (Myopia, Hyperopia, Astigmatism)",
        "Cataracts",
        "Glaucoma",
        "Macular Degeneration",
        "Diabetic Retinopathy",
        "Conjunctivitis (Pink Eye)",
        "Dry Eye Syndrome",
        "Uveitis",
        "Retinal Detachment",
        "Keratitis"
    ],
    "ear_nose_throat": [
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
    "dental_oral": [
        "Dental Cavities",
        "Gingivitis",
        "Periodontitis",
        "Oral Herpes",
        "Oral Cancer",
        "Temporomandibular Joint Disorders (TMJ)",
        "Tooth Abscess",
        "Halitosis (Bad Breath)",
        "Oral Thrush",
        "Impacted Wisdom Teeth"
    ],
    "reproductive_female": [
        "Menstrual Disorders (Dysmenorrhea, Menorrhagia)",
        "Polycystic Ovary Syndrome (PCOS)",
        "Endometriosis",
        "Uterine Fibroids",
        "Ovarian Cysts",
        "Pelvic Inflammatory Disease (PID)",
        "Breast Cancer",
        "Cervical Cancer",
        "Vaginitis",
        "Menopause Symptoms"
    ],
    "reproductive_male": [
        "Erectile Dysfunction",
        "Prostatitis",
        "Benign Prostatic Hyperplasia (BPH)",
        "Prostate Cancer",
        "Testicular Cancer",
        "Hydrocele",
        "Varicocele",
        "Infertility",
        "Orchitis",
        "Peyronie''s Disease"
    ],
    "genetic_disorders": [
        "Cystic Fibrosis",
        "Sickle Cell Disease",
        "Hemophilia",
        "Huntington's Disease",
        "Duchenne Muscular Dystrophy",
        "Thalassemia",
        "Fragile X Syndrome",
        "Turner Syndrome",
        "Marfan Syndrome"
    ],
    "autoimmune_diseases": [
        "Rheumatoid Arthritis",
        "Lupus",
        "Type 1 Diabetes",
        "Multiple Sclerosis",
        "Psoriasis",
        "Inflammatory Bowel Disease (IBD)",
        "Hashimoto's Thyroiditis",
        "Graves' Disease",
        "Celiac Disease",
        "Sjögren's Syndrome"
    ],
    "oncology": [
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
    "allergies_immune_disorders": [
        "Allergic Rhinitis (Hay Fever)",
        "Food Allergies",
        "Drug Allergies",
        "Asthma",
        "Eczema (Atopic Dermatitis)",
        "Anaphylaxis",
        "Autoimmune Diseases",
        "Immunodeficiency Disorders",
        "Contact Dermatitis",
        "Latex Allergy"
    ],
    "ophthalmology": [
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
    "maternity": [
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
    "obstetrics": [
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
    "gastroenterology": [
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
    "endocrinology": [
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
}

admission_mapping = {
    "emergency": {
        "injury_rtc": {
            "stay_types": ["inpatient", "day_patient"],
            "conditions": conditions["injury_rtc"]
        },
        "self_inflicted": {"inpatient"},
        "cardiology": {
            "stay_types": ["inpatient", "day_patient"],
            "conditions": conditions["cardiac"]
        },
        "neurology": {
            "stay_types": ["inpatient", "day_patient"],
            "conditions": conditions["neurological"]
        },
        "gastroenterology": {
            "stay_types": ["inpatient", "day_patient", "outpatient"],
            "conditions": conditions["gastroenterology"]
        },
        "respiratory": {
            "stay_types": ["inpatient", "day_patient"],
            "conditions": conditions["respiratory"]
        },
        "infectious_diseases": {
            "stay_types": ["inpatient", "day_patient"],
            "conditions": conditions["infectious_diseases"]
        },
        "maternity": {
            "stay_types": ["inpatient", "day_patient", "outpatient"],
            "conditions": conditions["maternity"]
        },
    },
    "gp_referral": {
        "psychiatric": {
            "stay_types": ["inpatient", "day_patient"],
            "conditions": conditions["psychiatric"]
        },
        "orthopedics": {
            "stay_types": ["inpatient", "day_patient"],
            "conditions": conditions["orthopedics"]
        },
        "gastroenterology": {
            "stay_types": ["inpatient", "day_patient"],
            "conditions": conditions["gastroenterology"]
        },
        "endocrinology": {
            "stay_types": ["outpatient"],
            "conditions": conditions["dermatology"]
        },
        "dermatology": {
            "stay_types": ["outpatient"],
            "conditions": conditions["dermatology"]
        },
        "maternity": {
            "stay_types": ["inpatient", "day_patient", "outpatient"],
            "conditions": conditions["maternity"]
        },
        "geriatrics": {"inpatient", "outpatient"}
    },
    "hospital_referral": {
        "nephrology": {"inpatient"},
        "cardiology": {
            "stay_types": ["inpatient", "day_patient"],
            "conditions": conditions["cardiac"]
        },
        "neurology": {
            "stay_types": ["inpatient", "day_patient"],
            "conditions": conditions["neurological"]
        },
        "oncology": {
            "stay_types": ["inpatient", "day_patient", "outpatient"],
            "conditions": conditions["oncology"]
        },
        "otorhinolaryngology_ENT": {
            "stay_type": ["inpatient", "day_patient"],
            "condition": conditions["ear_nose_throat"]
        }
    },
    "self_referral": {
        "psychiatric": {
            "stay_types": ["outpatient"],
            "conditions": conditions["psychiatric"]
        },
        "dermatology": {
            "stay_types": ["outpatient"],
            "conditions": conditions["dermatology"]
        },
        "orthopedics": {
            "stay_types": ["inpatient", "day_patient"],
            "conditions": conditions["orthopedics"]
        },
        "gastroenterology": {
            "stay_types": ["outpatient"],
            "conditions": conditions["gastroenterology"]
        },
        "endocrinology": {"outpatient"},
        "oncology": {
            "stay_types": ["inpatient", "day_patient", "outpatient"],
            "conditions": conditions["oncology"]
        },
    },
    "elective": {
        "maternity": {
            "stay_types": ["inpatient", "day_patient", "outpatient"],
            "conditions": conditions["maternity"]
        },
        "orthopedics": {
            "stay_types": ["inpatient", "day_patient"],
            "conditions": conditions["orthopedics"]
        },
        "obstetrics": {
            "stay_types": ["inpatient", "day_patient", "outpatient"],
            "conditions": conditions["obstetrics"]
        },
        "ophthalmology": {
            "stay_types": ["inpatient", "day_patient"],
            "conditions": conditions["ophthalmology"]
        },
        "geriatrics": {"inpatient", "outpatient"}
    }
}

stay_type = ["outpatient", "inpatient", "day_patient"]

admission_tests = {
    "maternity": ["Ultrasound", "Blood tests", "Glucose tolerance test", "Amniocentesis"],
    "mental": ["Psychological evaluation", "Blood tests", "Brain imaging (MRI, CT scans)",
               "Electroencephalogram (EEG)"],
    "injury_rtc": ["X-rays", "CT scans", "MRI", "Ultrasound", "Blood tests"],
    "self_inflicted": ["Psychological assessment", "X-rays (for physical injuries)", "Blood tests",
                       "Toxicology screening"],
    "neurology": ["MRI or CT scans of the brain", "Electroencephalogram (EEG)", "Lumbar puncture",
                  "Nerve conduction studies", "Blood tests"],
    "cardiology": ["ECG", "Echocardiogram", "Stress tests", "Cardiac catheterization", "Blood tests"],
    "orthopedics": ["X-rays", "MRI", "CT scans", "Bone scans", "Blood tests"],
    "pediatrics": ["Blood tests", "Urine tests", "X-rays", "Ultrasound", "MRI", "Developmental screening tests"],
    "gastroenterology": ["Endoscopy", "Colonoscopy", "Blood tests", "Stool tests", "Abdominal ultrasound",
                         "CT scan"],
    "pulmonology": ["Pulmonary function tests", "Chest X-ray", "CT scan", "Bronchoscopy"],
    "nephrology": ["Blood tests (renal function tests)", "Urine tests", "Ultrasound of the kidneys", "Biopsy"],
    "endocrinology": ["Blood tests (hormone levels)", "Thyroid function tests", "Bone density tests"],
    "dermatology": ["Skin biopsy", "Patch tests", "Skin scrapings", "Blood tests"],
    "oncology": ["Biopsies", "MRI", "Ultrasound", "Blood tests", "Imaging CT", "Imaging MRI", "Imaging PET scans",
                 "X-rays", "Biopsy", "CT scans"],
    "ophthalmology": ["Eye exam", "Tonometry (eye pressure test)", "Retinal imaging", "Visual field test"],
    "otorhinolaryngology_ENT": ["Hearing tests", "Endoscopy of the ear/nose/throat", "Imaging CT", "Imaging MRI)"],
    "geriatrics": ["Comprehensive geriatric assessment", "Blood tests", "Bone density scans", "Cognitive tests"],
    "obstetrics": ["Ultrasound", "Blood tests", "Glucose tolerance test", "Amniocentesis", "Cervical screening"],
    "infectious_diseases": ["Blood cultures", "PCR tests", "Antibody tests", "chest X-ray", "Lumbar puncture"],
    "hematology": ["Full Blood Count (FBC)", "Coagulation Profile", "Bone Marrow Biopsy",
                            "Haemoglobin Electrophoresis", "Erythrocyte Sedimentation Rate (ESR)", "Serum Ferritin",
                            "Blood Film", "Immunophenotyping", "Cytogenetic Testing", "Molecular Genetic Tests"],
    "musculoskeletal": ["X-rays", "MRI Scan", "CT Scan", "Bone Scan",
                                 "Dual-energy X-ray Absorptiometry (DEXA) Scan", "Electromyography (EMG)",
                                 "Nerve Conduction Studies", "Ultrasound", "Arthroscopy",
                                 "Blood Tests for Rheumatoid Factor & Anti-CCP"],
    "urology": ["Urinalysis", "Blood Tests for Kidney Function", "Ultrasound of the Kidneys and Bladder",
                         "Cystoscopy", "Urodynamic Testing", "Prostate-Specific Antigen (PSA) Test", "CT Urogram",
                         "MRI of the Pelvis", "Intravenous Pyelogram (IVP)", "Renal Biopsy"]
}

