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
# META     }
# META   }
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC 
# MAGIC --DROP TABLE core.fact_clinical_trial;
# MAGIC 
# MAGIC CREATE TABLE IF NOT EXISTS core.fact_clinical_trial (
# MAGIC     trial_id STRING,
# MAGIC     start_date DATE,
# MAGIC 
# MAGIC     organization_key STRING,
# MAGIC     condition_key STRING,
# MAGIC     intervention_key STRING,
# MAGIC     study_key STRING,
# MAGIC 
# MAGIC     overall_status STRING,
# MAGIC     study_type STRING,
# MAGIC     phases STRING
# MAGIC );

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

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
# MAGIC 
# MAGIC         o.organization_key,
# MAGIC         c.condition_key,
# MAGIC         i.intervention_key,
# MAGIC         u.study_key,
# MAGIC         s.overall_status,
# MAGIC         s.study_type,
# MAGIC         s.phases
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
# MAGIC     start_date,
# MAGIC     organization_key,
# MAGIC     condition_key,
# MAGIC     intervention_key,
# MAGIC     study_key,
# MAGIC     overall_status,
# MAGIC     study_type,
# MAGIC     phases
# MAGIC )
# MAGIC VALUES (
# MAGIC     s.trial_id,
# MAGIC     s.start_date,
# MAGIC     s.organization_key,
# MAGIC     s.condition_key,
# MAGIC     s.intervention_key,
# MAGIC     s.study_key,
# MAGIC     s.overall_status,
# MAGIC     s.study_type,
# MAGIC     s.phases
# MAGIC );

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
