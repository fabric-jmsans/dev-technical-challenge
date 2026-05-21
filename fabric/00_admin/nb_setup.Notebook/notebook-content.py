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

# MARKDOWN ********************

# # Core Layer Setup
# 
# ## Objective
# 
# This notebook initializes the core analytical layer of the Lakehouse.
# 
# The process creates the dimension and fact tables required for the dimensional model if they do not already exist.
# 
# Responsibilities:
# - create schemas and tables in core
# - define analytical structures
# - establish standardized datatypes
# - prepare the environment for dimension and fact loading processes
# 
# The notebook is intended to be executed:
# - during initial environment setup
# - after schema changes
# - during deployment or infrastructure provisioning
# 
# Target layer:
# `core`
# 
# Notes:
# - This notebook only defines table structures
# - No business transformations or data loading are performed here
# - Data ingestion and merge logic are handled in separate notebooks

# CELL ********************

# MAGIC %%sql
# MAGIC 
# MAGIC -------------------------
# MAGIC -- CREATE ALL SCHEMAS
# MAGIC ------------------------
# MAGIC 
# MAGIC CREATE SCHEMA IF NOT EXISTS sandbox;
# MAGIC 
# MAGIC CREATE SCHEMA IF NOT EXISTS raw;
# MAGIC 
# MAGIC CREATE SCHEMA IF NOT EXISTS stg;
# MAGIC 
# MAGIC CREATE SCHEMA IF NOT EXISTS core;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
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
# MAGIC CREATE TABLE IF NOT EXISTS core.dim_study (
# MAGIC     study_key STRING,
# MAGIC     study_short_title STRING,
# MAGIC     study_official_title STRING
# MAGIC );

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
