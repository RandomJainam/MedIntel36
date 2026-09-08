"""
============================================================
MedIntel360
Real Insight Generation — Phase 4.6

Tests the real OpenRouter LLM through InsightGenerator.

Pipeline:

DatabaseExecutionResult
        ↓
InsightGenerator
        ↓
OpenRouterClient
        ↓
Real LLM
        ↓
Natural-language answer

Author : Jainam Gada
============================================================
"""

from ai_engine.insight_generator import (
    InsightGenerator
)

from ai_engine.openrouter_client import (
    OpenRouterClient
)

from database.executor import (
    DatabaseExecutor
)


print()
print("=" * 60)
print("REAL INSIGHT GENERATION — PHASE 4.6")
print("=" * 60)


# ============================================================
# STEP 1 — INITIALIZE REAL LLM
# ============================================================

print()
print("STEP 1 — INITIALIZING OPENROUTER")
print("-" * 60)


llm = OpenRouterClient()

print()
print("PASS: OpenRouter configuration loaded.")


# ============================================================
# STEP 2 — EXECUTE REAL DATABASE QUERY
# ============================================================

print()
print("STEP 2 — DATABASE QUERY")
print("-" * 60)


executor = DatabaseExecutor(
    max_rows=100
)


sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "AS department_total_revenue "
    "FROM gold_finance_analytics "
    "GROUP BY department_name"
)


execution_result = executor.execute(
    sql
)


print()
print("SQL:")
print(sql)

print()
print("Execution Result:")
print(execution_result)


if execution_result.success:

    print()
    print("PASS: Database query executed.")

else:

    print()
    print(
        "FAIL: Database query failed."
    )

    print(
        "ERROR:",
        execution_result.error
    )

    raise SystemExit(1)


# ============================================================
# STEP 3 — REAL INSIGHT GENERATION
# ============================================================

print()
print("STEP 3 — REAL INSIGHT GENERATION")
print("-" * 60)


generator = InsightGenerator(
    llm
)


query = (
    "Which department has the highest "
    "total revenue?"
)


result = generator.generate(

    query=query,

    execution_result=execution_result
)


print()
print("Insight Result:")
print(result)


# ============================================================
# STEP 4 — VALIDATE RESPONSE
# ============================================================

print()
print("STEP 4 — RESPONSE VALIDATION")
print("-" * 60)


if result.error is not None:

    print()
    print(
        "FAIL: Insight generation failed."
    )

    print(
        "ERROR:",
        result.error
    )

    raise SystemExit(1)


if not result.answer:

    print()
    print(
        "FAIL: Model returned an empty answer."
    )

    raise SystemExit(1)


print()
print("PASS: Real LLM returned an answer.")


print()
print("ANSWER:")
print(result.answer)


# ============================================================
# COMPLETE
# ============================================================

print()
print("=" * 60)
print("PHASE 4.6 VALIDATION COMPLETE")
print("=" * 60)

print()
print("PASS: OpenRouter configuration")
print("PASS: Database execution")
print("PASS: Real LLM invocation")
print("PASS: Insight generation")
print("PASS: Natural-language response")
print()
print("PHASE 4.6 COMPLETE")
print()