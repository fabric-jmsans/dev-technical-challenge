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
# META       "environmentId": "56cd7efa-19af-810a-481c-642e63e02af5",
# META       "workspaceId": "00000000-0000-0000-0000-000000000000"
# META     }
# META   }
# META }

# MARKDOWN ********************

# # Core Dimension Loading
# 
# ## Objective
# 
# This notebook loads and transforms data from the staging layer into the core dimensional model.
# 
# The process:
# - extracts and standardizes business entities from staging data
# - applies deterministic business key generation
# - loads dimension tables using MERGE operations to ensure uniqueness
# 
# Source layer:
# `stg`
# 
# Target layer:
# `core`
# 
# During development, dimension tables may be truncated before reload to simplify iterative testing and rapid model changes.

# MARKDOWN ********************

# ## Development Reset
# 
# During development and testing, core tables are truncated before reloading data.
# 
# This approach simplifies:
# - iterative model changes
# - business rule adjustments
# - schema evolution
# - validation of transformation logic
# 
# In production environments, tables would normally be maintained incrementally using MERGE operations without full truncation.

# CELL ********************

# MAGIC %%sql
# MAGIC 
# MAGIC TRUNCATE TABLE core.dim_organization;
# MAGIC TRUNCATE TABLE core.dim_condition;
# MAGIC TRUNCATE TABLE core.dim_intervention;
# MAGIC TRUNCATE TABLE core.dim_study;
# MAGIC TRUNCATE TABLE core.dim_date;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Load Dimension Data
# 
# This section populates the dimension tables from the staging layer.
# 
# The process:
# - extracts distinct business entities
# - standardizes attribute values
# - generates deterministic business keys
# - loads new records using MERGE logic
# 
# The MERGE strategy supports future incremental loading patterns while preventing duplicate dimension entries.

# CELL ********************

# MAGIC %%sql
# MAGIC 
# MAGIC MERGE INTO core.dim_organization t
# MAGIC USING (
# MAGIC     SELECT DISTINCT
# MAGIC         SHA2(CONCAT(
# MAGIC             COALESCE(TRIM(organization_full_name), 'UNKNOWN'),
# MAGIC             '|',
# MAGIC             COALESCE(TRIM(organization_class), 'UNKNOWN'),
# MAGIC             '|',
# MAGIC             COALESCE(TRIM(responsible_party), 'UNKNOWN')
# MAGIC         ), 256) AS organization_key,
# MAGIC 
# MAGIC         COALESCE(TRIM(organization_full_name), 'Unknown') AS organization_full_name,
# MAGIC         COALESCE(TRIM(organization_class), 'Unknown') AS organization_class,
# MAGIC         COALESCE(TRIM(responsible_party), 'Unknown') AS responsible_party
# MAGIC 
# MAGIC     FROM stg.clinical_trials
# MAGIC ) s
# MAGIC ON t.organization_key = s.organization_key
# MAGIC 
# MAGIC WHEN NOT MATCHED THEN
# MAGIC INSERT (
# MAGIC     organization_key,
# MAGIC     organization_full_name,
# MAGIC     organization_class,
# MAGIC     responsible_party
# MAGIC )
# MAGIC VALUES (
# MAGIC     s.organization_key,
# MAGIC     s.organization_full_name,
# MAGIC     s.organization_class,
# MAGIC     s.responsible_party
# MAGIC );


# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC select count(1) from stg.clinical_trials

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC 
# MAGIC SELECT *
# MAGIC FROM stg.clinical_trials
# MAGIC LIMIT 10

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT  COALESCE(overall_status, 'Unknown') as overall_status, 
# MAGIC         count(1) as cases
# MAGIC FROM stg.clinical_trials
# MAGIC group by overall_status
# MAGIC order by cases desc

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC select count(1) from 
# MAGIC (
# MAGIC select brief_title, full_title , count(1) as cases
# MAGIC FROM stg.clinical_trials
# MAGIC group by brief_title, full_title 
# MAGIC )


# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC 
# MAGIC MERGE INTO core.dim_condition t
# MAGIC USING (
# MAGIC     SELECT DISTINCT
# MAGIC         SHA2(CONCAT(
# MAGIC             COALESCE(TRIM(conditions), 'UNKNOWN'),
# MAGIC             '|',
# MAGIC             COALESCE(TRIM(medical_subject_headings), 'UNKNOWN')
# MAGIC         ), 256) AS condition_key,
# MAGIC         COALESCE(TRIM(conditions), 'Unknown') AS condition_name,
# MAGIC         COALESCE(TRIM(medical_subject_headings), 'Unknown') AS medical_subject_headings
# MAGIC     FROM stg.clinical_trials
# MAGIC ) s
# MAGIC ON t.condition_key = s.condition_key
# MAGIC 
# MAGIC WHEN NOT MATCHED THEN
# MAGIC INSERT (
# MAGIC     condition_key,
# MAGIC     condition_name,
# MAGIC     medical_subject_headings
# MAGIC )
# MAGIC VALUES (
# MAGIC     s.condition_key,
# MAGIC     s.condition_name,
# MAGIC     s.medical_subject_headings
# MAGIC );

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC 
# MAGIC MERGE INTO core.dim_intervention t
# MAGIC USING (
# MAGIC     SELECT DISTINCT
# MAGIC         SHA2(CONCAT(
# MAGIC             COALESCE(TRIM(interventions), 'UNKNOWN'),
# MAGIC             '|',
# MAGIC             COALESCE(TRIM(intervention_description), 'UNKNOWN')
# MAGIC         ), 256) AS intervention_key,
# MAGIC         COALESCE(TRIM(interventions), 'Unknown') AS intervention_name,
# MAGIC         COALESCE(TRIM(intervention_description), 'Unknown') AS intervention_description
# MAGIC     FROM stg.clinical_trials
# MAGIC ) s
# MAGIC ON t.intervention_key = s.intervention_key
# MAGIC 
# MAGIC WHEN NOT MATCHED THEN
# MAGIC INSERT (
# MAGIC     intervention_key,
# MAGIC     intervention_name,
# MAGIC     intervention_description
# MAGIC )
# MAGIC VALUES (
# MAGIC     s.intervention_key,
# MAGIC     s.intervention_name,
# MAGIC     s.intervention_description
# MAGIC );

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC 
# MAGIC MERGE INTO core.dim_study t
# MAGIC USING (
# MAGIC     SELECT DISTINCT
# MAGIC         SHA2(CONCAT(
# MAGIC             COALESCE(TRIM(brief_title), 'UNKNOWN'),
# MAGIC             '|',
# MAGIC             COALESCE(TRIM(full_title), 'UNKNOWN')
# MAGIC         ), 256) AS study_key,
# MAGIC         COALESCE(TRIM(brief_title), 'Unknown') AS study_short_title,
# MAGIC         COALESCE(TRIM(full_title), 'Unknown') AS study_official_title
# MAGIC     FROM stg.clinical_trials
# MAGIC ) s
# MAGIC ON t.study_key = s.study_key
# MAGIC 
# MAGIC WHEN NOT MATCHED THEN
# MAGIC INSERT (
# MAGIC     study_key,
# MAGIC     study_short_title,
# MAGIC     study_official_title
# MAGIC )
# MAGIC VALUES (
# MAGIC     s.study_key,
# MAGIC     s.study_short_title,
# MAGIC     s.study_official_title
# MAGIC );

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC 
# MAGIC SELECT LEFT(start_date,4), count(1) as cases
# MAGIC FROM stg.clinical_trials
# MAGIC GROUP BY LEFT(start_date,4)
# MAGIC ORDER BY  LEFT(start_date,4) desc

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark",
# META   "frozen": true,
# META   "editable": false
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC 
# MAGIC SELECT * FROM stg.clinical_trials
# MAGIC WHERE LEFT(start_date,4) = '2050'

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark",
# META   "frozen": true,
# META   "editable": false
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC 
# MAGIC 
# MAGIC SELECT * FROM raw.clinical_trials
# MAGIC WHERE kaggle_id IN (6104,334122)

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark",
# META   "frozen": true,
# META   "editable": false
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC 
# MAGIC     SELECT
# MAGIC         DATE_SUB(MIN(start_date), 365) AS start_date,
# MAGIC         DATE_ADD(MAX(start_date), 365) AS end_date
# MAGIC     FROM stg.clinical_trials

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark",
# META   "frozen": true,
# META   "editable": false
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT standard_age , count(1) cases
# MAGIC FROM stg.clinical_trials
# MAGIC group by standard_age
# MAGIC order  by cases desc

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT study_type , count(1) cases
# MAGIC FROM stg.clinical_trials
# MAGIC group by study_type
# MAGIC order by cases desc

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC describe core.dim_date

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark",
# META   "frozen": true,
# META   "editable": false
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC 
# MAGIC WITH calendar AS (
# MAGIC     SELECT explode(
# MAGIC         sequence(
# MAGIC             to_date('1990-01-01'),
# MAGIC             to_date('2024-12-31'),
# MAGIC             interval 1 day
# MAGIC         )
# MAGIC     ) AS date_value
# MAGIC )
# MAGIC 
# MAGIC INSERT INTO core.dim_date
# MAGIC SELECT
# MAGIC     YEAR(date_value)*10000 + MONTH(date_value) *100 + DAY(date_value) AS date_key,
# MAGIC     date_value AS date_value,
# MAGIC     YEAR(date_value) AS year,
# MAGIC     MONTH(date_value) AS month,
# MAGIC     DATE_FORMAT(date_value, 'MMMM') AS month_name,
# MAGIC     QUARTER(date_value) AS quarter,
# MAGIC     WEEKOFYEAR(date_value) AS week,
# MAGIC     DAY(date_value) AS day,
# MAGIC     DATE_FORMAT(date_value, 'EEEE') AS day_name,
# MAGIC     CASE WHEN DAYOFWEEK(date_value) IN (1, 7) THEN true ELSE false END AS is_weekend
# MAGIC FROM calendar;


# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
