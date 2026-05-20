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
# META     "environment": {}
# META   }
# META }

# CELL ********************

from pyspark.sql import SparkSession
import re

# Read the CSV file using the required parsing options
# - header: first row contains column names
# - multiLine: allows line breaks inside quoted text fields
# - quote / escape: handles quoted text correctly
# - delimiter: comma-separated values
df = (
    spark.read
    .option("header", "true")
    .option("multiLine", "true")
    .option("quote", '"')
    .option("escape", '"')
    .option("delimiter", ",")
    .csv("Files/clin_trials.csv")
)

# Display original column names
print(df.columns)

# The first column exists but has an empty header name.
# It represents the original Kaggle row identifier.
original_cols = df.columns
original_cols[0] = "kaggle_id"

# Apply the temporary corrected column names
# df.toDF(*cols) is equivalent to df.toDF("id", "name", ...)
df = df.toDF(*original_cols)

# Function to sanitize column names for Lakehouse / SQL compatibility
def clean_column_name(col_name):
    # Convert to lowercase
    col_name = col_name.lower()

    # Replace invalid characters with underscore
    col_name = re.sub(r'[^a-z0-9]+', '_', col_name)

    # Replace multiple underscores with a single underscore
    col_name = re.sub(r'_+', '_', col_name)

    # Remove leading and trailing underscores
    col_name = col_name.strip('_')

    # Limit column length to 128 characters
    return col_name[:128]

# Apply column name sanitization
clean_cols = [clean_column_name(c) for c in df.columns]

df = df.toDF(*clean_cols)

# Display final schema
df.printSchema()

# Count total rows
print(f"Total rows: {df.count()}")

# Create staging schema if it does not exist
# spark.sql("CREATE SCHEMA IF NOT EXISTS raw")

# Save the dataframe as a Delta table in the Lakehouse
(
    df.write
    .mode("overwrite")
    .format("delta")
    .saveAsTable("raw.clinical_trials")
)

print("Table raw.clinical_trials created successfully")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Check distinct IDs because Kaggle IDs may contain duplicates, so distinct count validates uniqueness vs total rows
print(f"Total distinct rows: {df.select('kaggle_id').distinct().count()}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
