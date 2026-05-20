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

from pyspark.sql import functions as F
from pyspark.sql.types import LongType

# =========================
# READ FROM RAW
# =========================

df_raw = spark.table("raw.clinical_trials")

# =========================
# GENERIC NORMALIZATION FUNCTION
# =========================

def normalize_text(col_name):
    return (
        F.when(
            F.col(col_name).isNull(),
            None
        )
        .when(
            F.trim(F.lower(F.col(col_name))).isin(
                "",
                "unknown",
                "n/a",
                "na",
                "null",
                "none"
            ),
            None
        )
        .otherwise(
            F.trim(F.col(col_name))
        )
    )

# =========================
# STEP 1: GENERIC CLEANING
# =========================

df_stg = (
    df_raw
    .withColumn("kaggle_id", F.col("kaggle_id").cast(LongType()))
    .withColumn("organization_full_name", normalize_text("organization_full_name"))
    .withColumn("organization_class", normalize_text("organization_class"))
    .withColumn("responsible_party", normalize_text("responsible_party"))
    .withColumn("brief_title", normalize_text("brief_title"))
    .withColumn("full_title", normalize_text("full_title"))
    .withColumn("overall_status", normalize_text("overall_status"))
    .withColumn("start_date", normalize_text("start_date"))
    .withColumn("standard_age", normalize_text("standard_age"))
    .withColumn("conditions", normalize_text("conditions"))
    .withColumn("primary_purpose", normalize_text("primary_purpose"))
    .withColumn("interventions", normalize_text("interventions"))
    .withColumn("intervention_description", normalize_text("intervention_description"))
    .withColumn("study_type", normalize_text("study_type"))
    .withColumn("phases", normalize_text("phases"))
    .withColumn("outcome_measure", normalize_text("outcome_measure"))
    .withColumn("medical_subject_headings", normalize_text("medical_subject_headings"))
)

# =========================
# STEP 2: BUSINESS RULES (PHASES)
# =========================

df_stg = df_stg.withColumn(
    "phases",
    F.when(
        F.lower(F.col("phases")) == "no phases listed",
        None
    ).otherwise(
        F.col("phases")
    )
)

# =========================
# STEP 3: BUSINESS RULES (DATES)
# =========================


df_stg = df_stg.withColumn(
    "start_date",
    F.when(
        F.col("start_date").isNull(),
        None
    )
    # format YYYY-MM-DD already complete → keep it
    .when(
        F.col("start_date").rlike(r"^\d{4}-\d{2}-\d{2}$"),
        F.to_date(F.col("start_date"))
    )
    # format YYYY-MM → adding day 01
    .when(
        F.col("start_date").rlike(r"^\d{4}-\d{2}$"),
        F.to_date(F.concat(F.col("start_date"), F.lit("-01")))
    )
    # format only year → force gengenuary  1
    .when(
        F.col("start_date").rlike(r"^\d{4}$"),
        F.to_date(F.concat(F.col("start_date"), F.lit("-01-01")))
    )
    .otherwise(
        F.to_date(F.col("start_date"))
    )
)



# =========================
# CREATE STAGING SCHEMA
# =========================

#spark.sql("CREATE SCHEMA IF NOT EXISTS stg")

# =========================
# RESET TABLE (DEV ONLY)
# =========================

spark.sql("DROP TABLE IF EXISTS stg.clinical_trials")

# =========================
# CREATE TABLE
# =========================

spark.sql("""
CREATE TABLE stg.clinical_trials (

    kaggle_id BIGINT,
    organization_full_name STRING,
    organization_class STRING,
    responsible_party STRING,
    brief_title STRING,
    full_title STRING,
    overall_status STRING,
    start_date DATE,
    standard_age STRING,
    conditions STRING,
    primary_purpose STRING,
    interventions STRING,
    intervention_description STRING,
    study_type STRING,
    phases STRING,
    outcome_measure STRING,
    medical_subject_headings STRING
)
USING DELTA
""")

# =========================
# INSERT DATA
# =========================

(
    df_stg
    .write
    .mode("append")
    .insertInto("stg.clinical_trials")
)

# =========================
# VALIDATION
# =========================

print(f"Rows inserted: {df_stg.count()}")

spark.table("stg.clinical_trials").show(5)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Check distinct IDs because Kaggle IDs may contain duplicates, so distinct count validates uniqueness vs total rows
print(f"Total distinct rows: {df_stg.select('kaggle_id').distinct().count()}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
