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
