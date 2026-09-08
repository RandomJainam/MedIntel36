from database.executor import DatabaseExecutor


print()
print("=" * 60)
print("DATABASE EXECUTOR — PHASE 4.1")
print("=" * 60)


executor = DatabaseExecutor()


# ==================================================
# TEST 1 — Valid SELECT
# ==================================================

sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "AS department_total_revenue "
    "FROM gold_finance_analytics "
    "GROUP BY department_name "
    "LIMIT 5"
)

result = executor.execute(sql)


print()
print("TEST 1 — Valid SELECT")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)


if result.success:

    print("PASS: SELECT executed successfully.")

else:

    print("FAIL:", result.error)


# ==================================================
# TEST 2 — Empty SQL
# ==================================================

sql = ""

result = executor.execute(sql)


print()
print("TEST 2 — Empty SQL")
print()
print("Result:")
print(result)


if not result.success:

    print("PASS: Empty SQL rejected.")

else:

    print("FAIL: Empty SQL accepted.")


# ==================================================
# TEST 3 — DELETE
# ==================================================

sql = "DELETE FROM finance"

result = executor.execute(sql)


print()
print("TEST 3 — DELETE")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)


if not result.success:

    print("PASS: DELETE rejected.")

else:

    print("FAIL: DELETE accepted.")


# ==================================================
# TEST 4 — UPDATE
# ==================================================

sql = (
    "UPDATE finance "
    "SET department_name = 'Cardiology'"
)

result = executor.execute(sql)


print()
print("TEST 4 — UPDATE")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)


if not result.success:

    print("PASS: UPDATE rejected.")

else:

    print("FAIL: UPDATE accepted.")


# ==================================================
# TEST 5 — Invalid SQL
# ==================================================

sql = (
   "SELECT fake_column "
"FROM gold_finance_analytics"
)

result = executor.execute(sql)


print()
print("TEST 5 — Invalid SQL")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)


if not result.success:

    print("PASS: Database error captured.")

else:

    print("FAIL: Invalid SQL unexpectedly succeeded.")


# ==================================================
# COMPLETE
# ==================================================

print()
print("=" * 60)
print("PHASE 4.1 VALIDATION COMPLETE")
print("=" * 60)