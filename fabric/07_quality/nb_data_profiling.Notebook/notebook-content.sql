-- Fabric notebook source

-- METADATA ********************

-- META {
-- META   "kernel_info": {
-- META     "name": "sqldatawarehouse"
-- META   },
-- META   "dependencies": {
-- META     "lakehouse": {
-- META       "default_lakehouse_name": "",
-- META       "default_lakehouse_workspace_id": ""
-- META     },
-- META     "warehouse": {
-- META       "default_warehouse": "2aad1041-b26e-45ae-8ed6-422e337114ed",
-- META       "known_warehouses": [
-- META         {
-- META           "id": "2aad1041-b26e-45ae-8ed6-422e337114ed",
-- META           "type": "Lakewarehouse"
-- META         }
-- META       ]
-- META     }
-- META   }
-- META }

-- CELL ********************

SELECT 
    COLUMN_NAME
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'raw'
  AND TABLE_NAME = 'clinical_trials'
ORDER BY ORDINAL_POSITION;

-- METADATA ********************

-- META {
-- META   "language": "sql",
-- META   "language_group": "sqldatawarehouse"
-- META }

-- MARKDOWN ********************

-- The table clinical_trials has 496.615 rows, and the first column kaggle_id is the row number.
-- but I guess, maybe some rows are repeated, if we exclude this first id column.
-- Lets see if a distinct without the first row giv us the same count or less...

-- CELL ********************

SELECT COUNT(1) FROM raw.clinical_trials;

WITH the_IDs_excluded as
(
SELECT
--kaggle_id,
DISTINCT 
organization_full_name,
organization_class,
responsible_party,
brief_title,
full_title,
overall_status,
start_date,
standard_age,
conditions,
primary_purpose,
interventions,
intervention_description,
study_type,
phases,
outcome_measure,
medical_subject_headings  
FROM raw.clinical_trials
)
SELECT count(1) FROM the_IDs_excluded

-- METADATA ********************

-- META {
-- META   "language": "sql",
-- META   "language_group": "sqldatawarehouse"
-- META }

-- MARKDOWN ********************

-- Yes! is less 495712 
-- then 496615-495712 = 903 rows should be removed.
-- I will to this cleaning in staging layer..

-- CELL ********************

select 496615-495712 

-- METADATA ********************

-- META {
-- META   "language": "sparksql",
-- META   "language_group": "synapse_pyspark"
-- META }
