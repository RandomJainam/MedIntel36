"""
============================================================
MedIntel360
Analytical Pipeline — Phase 4.5

Tests the complete deterministic analytical pipeline:

DataUnderstandingResult
        ↓
SQLGenerator
        ↓
SQLValidator
        ↓
DatabaseExecutor
        ↓
InsightGenerator
        ↓
Mock LLM
        ↓
Final Answer

Author : Jainam Gada
============================================================
"""

from ai_engine.data_understanding_agent import (
    DataUnderstandingResult
)

from ai_engine.schema_manager import (
    SchemaManager
)

from ai_engine.sql_generator import (
    SQLGenerator
)

from ai_engine.sql_validator import (
    SQLValidator
)

from ai_engine.insight_generator import (
    InsightGenerator
)

from database.executor import (
    DatabaseExecutor
)


print()
print("=" * 60)
print("ANALYTICAL PIPELINE — PHASE 4.5")
print("=" * 60)


# ============================================================
# MOCK LLM
# ============================================================

class MockLLM:

    def chat(
        self,
        system_prompt,
        user_prompt,
        temperature=0.1,
        max_tokens=1000
    ):

        return (
            "The query returned department-level "
            "revenue results successfully."
        )


# ============================================================
# INITIALIZE COMPONENTS
# ============================================================

schema = SchemaManager()

generator = SQLGenerator(
    schema
)

validator = SQLValidator(
    schema
)

executor = DatabaseExecutor(
    max_rows=100
)

llm = MockLLM()

insight_generator = InsightGenerator(
    llm
)


# ============================================================
# STEP 1 — DATA UNDERSTANDING RESULT
# ============================================================

print()
print("STEP 1 — DATA UNDERSTANDING RESULT")
print("-" * 60)


understanding_result = DataUnderstandingResult(

    query=(
        "Show total revenue by department."
    ),

    intent="analytical",

    selected_dataset="finance",

    dataset_confidence=1.0,

    metrics=[
        "department_total_revenue"
    ],

    dimensions=[
        "department_name"
    ],

    filters=[],

    group_by=[
        "department_name"
    ],

    sort_by=None,

    limit=None,

    requires_clarification=False,

    clarification_question=None
)


print(
    "Selected Dataset:",
    understanding_result.selected_dataset
)

print(
    "Metrics:",
    understanding_result.metrics
)

print(
    "Dimensions:",
    understanding_result.dimensions
)


if understanding_result.selected_dataset == "finance":

    print()
    print("PASS: Dataset correctly selected.")

else:

    print()
    print("FAIL: Incorrect dataset.")

    raise SystemExit(1)


# ============================================================
# STEP 2 — SQL GENERATION
# ============================================================

print()
print("STEP 2 — SQL GENERATION")
print("-" * 60)


generation_result = generator.generate(
    understanding_result
)


print()
print("Generated SQL:")
print(generation_result.sql)

print()
print(
    "Logical Dataset:",
    generation_result.dataset
)


if (
    generation_result.dataset
    == "finance"
):

    print()
    print("PASS: Logical dataset preserved.")

else:

    print()
    print("FAIL: Logical dataset changed.")

    raise SystemExit(1)


if (
    "gold_finance_analytics"
    in generation_result.sql
):

    print()
    print(
        "PASS: Physical table resolved correctly."
    )

else:

    print()
    print(
        "FAIL: Physical table not resolved."
    )

    raise SystemExit(1)


# ============================================================
# STEP 3 — SQL VALIDATION
# ============================================================

print()
print("STEP 3 — SQL VALIDATION")
print("-" * 60)


validation_result = validator.validate(
    generation_result.sql
)


print()
print("Validation Result:")
print(validation_result)


if validation_result.valid:

    print()
    print("PASS: Generated SQL passed validation.")

else:

    print()
    print("FAIL: Generated SQL failed validation.")

    for error in validation_result.errors:

        print(
            "ERROR:",
            error
        )

    raise SystemExit(1)


# ============================================================
# STEP 4 — DATABASE EXECUTION
# ============================================================

print()
print("STEP 4 — DATABASE EXECUTION")
print("-" * 60)


execution_result = executor.execute(
    generation_result.sql
)


print()
print("Execution Result:")
print(execution_result)


if execution_result.success:

    print()
    print(
        "PASS: Validated SQL executed successfully."
    )

else:

    print()
    print(
        "FAIL: Database execution failed."
    )

    print(
        "ERROR:",
        execution_result.error
    )

    raise SystemExit(1)


# ============================================================
# STEP 5 — RESULT VALIDATION
# ============================================================

print()
print("STEP 5 — RESULT VALIDATION")
print("-" * 60)


if execution_result.row_count > 0:

    print()
    print(
        "PASS: Database returned "
        f"{execution_result.row_count} row(s)."
    )

else:

    print()
    print(
        "FAIL: Database returned no rows."
    )

    raise SystemExit(1)


if "department_name" in execution_result.columns:

    print()
    print(
        "PASS: Department column returned."
    )

else:

    print()
    print(
        "FAIL: Department column missing."
    )

    raise SystemExit(1)


if "department_total_revenue" in execution_result.columns:

    print()
    print(
        "PASS: Revenue column returned."
    )

else:

    print()
    print(
        "FAIL: Revenue column missing."
    )

    raise SystemExit(1)


# ============================================================
# STEP 6 — INSIGHT GENERATION
# ============================================================

print()
print("STEP 6 — INSIGHT GENERATION")
print("-" * 60)


insight_result = insight_generator.generate(

    query=understanding_result.query,

    execution_result=execution_result,

    understanding_result=understanding_result
)


print()
print("Insight Result:")
print(insight_result)


if insight_result.has_data:

    print()
    print(
        "PASS: Insight generator received data."
    )

else:

    print()
    print(
        "FAIL: Insight generator did not detect data."
    )

    raise SystemExit(1)


if insight_result.answer:

    print()
    print(
        "PASS: Natural-language answer generated."
    )

else:

    print()
    print(
        "FAIL: Natural-language answer missing."
    )

    raise SystemExit(1)


if insight_result.error is None:

    print()
    print(
        "PASS: No insight-generation error."
    )

else:

    print()
    print(
        "FAIL:",
        insight_result.error
    )

    raise SystemExit(1)


# ============================================================
# STEP 7 — COMPLETE PIPELINE
# ============================================================

print()
print("=" * 60)
print("PHASE 4.5 VALIDATION COMPLETE")
print("=" * 60)

print()
print("PASS: Data Understanding Result")
print("PASS: SQL Generation")
print("PASS: Physical Table Resolution")
print("PASS: SQL Validation")
print("PASS: Database Execution")
print("PASS: Result Validation")
print("PASS: Insight Generation")
print("PASS: Mock LLM Integration")

print()
print("PHASE 4.5 COMPLETE")
print()