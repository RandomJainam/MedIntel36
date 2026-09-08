# MedIntel360

**AI-Powered Healthcare Analytics & Natural-Language Intelligence Platform**

MedIntel360 is an end-to-end healthcare analytics platform that transforms structured hospital data into actionable insights through interactive dashboards and a natural-language AI analytics interface.

It combines **data preprocessing, data mining, ETL, metadata-driven analytics, database querying, and LLM-powered insight generation** into a unified workflow so users can explore healthcare data without manually writing SQL.

---

## Overview

Healthcare data can span multiple operational and analytical datasets. Turning that data into useful answers requires more than querying a table: the system needs to understand the analytical intent, identify the relevant metrics and dimensions, generate appropriate SQL, validate it, execute it safely, and explain the result.

MedIntel360 is designed around that complete workflow.

```text
Source Data
    │
    ▼
Preprocessing & Data Mining
    │
    ▼
ETL / Analytical Preparation
    │
    ▼
Metadata & Semantic Layer
    │
    ▼
SQLite Analytical Database
    │
    ├───────────────────┐
    ▼                   ▼
Dashboards         AI Analytics
                        │
                        ▼
                 Natural-Language Query
                        │
                        ▼
              Understanding & Context
                        │
                        ▼
                  SQL Generation
                        │
                        ▼
                  SQL Validation
                        │
                        ▼
                Database Execution
                        │
                        ▼
                 Insight Generation
                        │
                        ▼
                 Analytical Response
```

---

## Key Features

### Healthcare Analytics
- Interactive Streamlit dashboards
- Finance, operations, patient, and medical analytics
- KPI-oriented analytical views
- Structured analytical datasets

### AI-Powered Analytics
- Natural-language healthcare queries
- Metadata-driven query understanding
- Natural-language-to-SQL generation
- SQL validation and safety checks
- Controlled database execution
- LLM-powered insight generation
- Response formatting and normalization
- Conversation and follow-up query handling
- Input and LLM-output guardrails

### Data Engineering & Mining
- Data preprocessing workflows
- ETL and analytical data preparation
- Star-schema / analytical data workflows
- Data-mining capabilities
- Structured metadata and business rules
- Dataset, metric, dimension, and relationship definitions

### Engineering
- Modular Python architecture
- Dedicated database execution layer
- Automated tests for major components
- Configurable LLM integration through OpenRouter
- Environment-variable based configuration

---

# AI Analytics Pipeline

The core natural-language analytics workflow is orchestrated by the **Query Engine**.

```text
User Query
    │
    ▼
Data Understanding
    │
    ├── Conversation Context
    ├── Schema Metadata
    ├── Metrics
    ├── Dimensions
    └── Business Definitions
    │
    ▼
SQL Generation
    │
    ▼
SQL Validation
    │
    ▼
Controlled Database Execution
    │
    ▼
Insight Generation
    │
    ▼
Response Formatting
    │
    ▼
Analytical Response
```

### 1. Data Understanding

The natural-language question is interpreted using structured metadata and conversation context.

The system can identify analytical concepts such as:

- datasets
- metrics
- dimensions
- filters
- analytical intent
- schema relationships
- business definitions

### 2. SQL Generation

The structured understanding is converted into an SQL query suitable for the analytical database.

### 3. SQL Validation

Generated SQL passes through a validation layer before reaching the database.

This creates a controlled boundary between LLM-generated SQL and database execution and helps reject unsupported or unsafe operations.

### 4. Database Execution

Validated queries are executed through the dedicated database layer.

Execution results can contain:

- columns
- rows
- row count
- execution status
- errors
- truncation state

### 5. Insight Generation

The database result is passed to the insight-generation layer.

The LLM is instructed to base the analytical response on the supplied database result rather than inventing database facts independently.

### 6. Response Formatting

The generated response is normalized before being presented to the user through the dashboard.

---

# Conversation & Follow-Up Analytics

MedIntel360 includes conversation-aware query handling so users can interact with the analytics layer naturally.

For example:

```text
User: What is the total revenue?

AI: The total revenue is ...

User: What about by department?

AI: ...
```

The system can use conversational context when determining whether a new question depends on a previous analytical query.

At the same time, follow-up detection is being refined to distinguish a genuine continuation from a completely new analytical topic.

> Conversational analytics is an actively evolving part of the project.

---

# Data & Analytics Workflow

MedIntel360 separates data preparation from the AI querying layer.

```text
Source Data
    │
    ▼
Preprocessing
    │
    ▼
Data Mining / Feature Engineering
    │
    ▼
ETL Processing
    │
    ▼
Analytical / Gold Data
    │
    ▼
SQLite Database
    │
    ├───────────────┐
    ▼               ▼
Dashboards      AI Analytics
```

The metadata layer provides structured definitions for concepts including:

- datasets
- relationships
- metrics
- dimensions
- calculated metrics
- KPIs
- business rules
- glossary terms
- synonyms
- query templates
- prompt rules

This gives the AI layer a defined analytical vocabulary rather than forcing it to reason only from raw database column names.

---

# Architecture

```text
                         ┌──────────────────────┐
                         │     Streamlit UI     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     Query Engine     │
                         └──────────┬───────────┘
                                    │
             ┌──────────────────────┼──────────────────────┐
             │                      │                      │
             ▼                      ▼                      ▼
      Data Understanding     SQL Generation        Conversation
             │                      │                Context
             └──────────────────────┼──────────────────────┘
                                    ▼
                           ┌─────────────────┐
                           │ SQL Validation  │
                           └────────┬────────┘
                                    ▼
                           ┌─────────────────┐
                           │ DB Executor     │
                           └────────┬────────┘
                                    ▼
                           ┌─────────────────┐
                           │ Insight         │
                           │ Generator       │
                           └────────┬────────┘
                                    ▼
                           ┌─────────────────┐
                           │ Response        │
                           │ Formatter      │
                           └─────────────────┘

Supporting layers:
├── Metadata & Schema Management
├── Business Rules
├── Guardrails
├── ETL
├── Data Mining
├── Database Connectivity
└── Validation / Utilities
```

---

# Project Structure

```text
MedIntel360/
│
├── ai_engine/                 # AI analytics and query orchestration
│   ├── base_agent.py
│   ├── conversation_manager.py
│   ├── data_quality_agent.py
│   ├── data_understanding_agent.py
│   ├── input_guardrail.py
│   ├── insight_generator.py
│   ├── llm_output_guardrail.py
│   ├── openrouter_client.py
│   ├── patient_agent.py
│   ├── query_engine.py
│   ├── response_formatter.py
│   ├── schema_manager.py
│   ├── sql_generator.py
│   └── sql_validator.py
│
├── analytics_engine/           # KPI and business analytics
│   ├── business_rules.py
│   └── kpi_engine.py
│
├── assets/                     # Screenshots and visual assets
│
├── configs/                    # Configurable project thresholds
│   └── business_thresholds.py
│
├── dashboard/                  # Streamlit application
│   ├── Home.py
│   ├── components.py
│   ├── styles.py
│   ├── theme.py
│   ├── utils.py
│   └── pages/
│       ├── 1_Executive_Dashboard.py
│       ├── 2_Operations.py
│       ├── 3_Finance.py
│       ├── 4_Advanced_Analytics.py
│       └── 5_AI_Copilot.py
│
├── data/                       # Data at different processing stages
│   ├── raw/
│   ├── processed/
│   ├── feature_store/
│   ├── warehouse/
│   └── gold/
│
├── database/                   # Database creation and execution
│   ├── connection.py
│   ├── create_database.py
│   ├── executor.py
│   └── schema.py
│
├── docs/                       # Technical and user documentation
│
├── etl/                        # ETL and analytical data preparation
│   ├── build_star_schema.py
│   ├── feature_engineering_v1.py
│   ├── gold_layer.py
│   └── semantic_layer.py
│
├── metadata/                   # Semantic and analytical metadata
│   ├── datasets/
│   ├── schema.json
│   ├── relationships.json
│   ├── calculated_metrics.json
│   ├── business_rules.json
│   ├── glossary.json
│   ├── kpis.json
│   ├── prompt_rules.json
│   ├── query_templates.json
│   ├── synonym_dictionary.json
│   └── ...
│
├── mining/                     # Data-mining workflows
│   ├── anomaly_detection.py
│   ├── association_rules.py
│   ├── clustering.py
│   ├── data_loader.py
│   ├── sequential_patterns.py
│   └── timeseries.py
│
├── models/                     # Model-related project resources
├── prompts/                    # LLM prompt definitions
├── tests/                      # Automated test suite
│
├── utils/                      # Shared utilities
│   ├── database_manager.py
│   └── validators.py
│
├── config.py
├── manifest.json
├── requirements.txt
├── LICENSE
└── README.md
```

Local/generated artifacts such as `.env`, `.venv`, `__pycache__`, logs, and the runtime SQLite database are intentionally excluded from version control.

---

# Technology Stack

| Area | Technology |
|---|---|
| Language | Python |
| Dashboard | Streamlit |
| Database | SQLite |
| Database Access | SQLAlchemy |
| Data Processing | Pandas, NumPy |
| Data Mining / ML | scikit-learn, mlxtend |
| Visualization | Plotly |
| AI / LLM | OpenRouter |
| Testing | Pytest |
| Configuration | python-dotenv |
| Reporting | ReportLab |

---

# Running Locally

## 1. Clone the repository

```bash
git clone https://github.com/RandomJainam/MedIntel360.git
cd MedIntel360
```

## 2. Create a virtual environment

```bash
python -m venv .venv
```

## 3. Activate the environment

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### Windows CMD

```cmd
.venv\Scriptsctivate
```

## 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

## 5. Configure environment variables

Create a local `.env` file with the required LLM configuration.

Example:

```env
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_MODEL=your_model_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1/chat/completions
```

**Never commit `.env` or API keys to GitHub.**

## 6. Prepare the analytical data and database

Run the project's data preparation / ETL workflow required for the current project version.

The local SQLite database is generated as part of the runtime/data workflow and is not committed to the repository.

## 7. Launch the dashboard

From the project root:

```bash
python -m streamlit run dashboard/Home.py
```

---

# Testing

The project contains automated tests covering major parts of the system, including:

- Data understanding
- Conversation handling
- Follow-up detection
- SQL generation
- SQL validation
- Database execution and safety
- Insight generation
- Response formatting
- Input guardrails
- LLM output guardrails
- Analytical pipeline behavior
- Schema and metadata behavior

Run the full test suite:

```bash
python -m pytest -v
```

Run a specific test module:

```bash
python -m pytest tests/test_follow_up_detection.py -v
```

---

# Database

MedIntel360 currently uses a local SQLite analytical database.

The runtime database is intentionally excluded from Git version control because it is a generated/local artifact.

The repository contains the components needed to recreate the analytical environment, including:

- data
- ETL workflows
- schema definitions
- metadata
- database creation utilities
- connection and execution layers

This keeps the repository cleaner while allowing the analytical database to be rebuilt locally.

---

# AI Model Configuration

The AI layer uses an LLM backend through OpenRouter.

Model configuration is supplied through environment variables rather than being hard-coded into the application.

The architecture separates AI responsibilities into dedicated components:

- Query understanding
- Conversation management
- SQL generation
- SQL validation
- Insight generation
- Input guardrails
- Output guardrails
- Response formatting

This separation makes the AI pipeline easier to test, debug, and evolve.

---

# Documentation

Additional documentation is maintained in the `docs/` directory.

| Document | Purpose |
|---|---|
| `AI_Copilot.md` | AI analytics workflow |
| `API.md` | API/application documentation |
| `architecture.md` | System architecture |
| `Database.md` | Database architecture |
| `database_schema.md` | Database schema |
| `DataMining.md` | Data-mining workflows |
| `data_flow.md` | Data flow through the platform |
| `Installation.md` | Installation and setup |
| `UserGuide.md` | User-facing guide |

---

# Development Philosophy

MedIntel360 is being developed iteratively.

The architecture has evolved through repeated evaluation of:

- how users naturally formulate analytical questions
- how conversational context should be maintained
- how follow-up queries should be distinguished from new questions
- how LLM-generated SQL should be controlled
- how analytical results should be presented
- how data preparation should remain separated from AI querying
- how the project can eventually become easier to install and distribute

The objective is to build a **usable analytical product**, not simply demonstrate an LLM connected directly to a database.

---

# Roadmap

Areas being explored include:

- More robust conversational and follow-up query handling
- Session-aware analytical history
- Automated PDF report generation
- Improved analytical result presentation
- Expanded data-mining workflows
- Deployment and installation automation
- Reproducible project setup
- Additional validation and testing
- Continued architecture refinement

---

# Disclaimer

MedIntel360 is an educational and software-engineering project focused on healthcare analytics and data intelligence.

It is **not a medical diagnostic system** and should not be used for medical diagnosis, treatment decisions, or clinical decision-making.

---

## Author

**Jainam Gada**

MedIntel360 is an ongoing project built around experimentation, iterative architecture design, analytics engineering, and applied AI.
