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

# ## Fact Table Load: `core.fact_clinical_trial`
# 
# ### Overview
# 
# This notebook is responsible for loading data into the `core.fact_clinical_trial` fact table.
# 
# The loading strategy follows a **merge-based ingestion pattern**:
# - Data is sourced from the `stg.clinical_trials` staging table
# - Surrogate/business keys are resolved via joins to dimension tables
# - The final result is upserted into the fact table
# 
# ---
# 
# ### Loading Strategy
# 
# The process consists of two steps:
# 
# 1. **Table reset (optional / full refresh step)**
#    - The target fact table is truncated before loading
#    - This ensures a clean state before re-inserting data
# 
# 2. **Merge operation**
#    - Data from staging is transformed and enriched
#    - Dimension keys are resolved using hashed natural keys
#    - Records are inserted into the fact table if they do not already exist
# 
# ---
# 
# ### ⚠️ Important Note on TRUNCATE
# 
# The current implementation includes a:
# 
# ```sql
# TRUNCATE TABLE core.fact_clinical_trial

# CELL ********************

# MAGIC %%sql
# MAGIC 
# MAGIC TRUNCATE TABLE core.fact_clinical_trial

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark",
# META   "frozen": false,
# META   "editable": true
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC 
# MAGIC MERGE INTO core.fact_clinical_trial t
# MAGIC USING (
# MAGIC     SELECT
# MAGIC         s.kaggle_id AS trial_id,
# MAGIC         s.start_date,
# MAGIC         o.organization_key,
# MAGIC         c.condition_key,
# MAGIC         i.intervention_key,
# MAGIC         u.study_key,
# MAGIC         s.overall_status,
# MAGIC         s.study_type,
# MAGIC         s.phases,
# MAGIC         s.primary_purpose,
# MAGIC         s.standard_age,
# MAGIC         s.outcome_measure
# MAGIC 
# MAGIC     FROM stg.clinical_trials s
# MAGIC 
# MAGIC     LEFT JOIN core.dim_organization o
# MAGIC         ON SHA2(CONCAT(
# MAGIC             COALESCE(TRIM(s.organization_full_name), 'UNKNOWN'),
# MAGIC             '|',
# MAGIC             COALESCE(TRIM(s.organization_class), 'UNKNOWN'),
# MAGIC             '|',
# MAGIC             COALESCE(TRIM(s.responsible_party), 'UNKNOWN')
# MAGIC         ), 256) = o.organization_key
# MAGIC 
# MAGIC     LEFT JOIN core.dim_condition c
# MAGIC         ON SHA2(CONCAT(
# MAGIC             COALESCE(TRIM(s.conditions), 'UNKNOWN'),
# MAGIC             '|',
# MAGIC             COALESCE(TRIM(s.medical_subject_headings), 'UNKNOWN')
# MAGIC         ), 256) = c.condition_key
# MAGIC 
# MAGIC     LEFT JOIN core.dim_intervention i
# MAGIC         ON SHA2(CONCAT(
# MAGIC             COALESCE(TRIM(s.interventions), 'UNKNOWN'),
# MAGIC             '|',
# MAGIC             COALESCE(TRIM(s.intervention_description), 'UNKNOWN')
# MAGIC         ), 256) = i.intervention_key
# MAGIC 
# MAGIC     LEFT JOIN core.dim_study u
# MAGIC         ON SHA2(CONCAT(
# MAGIC             COALESCE(TRIM(s.brief_title), 'UNKNOWN'),
# MAGIC             '|',
# MAGIC             COALESCE(TRIM(s.full_title), 'UNKNOWN')
# MAGIC         ), 256) = u.study_key        
# MAGIC ) s
# MAGIC 
# MAGIC ON t.trial_id = s.trial_id
# MAGIC 
# MAGIC WHEN NOT MATCHED THEN
# MAGIC INSERT (
# MAGIC     trial_id,
# MAGIC     date_key, 
# MAGIC     start_date,
# MAGIC     organization_key,
# MAGIC     condition_key,
# MAGIC     intervention_key,
# MAGIC     study_key,
# MAGIC     overall_status,
# MAGIC     study_type,
# MAGIC     phases,
# MAGIC     primary_purpose,
# MAGIC     standard_age,
# MAGIC     outcome_measure
# MAGIC )
# MAGIC VALUES (
# MAGIC     s.trial_id,
# MAGIC     YEAR(s.start_date)*10000 + MONTH(s.start_date)*100+ DAY(s.start_date),
# MAGIC     s.start_date,    
# MAGIC     s.organization_key,
# MAGIC     s.condition_key,
# MAGIC     s.intervention_key,
# MAGIC     s.study_key,
# MAGIC     s.overall_status,
# MAGIC     s.study_type,
# MAGIC     s.phases,
# MAGIC     s.primary_purpose,
# MAGIC     s.standard_age,
# MAGIC     s.outcome_measure
# MAGIC );

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC select * from  core.fact_clinical_trial limit 10

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
