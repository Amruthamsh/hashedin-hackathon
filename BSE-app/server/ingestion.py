"""
BSE — Layer 1: Broad Biomarker Ingestion & Profiling
------------------------------------------------------
Reads TCGA-BRCA clinical + biospecimen TSVs, builds a unified
patient-level biomarker matrix, and separates markers into
  - protocol_specified  : ER, PR, HER2 (the pre-specified trial arms)
  - unexamined          : everything else in the landscape
 
Output: data/bse_patient_matrix.parquet  (used by discovery.py)
        data/bse_profiling_report.json   (used by the dashboard)
"""


import os
import json
import warnings
import pandas as pd
import numpy as np
from pathlib import Path
 
warnings.filterwarnings("ignore")
 
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "TCGA-BRCA"

if not DATA_DIR.exists():
  raise FileNotFoundError(f"Data directory not found: {DATA_DIR}")
 
CLINICAL_DIR  = next(DATA_DIR.glob("clinical.project-tcga-brca*"), None)
BIO_DIR       = next(DATA_DIR.glob("biospecimen.project-tcga-brca*"), None)
ANNOTATIONS   = next(DATA_DIR.glob("annotations-table*"), None)
 
OUT_MATRIX    = DATA_DIR / "bse_patient_matrix.parquet"
OUT_REPORT    = DATA_DIR / "bse_profiling_report.json"
 
print(f"Reading clinical data from: {CLINICAL_DIR}")
print(f"Reading biospecimen data from: {BIO_DIR}")
print(f"Reading annotations from: {ANNOTATIONS}")