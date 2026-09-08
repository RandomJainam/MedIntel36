from ai_engine.sql_generator import SQLGenerator
from ai_engine.sql_validator import SQLValidator
from ai_engine.schema_manager import SchemaManager
from database.executor import DatabaseExecutor


print()
print("=" * 60)
print("SQL PIPELINE — PHASE 4.2")
print("=" * 60)


# ============================================================
# SETUP
# ============================================================

schema = SchemaManager()

generator = SQLGenerator(
    schema_manager=schema
)

validator = SQLValidator(
    schema_manager=schema
)

executor = DatabaseExecutor()


# ============================================================
# TEST INPUT
# ============================================================

class TestUnderstandingResult:

    selected_dataset = "finance"

    metrics = [
        "department_total_revenue"
    ]

    dimensions = [
        "department_name"
    ]

    filters = []


result = TestUnderstandingResult()


# ============================================================
# STEP 1 — SQL GENERATION
# ============================================================

print()
print("STEP 1 — SQL GENERATION")
print("-" * 60)


generation_result = generator.generate(
    result
)


print()
print("Generated SQL:")
print(generation_result.sql)


print()
print("Logical Dataset:")
print(generation_result.dataset)


expected_table = "gold_finance_analytics"


if expected_table in generation_result.sql:

    print()
    print("PASS: Generator resolved physical table correctly.")

else:

    print()
    print("FAIL: Generator did not use physical table.")

    raise SystemExit(1)


if generation_result.dataset == "finance":

    print()
    print("PASS: Logical dataset preserved.")

else:

    print()
    print("FAIL: Logical dataset was changed.")

    raise SystemExit(1)


# ============================================================
# STEP 2 — SQL VALIDATION
# ============================================================

print()
print("STEP 2 — SQL VALIDATION")
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

    raise SystemExit(1)


# ============================================================
# STEP 3 — DATABASE EXECUTION
# ============================================================

print()
print("STEP 3 — DATABASE EXECUTION")
print("-" * 60)


execution_result = executor.execute(
    generation_result.sql
)


print()
print("Execution Result:")
print(execution_result)


if execution_result.success:

    print()
    print("PASS: Validated SQL executed successfully.")

else:

    print()
    print("FAIL: Database execution failed.")
    print(execution_result.error)

    raise SystemExit(1)


# ============================================================
# STEP 4 — RESULT VALIDATION
# ============================================================

print()
print("STEP 4 — RESULT VALIDATION")
print("-" * 60)


if "department_name" in execution_result.columns:

    print()
    print("PASS: Department column returned.")

else:

    print()
    print("FAIL: Department column missing.")

    raise SystemExit(1)


if "department_total_revenue" in execution_result.columns:

    print()
    print("PASS: Revenue column returned.")

else:

    print()
    print("FAIL: Revenue column missing.")

    raise SystemExit(1)


if execution_result.row_count > 0:

    print()
    print(
        "PASS: Database returned "
        f"{execution_result.row_count} row(s)."
    )

else:

    print()
    print("FAIL: No rows returned.")

    raise SystemExit(1)


# ============================================================
# COMPLETE
# ============================================================

print()
print("=" * 60)
print("PHASE 4.2 END-TO-END VALIDATION COMPLETE")
print("=" * 60)

print()
print("PASS: SQL Generator")
print("PASS: Physical Table Resolution")
print("PASS: SQL Validator")
print("PASS: Database Executor")
print("PASS: Result Retrieval")
print()
print("PHASE 4.2 COMPLETE")
print()