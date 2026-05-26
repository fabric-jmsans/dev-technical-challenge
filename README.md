# Clinical Trial Data Pipeline — Microsoft Fabric Implementation

## Overview

This project was developed as part of a **Data Engineering Technical Challenge** focused on designing and implementing a clinical trial data platform.

The solution was built entirely using [Microsoft Fabric](https://www.microsoft.com/microsoft-fabric), leveraging Lakehouse architecture, notebooks, orchestration pipelines, semantic modeling, and reporting capabilities.

The goal of the project was to demonstrate practical Data Engineering skills including:

- Data ingestion
- Layered data architecture
- Data cleaning and transformation
- Dimensional modeling
- Orchestration
- Analytical consumption
- Reporting integration

Additionally, a lightweight reporting layer was created as part of the Data Analytics challenge exploration. However, the primary focus of the project remained on the Data Engineering architecture and implementation rather than deep clinical or medical analytics.

---

# Architecture Overview

The solution follows a layered medallion-style architecture implemented inside Microsoft Fabric.

```text
                        +----------------------+
                        | Clinical Trial Data  |
                        | CSV / API / Sources  |
                        +----------+-----------+
                                   |
                                   v
                     +--------------------------+
                     | 01_raw                   |
                     | Ingestion Notebooks      |
                     +------------+-------------+
                                  |
                                  v
                     +--------------------------+
                     | 02_stg                   |
                     | Cleaning & Standardizing |
                     +------------+-------------+
                                  |
                                  v
                     +--------------------------+
                     | 03_core                  |
                     | Facts & Dimensions       |
                     +------------+-------------+
                                  |
                                  v
                     +--------------------------+
                     | Semantic Model           |
                     | Power BI / Fabric Model  |
                     +------------+-------------+
                                  |
                                  v
                     +--------------------------+
                     | Reporting Layer          |
                     | MVP Power BI Report      |
                     +--------------------------+
```

---

<img width="1952" height="537" alt="image" src="https://github.com/user-attachments/assets/2871d9c2-6575-4b85-8a94-cbce54320332" />


# Project Structure

```text
fabric/
│
├── 00_admin/
│   ├── lh_clinical.Lakehouse
│   ├── nb_setup_schemas.Notebook
│   └── nb_kaggle_ingest.Notebook
│
├── 01_raw/
│   └── nb_raw_ingestion.Notebook
│
├── 02_stg/
│   └── nb_stg_cleaning.Notebook
│
├── 03_core/
│   ├── nb_core_dimensions.Notebook
│   └── nb_core_facts.Notebook
│
├── 04_model/
│   └── sm_clinical.SemanticModel
│
├── 05_orchestration/
│   └── pl_clinical_bootstrap.DataPipeline
│
└── 06_reporting/
    └── rpt_clinical_mvp.Report
```

---

# Solution Components

## Lakehouse

### `lh_clinical.Lakehouse`

The Lakehouse acts as the central storage layer for the solution.

It stores:

- Raw ingested datasets
- Staging tables
- Curated dimensional models
- Fact tables for analytics

The architecture follows a structured layered approach to improve maintainability, traceability, and scalability.

---

## Administration & Schema Setup

### `nb_setup_schemas.Notebook`

This notebook initializes the environment and prepares the required schemas and structures used throughout the pipeline.

Responsibilities include:

- Schema creation  
- Environment initialization  
- Table setup  
- Base configuration logic  

---

## Data Ingestion (Kaggle API)

### `nb_kaggle_ingest.Notebook`

The project now automates the ingestion of the source dataset using the :contentReference[oaicite:0]{index=0} API instead of manual CSV uploads.

Responsibilities:

- Download CSV from Kaggle to datalake via API

A Kaggle API token is securely stored in the Data Lake and used by a dedicated notebook to authenticate and download the dataset programmatically.

To enable this process in Microsoft Fabric, the required Kaggle Python libraries have been installed in a dedicated execution environment, and the notebooks are configured to run using this environment.

The downloaded dataset is written directly into the Lakehouse `Files` area, replacing the previous manual ingestion step.

---

# Data Pipeline Layers

## 01_raw — Data Ingestion

### `nb_raw_ingestion.Notebook`

This notebook handles ingestion of clinical trial datasets into the raw layer.

Responsibilities:

- Load CSV from datalake
- Preserve original structure
- Minimal transformation
- Initial metadata capture
- Basic ingestion validation

The raw layer is intentionally kept close to the source data for traceability and reproducibility.

---

## 02_stg — Data Cleaning & Standardization

### `nb_stg_cleaning.Notebook`

The staging layer performs cleaning and normalization operations.

Transformations include:

- Null handling
- Data type normalization
- Date standardization
- Duplicate removal
- Column renaming
- Schema alignment
- Data quality validation

This layer prepares the data for analytical modeling.

---

## 03_core — Dimensional Modeling

### `nb_core_dimensions.Notebook`

Creates and maintains dimension tables.

Examples:

- Studies
- Conditions
- Interventions
- Locations
- Sponsors

### `nb_core_facts.Notebook`

Builds fact tables containing measurable events and metrics related to clinical trials.

Examples:

- Enrollment metrics
- Study progress
- Completion statistics
- Outcome aggregations

The core layer follows dimensional modeling principles optimized for analytics consumption.

---

# Semantic Model

## `sm_clinical.SemanticModel`

A semantic model was created to expose curated analytical data for reporting.

The model includes:

- Relationships
- Measures
- Business logic
- Hierarchies
- Optimized analytical structures

This layer enables simplified consumption from Power BI reports.

---

# Orchestration

## `pl_clinical_bootstrap.DataPipeline`

The orchestration pipeline coordinates execution of the notebooks in the correct sequence.

Pipeline flow:

1. Schema setup
2. Raw ingestion
3. Staging transformations
4. Core dimensional loading
5. Fact generation

The pipeline demonstrates orchestration concepts such as:

- Dependency management
- Execution sequencing
- Modular processing
- Reusability

Execution Gantt:

<img width="1762" height="715" alt="image" src="https://github.com/user-attachments/assets/c930d633-5c34-44c6-8ee5-cff8416f2dde" />


---

# Reporting Layer

## `rpt_clinical_mvp.Report`

A lightweight MVP report was developed to demonstrate analytical consumption of the curated model.

The report includes exploratory visualizations such as:

- Clinical trials by phase
- Enrollment distributions
- Geographic analysis
- Study timelines
- Intervention analysis

The reporting layer was intentionally kept simple because the project focus was primarily on Data Engineering implementation rather than advanced clinical analytics.

---

# Technologies Used

## Microsoft Fabric Components

- Fabric Lakehouse
- Fabric Notebooks
- Fabric Data Pipelines
- Semantic Models
- Power BI Reporting

## Languages & Frameworks

- Python
- PySpark
- SQL
- DAX

---

# Engineering Concepts Demonstrated

## Medallion Architecture

The solution follows a layered architecture pattern:

| Layer | Purpose |
|---|---|
| Raw | Preserve source data |
| Staging | Cleaning and standardization |
| Core | Business-ready dimensional model |
| Reporting | Analytical consumption |

---

## Data Quality Handling

The pipeline includes validation and cleaning logic for handling real-world dataset inconsistencies.

Examples:

- Missing values
- Invalid dates
- Duplicated studies
- Non-standard categorical values
- Schema inconsistencies

---

## Dimensional Modeling

The curated model separates:

- Dimension entities
- Fact measurements
- Business metrics

This improves:

- Query performance
- Analytical flexibility
- Reporting usability

---

# Scalability Considerations

The architecture was designed with scalability in mind.

Potential future improvements include:

- Incremental loading
- Partitioning strategies
- Larger Spark optimizations
- CI/CD integration
- Automated testing
- Metadata-driven pipelines
- Parameterized orchestration
- Data lineage tracking

Microsoft Fabric provides strong foundations for scaling these workloads.

---

# Monitoring & Observability

Microsoft Fabric already provides built-in monitoring capabilities for pipelines, notebook executions, semantic model refreshes, and dataflows.  
For this challenge, monitoring and operational visibility were validated using the native Fabric monitoring experience, including execution history, duration tracking, and failure diagnostics.

The solution can be further enhanced with production-oriented observability practices such as:

- Centralized monitoring of pipeline and notebook executions
- Data quality validation dashboards
- Automated failure alerting and notifications
- SLA and execution time monitoring
- Centralized logging and audit tracking
- Historical execution metrics and trend analysis
- Refresh and dependency monitoring across workloads

Additionally, screenshots of the latest successful and failed executions were included to demonstrate operational traceability, execution monitoring, and troubleshooting capabilities available within Microsoft Fabric.

<img width="1685" height="1039" alt="image" src="https://github.com/user-attachments/assets/cbb365c0-9eec-468d-9dac-75afe21c6a3c" />

---

# Security Considerations

For sensitive healthcare-related datasets, additional controls would be recommended:

- RBAC security
- Workspace isolation
- Managed identities
- Secret management
- Data masking
- Encryption at rest and in transit
- Audit logging

---

# Limitations

Due to the challenge time constraints, some areas were intentionally simplified:

- Limited reporting sophistication
- Basic business metrics
- Minimal clinical domain interpretation
- Limited automated testing
- No production deployment automation

The primary goal was to demonstrate strong Data Engineering foundations and architectural thinking inside the Microsoft Fabric ecosystem.

---

# AI Assistance

AI tools such as ChatGPT were used during development to support:

- Architecture brainstorming
- Documentation drafting
- Transformation logic ideas
- SQL and PySpark assistance
- Troubleshooting

All final implementation decisions and validations were reviewed manually.

---

# Future Improvements

Potential future enhancements:

- Advanced Power BI dashboards
- dbt integration
- Automated data validation framework
- Incremental processing
- Real-time ingestion
- Data catalog integration
- CI/CD deployment pipelines
- Healthcare-specific KPI modeling

---

# Final Notes

This project was designed to showcase practical modern Data Engineering skills using Microsoft Fabric.

The implementation focuses on:

- Structured layered architecture
- Maintainable transformation pipelines
- Dimensional modeling
- Analytical readiness
- Orchestration concepts
- Scalable design principles

Although a reporting layer was included, the main emphasis of the project was the Data Engineering challenge and the implementation of a robust data platform architecture within the Fabric ecosystem.
