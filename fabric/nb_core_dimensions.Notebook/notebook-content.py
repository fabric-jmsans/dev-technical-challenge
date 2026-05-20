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
# MAGIC CREATE TABLE IF NOT EXISTS core.dim_organization (
# MAGIC     organization_key STRING,
# MAGIC     organization_full_name STRING,
# MAGIC     organization_class STRING,
# MAGIC     responsible_party STRING
# MAGIC );

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC 
# MAGIC CREATE TABLE IF NOT EXISTS core.dim_condition (
# MAGIC     condition_key STRING,
# MAGIC     condition_name STRING,
# MAGIC     medical_subject_headings STRING
# MAGIC );

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC 
# MAGIC CREATE TABLE IF NOT EXISTS core.dim_intervention (
# MAGIC     intervention_key STRING,
# MAGIC     intervention_name STRING,
# MAGIC     intervention_description STRING
# MAGIC );

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC 
# MAGIC CREATE TABLE IF NOT EXISTS core.dim_date (
# MAGIC     date_key DATE,
# MAGIC     year INT,
# MAGIC     month INT,
# MAGIC     month_name STRING,
# MAGIC     quarter INT,
# MAGIC     week INT,
# MAGIC     day INT,
# MAGIC     day_name STRING,
# MAGIC     is_weekend BOOLEAN
# MAGIC );

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC 
# MAGIC TRUNCATE TABLE core.dim_organization;
# MAGIC 
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
# MAGIC 
# MAGIC SELECT *
# MAGIC FROM stg.clinical_trials
# MAGIC LIMIT 3

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC 
# MAGIC TRUNCATE TABLE core.dim_condition;
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
# MAGIC TRUNCATE TABLE core.dim_intervention;
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
# MAGIC 
# MAGIC TRUNCATE TABLE core.dim_date;
# MAGIC 
# MAGIC WITH calendar AS (
# MAGIC     SELECT explode(
# MAGIC         sequence(
# MAGIC             to_date('1990-01-01'),
# MAGIC             to_date('2024-12-31'),
# MAGIC             interval 1 day
# MAGIC         )
# MAGIC     ) AS date_key
# MAGIC )
# MAGIC 
# MAGIC INSERT INTO core.dim_date
# MAGIC SELECT
# MAGIC     date_key,
# MAGIC     YEAR(date_key) AS year,
# MAGIC     MONTH(date_key) AS month,
# MAGIC     DATE_FORMAT(date_key, 'MMMM') AS month_name,
# MAGIC     QUARTER(date_key) AS quarter,
# MAGIC     WEEKOFYEAR(date_key) AS week,
# MAGIC     DAY(date_key) AS day,
# MAGIC     DATE_FORMAT(date_key, 'EEEE') AS day_name,
# MAGIC     CASE WHEN DAYOFWEEK(date_key) IN (1, 7) THEN true ELSE false END AS is_weekend
# MAGIC FROM calendar;


# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
