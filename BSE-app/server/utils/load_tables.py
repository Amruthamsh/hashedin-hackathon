import pandas as pd
from pathlib import Path

def load_tsv(path: Path) -> pd.DataFrame:
    """Load a GDC TSV, dropping the redundant second header row GDC inserts."""
    df = pd.read_csv(path, sep="\t", low_memory=False)
    # GDC adds a second row with column descriptions — drop it
    if df.iloc[0].astype(str).str.startswith("The").any():
        df = df.iloc[1:].reset_index(drop=True)
    return df
 
 
def load_clinical(CLINICAL_DIR: Path) -> pd.DataFrame:
    """Primary patient table: demographics, vital status, days_to_death."""
    path = CLINICAL_DIR / "clinical.tsv"
    df = load_tsv(path)

    keep = [
        # identifiers
        "cases.case_id", "cases.submitter_id",
        
        # demographics
        "demographic.age_at_index", "demographic.gender",
        "demographic.race", "demographic.ethnicity",
        "demographic.vital_status", "demographic.days_to_death",
        "demographic.days_to_birth",
        
        # diagnosis / staging
        "diagnoses.ajcc_pathologic_stage",
        "diagnoses.ajcc_pathologic_t",
        "diagnoses.ajcc_pathologic_n",
        "diagnoses.ajcc_pathologic_m",
        "diagnoses.age_at_diagnosis",
        "diagnoses.days_to_diagnosis",
        "diagnoses.days_to_last_follow_up",
        "diagnoses.days_to_recurrence",        # ← key outcome
        "diagnoses.progression_or_recurrence", # ← key outcome
        "diagnoses.last_known_disease_status",
        "diagnoses.primary_diagnosis",
        "diagnoses.morphology",
        "diagnoses.tumor_grade",
        "diagnoses.prior_malignancy",
        "diagnoses.prior_treatment",
        "diagnoses.residual_disease",
        "diagnoses.tumor_focality",
        "diagnoses.laterality",
        "diagnoses.method_of_diagnosis",
        
        # treatment response — this is your primary outcome variable
        "treatments.treatment_or_therapy",
        "treatments.treatment_outcome",        # ← primary response label
        "treatments.treatment_intent_type",
        "treatments.therapeutic_agents",
        "treatments.initial_disease_status",
        "treatments.days_to_treatment_start",
        "treatments.days_to_treatment_end",
        "treatments.number_of_cycles",
        "treatments.treatment_type",
        "treatments.reason_treatment_ended",
    ]
    available = [c for c in keep if c in df.columns]
    return df[available].copy()
 
 
def load_pathology(CLINICAL_DIR: Path) -> pd.DataFrame:
    """
    Receptor status lives here: ER, PR, HER2.
    These are the PROTOCOL-SPECIFIED biomarkers for most BRCA trials.
    """
    path = CLINICAL_DIR / "pathology_detail.tsv"
    df = load_tsv(path)
    keep = [
        "case_id",
        "er_status_by_ihc",          # Estrogen receptor
        "pr_status_by_ihc",          # Progesterone receptor
        "her2_status_by_ihc",        # HER2 (IHC)
        "her2_fish_status",          # HER2 (FISH)
        "aneuploidy_score",
        "fraction_genome_altered",
        "tumor_grade",
        "lymph_node_examined_count",
        "lymph_nodes_positive",
    ]
    available = [c for c in keep if c in df.columns]
    return df[available].drop_duplicates("case_id")
 
 
def load_followup(CLINICAL_DIR: Path) -> pd.DataFrame:
    """Follow-up table — treatment response, progression."""
    path = CLINICAL_DIR / "follow_up.tsv"
    df = load_tsv(path)
    keep = [
        "case_id",
        "days_to_recurrence",
        "progression_or_recurrence",
        "disease_response",
        "ecog_performance_status",
        "karnofsky_performance_status",
    ]
    available = [c for c in keep if c in df.columns]
    # Take the most recent follow-up per patient
    if "days_to_recurrence" in available:
        df = df.sort_values("days_to_recurrence", ascending=False)
    return df[available].drop_duplicates("case_id")
 
 
def load_exposure(CLINICAL_DIR: Path) -> pd.DataFrame:
    """Exposure table — smoking, BMI, alcohol."""
    path = CLINICAL_DIR / "exposure.tsv"
    df = load_tsv(path)
    keep = [
        "case_id",
        "bmi", "weight", "height",
        "cigarettes_per_day", "years_smoked",
        "alcohol_history", "alcohol_intensity",
        "pack_years_smoked",
    ]
    available = [c for c in keep if c in df.columns]
    return df[available].drop_duplicates("case_id")
 
 
def load_sample(BIO_DIR: Path) -> pd.DataFrame:
    """Sample metadata — tumor vs normal, sample type."""
    path = BIO_DIR / "sample.tsv"
    df = load_tsv(path)
    keep = ["case_id", "sample_type", "tumor_descriptor", "tissue_type"]
    available = [c for c in keep if c in df.columns]
    return df[available].drop_duplicates("case_id")