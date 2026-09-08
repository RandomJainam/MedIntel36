from database.executor import DatabaseExecutor


print()
print("=" * 60)
print("DATABASE EXECUTOR — PHASE 4.3")
print("=" * 60)


# ============================================================
# TEST 1 — Normal Result
# ============================================================

print()
print("TEST 1 — Normal Result")
print()


executor = DatabaseExecutor(
    max_rows=10
)


sql = (
    "SELECT department_name, "
    "department_total_revenue "
    "FROM gold_finance_analytics "
    "LIMIT 5"
)


result = executor.execute(
    sql
)


print("SQL:")
print(sql)

print()
print("Result:")
print(result)


if result.success:

    print()
    print("PASS: Normal query executed.")

else:

    print()
    print("FAIL:", result.error)

    raise SystemExit(1)


if result.row_count <= 10:

    print()
    print("PASS: Result is within row limit.")

else:

    print()
    print("FAIL: Result exceeded row limit.")

    raise SystemExit(1)


if not result.truncated:

    print()
    print("PASS: Result correctly marked as not truncated.")

else:

    print()
    print("FAIL: Result incorrectly marked as truncated.")

    raise SystemExit(1)


# ============================================================
# TEST 2 — Result Truncation
# ============================================================

print()
print("TEST 2 — Result Truncation")
print()


executor = DatabaseExecutor(
    max_rows=3
)


sql = (
    "SELECT department_name, "
    "department_total_revenue "
    "FROM gold_finance_analytics"
)


result = executor.execute(
    sql
)


print("SQL:")
print(sql)

print()
print("Result:")
print(result)


if result.success:

    print()
    print("PASS: Large query executed.")

else:

    print()
    print("FAIL:", result.error)

    raise SystemExit(1)


if result.row_count == 3:

    print()
    print("PASS: Result limited to 3 rows.")

else:

    print()
    print(
        "FAIL: Expected 3 rows, got "
        f"{result.row_count}."
    )

    raise SystemExit(1)


if result.truncated:

    print()
    print("PASS: Result correctly marked as truncated.")

else:

    print()
    print("FAIL: Result was not marked as truncated.")

    raise SystemExit(1)


# ============================================================
# TEST 3 — Invalid max_rows
# ============================================================

print()
print("TEST 3 — Invalid max_rows")
print()


try:

    DatabaseExecutor(
        max_rows=0
    )

    print()
    print("FAIL: Zero max_rows was accepted.")

    raise SystemExit(1)

except ValueError:

    print()
    print("PASS: Zero max_rows rejected.")


# ============================================================
# TEST 4 — Empty SQL
# ============================================================

print()
print("TEST 4 — Empty SQL")
print()


executor = DatabaseExecutor(
    max_rows=10
)


result = executor.execute(
    ""
)


print("Result:")
print(result)


if not result.success:

    print()
    print("PASS: Empty SQL rejected.")

else:

    print()
    print("FAIL: Empty SQL accepted.")

    raise SystemExit(1)


# ============================================================
# TEST 5 — Non-SELECT
# ============================================================

print()
print("TEST 5 — DELETE")
print()


result = executor.execute(
    "DELETE FROM gold_finance_analytics"
)


print("Result:")
print(result)


if not result.success:

    print()
    print("PASS: DELETE rejected.")

else:

    print()
    print("FAIL: DELETE was accepted.")

    raise SystemExit(1)


# ============================================================
# COMPLETE
# ============================================================

print()
print("=" * 60)
print("PHASE 4.3 VALIDATION COMPLETE")
print("=" * 60)

print()
print("PASS: Normal result handling")
print("PASS: Result size protection")
print("PASS: Truncation detection")
print("PASS: Invalid configuration rejection")
print("PASS: Empty SQL protection")
print("PASS: SELECT-only protection")
print()
print("PHASE 4.3 COMPLETE")
print()