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
        "cardiology": {
            "stay_types": ["inpatient", "day_patient"],
            "conditions": "cardiac"
        },
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

conditions = {
    "infectious_diseases": [
        "Common Cold",
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
    "musculoskeletal": [
        "Arthritis (Osteoarthritis, Rheumatoid Arthritis)",
        "Osteoporosis",
        "Low Back Pain",
        "Tendinitis",
        "Fibromyalgia",
        "Carpal Tunnel Syndrome",
        "Gout",
        "Lupus",
        "Scoliosis",
        "Fractures"
    ],
    "skin_conditions": [
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
        "Peyronie's Disease"
    ],
    "genetic_disorders": [
        "Down Syndrome",
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
    "oncological_conditions": [
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
    ]
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