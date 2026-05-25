# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "99f8b8c7-918b-4151-a05c-3b3707ad8488",
# META       "default_lakehouse_name": "lh_clinical",
# META       "default_lakehouse_workspace_id": "0a207e52-568d-442c-a669-d39849fb8cc5",
# META       "known_lakehouses": [
# META         {
# META           "id": "99f8b8c7-918b-4151-a05c-3b3707ad8488"
# META         }
# META       ]
# META     },
# META     "environment": {
# META       "environmentId": "ded45eef-c2ae-b335-4b59-d5f15503cc91",
# META       "workspaceId": "00000000-0000-0000-0000-000000000000"
# META     }
# META   }
# META }

# MARKDOWN ********************

# ## 1 — Load credentials and configure the Kaggle client

# CELL ********************

import os
import sys

# ── Locate the secrets file ──────────────────────────────────────────────────
SECRETS_PATH = "/lakehouse/default/Files/kaggle_secrets.py"

if not os.path.exists(SECRETS_PATH):
    raise FileNotFoundError(
        f"kaggle_secrets.py not found at {SECRETS_PATH}.\n"
        "Create it with KAGGLE_USERNAME and KAGGLE_KEY, and add it to .gitignore."
    )

# ── Import secrets ───────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(SECRETS_PATH))
import kaggle_secrets as _s

# ── Inject credentials as env vars (required by the kaggle library) ──────────
os.environ['KAGGLE_USERNAME'] = _s.KAGGLE_USERNAME
os.environ['KAGGLE_KEY']      = _s.KAGGLE_KEY

print('✅ Kaggle credentials loaded.')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 3 — Download a dataset from Kaggle

# CELL ********************

import kaggle

# Format: 'owner/dataset-slug'
DATASET      = 'danielansted/clinicaltrials-gov-clinical-trials-dataset'
DOWNLOAD_DIR = '/lakehouse/default/Files'  # local staging area inside the Fabric session

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

kaggle.api.authenticate()
kaggle.api.dataset_download_files(
    DATASET,
    path=DOWNLOAD_DIR,
    unzip=True
)

print(f'Dataset downloaded to {DOWNLOAD_DIR}')
print('Files:', os.listdir(DOWNLOAD_DIR))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
