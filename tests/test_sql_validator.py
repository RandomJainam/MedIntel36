from ai_engine.schema_manager import SchemaManager
from ai_engine.sql_validator import SQLValidator


print()
print("=" * 60)
print("SQL VALIDATOR — PHASE 2")
print("=" * 60)


schema = SchemaManager()

validator = SQLValidator(
    schema_manager=schema
)


# ==================================================
# TEST 1
# Valid dataset + valid fields
# ==================================================

sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "GROUP BY department_name"
)

result = validator.validate(sql)

print()
print("TEST 1 — Valid Schema")

print()
print("SQL:")
print(sql)

print()
print("Result:")
print(result)

if result.valid:

    print("PASS: Valid schema accepted.")

else:

    print("FAIL: Valid schema rejected.")


# ==================================================
# TEST 2
# Invalid dataset
# ==================================================

sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "FROM fake_dataset "
    "GROUP BY department_name"
)

result = validator.validate(sql)

print()
print("TEST 2 — Invalid Dataset")

print()
print("SQL:")
print(sql)

print()
print("Result:")
print(result)

if not result.valid:

    print("PASS: Invalid dataset rejected.")

else:

    print("FAIL: Invalid dataset accepted.")


# ==================================================
# TEST 3
# Unknown fields
# ==================================================

sql = (
    "SELECT fake_department, "
    "SUM(fake_metric) "
    "FROM finance "
    "GROUP BY fake_department"
)

result = validator.validate(sql)

print()
print("TEST 3 — Unknown Fields")

print()
print("SQL:")
print(sql)

print()
print("Result:")
print(result)

if not result.valid:

    print("PASS: Unknown fields rejected.")

else:

    print("FAIL: Unknown fields accepted.")


# ==================================================
# TEST 4
# Valid multiple dimensions
# ==================================================

sql = (
    "SELECT department_name, revenue_band, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "GROUP BY department_name, revenue_band"
)

result = validator.validate(sql)

print()
print("TEST 4 — Multiple Dimensions")

print()
print("SQL:")
print(sql)

print()
print("Result:")
print(result)

if result.valid:

    print("PASS: Multiple dimensions accepted.")

else:

    print("FAIL: Multiple dimensions rejected.")


print()
print("=" * 60)
print("PHASE 2 VALIDATION COMPLETE")
print("=" * 60)

# ==================================================
# TEST 5
# Dimension missing from GROUP BY
# ==================================================

sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "FROM finance"
)

result = validator.validate(sql)

print()
print("TEST 5 — Missing GROUP BY")

print()
print("SQL:")
print(sql)

print()
print("Result:")
print(result)


if not result.valid:

    print("PASS: Missing GROUP BY rejected.")

else:

    print("FAIL: Missing GROUP BY accepted.")


# ==================================================
# TEST 6
# Wrong GROUP BY dimension
# ==================================================

sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "GROUP BY revenue_band"
)

result = validator.validate(sql)

print()
print("TEST 6 — Wrong GROUP BY")

print()
print("SQL:")
print(sql)

print()
print("Result:")
print(result)


if not result.valid:

    print("PASS: Wrong GROUP BY rejected.")

else:

    print("FAIL: Wrong GROUP BY accepted.")

# ==================================================
# TEST 7
# Correct multiple dimensions
# ==================================================

sql = (
    "SELECT department_name, revenue_band, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "GROUP BY department_name, revenue_band"
)

result = validator.validate(sql)

print()
print("TEST 7 — Correct Multiple Dimensions")

print()
print("SQL:")
print(sql)

print()
print("Result:")
print(result)


if result.valid:

    print("PASS: Correct multiple dimensions accepted.")

else:

    print("FAIL: Correct multiple dimensions rejected.")

# ==================================================
# TEST 8
# Valid WHERE filter
# ==================================================

sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "WHERE department_name = 'Cardiology' "
    "GROUP BY department_name"
)

result = validator.validate(sql)

print()
print("TEST 8 — Valid WHERE Filter")

print()
print("SQL:")
print(sql)

print()
print("Result:")
print(result)


if result.valid:

    print("PASS: Valid WHERE filter accepted.")

else:

    print("FAIL: Valid WHERE filter rejected.")

# ==================================================
# TEST 9
# Invalid WHERE field
# ==================================================

sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "WHERE fake_department = 'Cardiology' "
    "GROUP BY department_name"
)

result = validator.validate(sql)

print()
print("TEST 9 — Invalid WHERE Field")

print()
print("SQL:")
print(sql)

print()
print("Result:")
print(result)


if not result.valid:

    print("PASS: Invalid WHERE field rejected.")

else:

    print("FAIL: Invalid WHERE field accepted.")

# ==================================================
# TEST 10
# Empty WHERE value
# ==================================================

sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "WHERE department_name = "
    "GROUP BY department_name"
)

result = validator.validate(sql)

print()
print("TEST 10 — Empty WHERE Value")

print()
print("SQL:")
print(sql)

print()
print("Result:")
print(result)


if not result.valid:

    print("PASS: Empty WHERE value rejected.")

else:

    print("FAIL: Empty WHERE value accepted.")

# ==================================================
# TEST 11
# Multiple WHERE filters
# ==================================================

sql = (
    "SELECT department_name, revenue_band, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "WHERE department_name = 'Cardiology' "
    "AND revenue_band = 'High' "
    "GROUP BY department_name, revenue_band"
)

result = validator.validate(sql)

print()
print("TEST 11 — Multiple WHERE Filters")

print()
print("SQL:")
print(sql)

print()
print("Result:")
print(result)


if result.valid:

    print("PASS: Multiple WHERE filters accepted.")

else:

    print("FAIL: Multiple WHERE filters rejected.")

print()
print("=" * 60)
print("PHASE 3.1 — AGGREGATION VALIDATION")
print("=" * 60)


# --------------------------------------------------
# TEST 12 — Valid SUM
# --------------------------------------------------

sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "GROUP BY department_name"
)

result = validator.validate(sql)

print()
print("TEST 12 — Valid SUM")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if result.valid:
    print("PASS: Valid SUM accepted.")
else:
    print("FAIL: Valid SUM rejected.")


# --------------------------------------------------
# TEST 13 — Valid AVG
# --------------------------------------------------

sql = (
    "SELECT department_name, "
    "AVG(average_revenue) "
    "FROM finance "
    "GROUP BY department_name"
)

result = validator.validate(sql)

print()
print("TEST 13 — Valid AVG")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if result.valid:
    print("PASS: Valid AVG accepted.")
else:
    print("FAIL: Valid AVG rejected.")


# --------------------------------------------------
# TEST 14 — Unknown metric inside aggregation
# --------------------------------------------------

sql = (
    "SELECT department_name, "
    "SUM(fake_metric) "
    "FROM finance "
    "GROUP BY department_name"
)

result = validator.validate(sql)

print()
print("TEST 14 — Unknown Metric")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if not result.valid:
    print("PASS: Unknown metric rejected.")
else:
    print("FAIL: Unknown metric accepted.")


# --------------------------------------------------
# TEST 15 — Multiple valid aggregations
# --------------------------------------------------

sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue), "
    "AVG(average_revenue) "
    "FROM finance "
    "GROUP BY department_name"
)

result = validator.validate(sql)

print()
print("TEST 15 — Multiple Aggregations")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if result.valid:
    print("PASS: Multiple valid aggregations accepted.")
else:
    print("FAIL: Multiple valid aggregations rejected.")


print()
print("=" * 60)
print("PHASE 3.1 VALIDATION COMPLETE")
print("=" * 60)

# --------------------------------------------------
# TEST 16 — Aggregation on dimension
# --------------------------------------------------

sql = (
    "SELECT department_name, "
    "SUM(department_name) "
    "FROM finance "
    "GROUP BY department_name"
)

result = validator.validate(sql)

print()
print("TEST 16 — Aggregation on Dimension")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if not result.valid:
    print("PASS: Aggregation on dimension rejected.")
else:
    print("FAIL: Aggregation on dimension accepted.")


# --------------------------------------------------
# TEST 17 — COUNT on valid metric
# --------------------------------------------------

sql = (
    "SELECT department_name, "
    "COUNT(department_total_revenue) "
    "FROM finance "
    "GROUP BY department_name"
)

result = validator.validate(sql)

print()
print("TEST 17 — COUNT on Valid Metric")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if result.valid:
    print("PASS: COUNT on valid metric accepted.")
else:
    print("FAIL: COUNT on valid metric rejected.")


# --------------------------------------------------
# TEST 18 — MIN on valid metric
# --------------------------------------------------

sql = (
    "SELECT department_name, "
    "MIN(department_total_revenue) "
    "FROM finance "
    "GROUP BY department_name"
)

result = validator.validate(sql)

print()
print("TEST 18 — MIN on Valid Metric")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if result.valid:
    print("PASS: MIN on valid metric accepted.")
else:
    print("FAIL: MIN on valid metric rejected.")


# --------------------------------------------------
# TEST 19 — MAX on valid metric
# --------------------------------------------------

sql = (
    "SELECT department_name, "
    "MAX(department_total_revenue) "
    "FROM finance "
    "GROUP BY department_name"
)

result = validator.validate(sql)

print()
print("TEST 19 — MAX on Valid Metric")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if result.valid:
    print("PASS: MAX on valid metric accepted.")
else:
    print("FAIL: MAX on valid metric rejected.")


print()
print("=" * 60)
print("PHASE 3.2 VALIDATION COMPLETE")
print("=" * 60)

print()
print("=" * 60)
print("PHASE 3.3 — SELECT EXPRESSION VALIDATION")
print("=" * 60)


# --------------------------------------------------
# TEST 20 — Valid dimension in SELECT
# --------------------------------------------------

sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "GROUP BY department_name"
)

result = validator.validate(sql)

print()
print("TEST 20 — Valid SELECT Expressions")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if result.valid:
    print("PASS: Valid SELECT expressions accepted.")
else:
    print("FAIL: Valid SELECT expressions rejected.")


# --------------------------------------------------
# TEST 21 — Unknown SELECT field
# --------------------------------------------------

sql = (
    "SELECT fake_department, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "GROUP BY fake_department"
)

result = validator.validate(sql)

print()
print("TEST 21 — Unknown SELECT Field")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if not result.valid:
    print("PASS: Unknown SELECT field rejected.")
else:
    print("FAIL: Unknown SELECT field accepted.")


# --------------------------------------------------
# TEST 22 — Arbitrary SELECT expression
# --------------------------------------------------

sql = (
    "SELECT department_name + 1, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "GROUP BY department_name"
)

result = validator.validate(sql)

print()
print("TEST 22 — Arbitrary SELECT Expression")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if not result.valid:
    print("PASS: Arbitrary SELECT expression rejected.")
else:
    print("FAIL: Arbitrary SELECT expression accepted.")


# --------------------------------------------------
# TEST 23 — Valid metric alias
# --------------------------------------------------

sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "AS total_revenue "
    "FROM finance "
    "GROUP BY department_name"
)

result = validator.validate(sql)

print()
print("TEST 23 — Valid Metric Alias")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if result.valid:
    print("PASS: Valid metric alias accepted.")
else:
    print("FAIL: Valid metric alias rejected.")


print()
print("=" * 60)
print("PHASE 3.3 VALIDATION COMPLETE")
print("=" * 60)

print()
print("=" * 60)
print("PHASE 3.4 — WHERE OPERATOR VALIDATION")
print("=" * 60)


# --------------------------------------------------
# TEST 24 — Equality operator
# --------------------------------------------------

sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "WHERE department_name = 'Cardiology' "
    "GROUP BY department_name"
)

result = validator.validate(sql)

print()
print("TEST 24 — Equality Operator")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if result.valid:
    print("PASS: Equality operator accepted.")
else:
    print("FAIL: Equality operator rejected.")


# --------------------------------------------------
# TEST 25 — Greater than operator
# --------------------------------------------------

sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "WHERE department_total_revenue > 100000 "
    "GROUP BY department_name"
)

result = validator.validate(sql)

print()
print("TEST 25 — Greater Than Operator")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if result.valid:
    print("PASS: Greater than operator accepted.")
else:
    print("FAIL: Greater than operator rejected.")


# --------------------------------------------------
# TEST 26 — Greater than or equal
# --------------------------------------------------

sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "WHERE department_total_revenue >= 100000 "
    "GROUP BY department_name"
)

result = validator.validate(sql)

print()
print("TEST 26 — Greater Than or Equal")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if result.valid:
    print("PASS: >= operator accepted.")
else:
    print("FAIL: >= operator rejected.")


# --------------------------------------------------
# TEST 27 — Missing operator/value
# --------------------------------------------------

sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "WHERE department_name "
    "GROUP BY department_name"
)

result = validator.validate(sql)

print()
print("TEST 27 — Missing WHERE Operator")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if not result.valid:
    print("PASS: Malformed WHERE condition rejected.")
else:
    print("FAIL: Malformed WHERE condition accepted.")


# --------------------------------------------------
# TEST 28 — Empty WHERE value
# --------------------------------------------------

sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "WHERE department_name = "
    "GROUP BY department_name"
)

result = validator.validate(sql)

print()
print("TEST 28 — Empty WHERE Value")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if not result.valid:
    print("PASS: Empty WHERE value rejected.")
else:
    print("FAIL: Empty WHERE value accepted.")


# --------------------------------------------------
# TEST 29 — Multiple valid operators
# --------------------------------------------------

sql = (
    "SELECT department_name, revenue_band, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "WHERE department_name = 'Cardiology' "
    "AND revenue_band != 'Low' "
    "GROUP BY department_name, revenue_band"
)

result = validator.validate(sql)

print()
print("TEST 29 — Multiple WHERE Operators")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if result.valid:
    print("PASS: Multiple WHERE operators accepted.")
else:
    print("FAIL: Multiple WHERE operators rejected.")


print()
print("=" * 60)
print("PHASE 3.4 VALIDATION COMPLETE")
print("=" * 60)

print()
print("=" * 60)
print("PHASE 3.5 — HAVING VALIDATION")
print("=" * 60)


# --------------------------------------------------
# TEST 30 — Valid HAVING
# --------------------------------------------------

sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "GROUP BY department_name "
    "HAVING SUM(department_total_revenue) > 100000"
)

result = validator.validate(sql)

print()
print("TEST 30 — Valid HAVING")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if result.valid:
    print("PASS: Valid HAVING accepted.")
else:
    print("FAIL: Valid HAVING rejected.")


# --------------------------------------------------
# TEST 31 — HAVING >=
# --------------------------------------------------

sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "GROUP BY department_name "
    "HAVING SUM(department_total_revenue) >= 100000"
)

result = validator.validate(sql)

print()
print("TEST 31 — HAVING Greater Than or Equal")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if result.valid:
    print("PASS: HAVING >= accepted.")
else:
    print("FAIL: HAVING >= rejected.")


# --------------------------------------------------
# TEST 32 — Unknown metric
# --------------------------------------------------

sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "GROUP BY department_name "
    "HAVING SUM(fake_metric) > 100000"
)

result = validator.validate(sql)

print()
print("TEST 32 — Unknown HAVING Metric")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if not result.valid:
    print("PASS: Unknown HAVING metric rejected.")
else:
    print("FAIL: Unknown HAVING metric accepted.")


# --------------------------------------------------
# TEST 33 — Dimension inside HAVING aggregation
# --------------------------------------------------

sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "GROUP BY department_name "
    "HAVING SUM(department_name) > 100000"
)

result = validator.validate(sql)

print()
print("TEST 33 — Dimension in HAVING")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if not result.valid:
    print("PASS: Dimension aggregation in HAVING rejected.")
else:
    print("FAIL: Dimension aggregation in HAVING accepted.")


# --------------------------------------------------
# TEST 34 — Missing HAVING condition
# --------------------------------------------------

sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "GROUP BY department_name "
    "HAVING SUM(department_total_revenue)"
)

result = validator.validate(sql)

print()
print("TEST 34 — Invalid HAVING Condition")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if not result.valid:
    print("PASS: Invalid HAVING condition rejected.")
else:
    print("FAIL: Invalid HAVING condition accepted.")


# --------------------------------------------------
# TEST 35 — Multiple HAVING conditions
# --------------------------------------------------

sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue), "
    "AVG(average_revenue) "
    "FROM finance "
    "GROUP BY department_name "
    "HAVING SUM(department_total_revenue) > 100000 "
    "AND AVG(average_revenue) >= 50000"
)

result = validator.validate(sql)

print()
print("TEST 35 — Multiple HAVING Conditions")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if result.valid:
    print("PASS: Multiple HAVING conditions accepted.")
else:
    print("FAIL: Multiple HAVING conditions rejected.")


print()
print("=" * 60)
print("PHASE 3.5 VALIDATION COMPLETE")
print("=" * 60)

print()
print("=" * 60)
print("PHASE 3.6 — ORDER BY VALIDATION")
print("=" * 60)


# --------------------------------------------------
# TEST 36 — ORDER BY dimension ASC
# --------------------------------------------------

sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "GROUP BY department_name "
    "ORDER BY department_name ASC"
)

result = validator.validate(sql)

print()
print("TEST 36 — ORDER BY Dimension ASC")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if result.valid:
    print("PASS: ORDER BY dimension ASC accepted.")
else:
    print("FAIL: ORDER BY dimension ASC rejected.")


# --------------------------------------------------
# TEST 37 — ORDER BY dimension DESC
# --------------------------------------------------

sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "GROUP BY department_name "
    "ORDER BY department_name DESC"
)

result = validator.validate(sql)

print()
print("TEST 37 — ORDER BY Dimension DESC")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if result.valid:
    print("PASS: ORDER BY dimension DESC accepted.")
else:
    print("FAIL: ORDER BY dimension DESC rejected.")


# --------------------------------------------------
# TEST 38 — ORDER BY metric DESC
# --------------------------------------------------

sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "GROUP BY department_name "
    "ORDER BY department_total_revenue DESC"
)

result = validator.validate(sql)

print()
print("TEST 38 — ORDER BY Metric DESC")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if result.valid:
    print("PASS: ORDER BY metric DESC accepted.")
else:
    print("FAIL: ORDER BY metric DESC rejected.")


# --------------------------------------------------
# TEST 39 — Unknown ORDER BY field
# --------------------------------------------------

sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "GROUP BY department_name "
    "ORDER BY fake_column DESC"
)

result = validator.validate(sql)

print()
print("TEST 39 — Unknown ORDER BY Field")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if not result.valid:
    print("PASS: Unknown ORDER BY field rejected.")
else:
    print("FAIL: Unknown ORDER BY field accepted.")


# --------------------------------------------------
# TEST 40 — Invalid direction
# --------------------------------------------------

sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "GROUP BY department_name "
    "ORDER BY department_name SIDEWAYS"
)

result = validator.validate(sql)

print()
print("TEST 40 — Invalid ORDER BY Direction")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if not result.valid:
    print("PASS: Invalid ORDER BY direction rejected.")
else:
    print("FAIL: Invalid ORDER BY direction accepted.")


# --------------------------------------------------
# TEST 41 — Empty ORDER BY
# --------------------------------------------------

sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "GROUP BY department_name "
    "ORDER BY"
)

result = validator.validate(sql)

print()
print("TEST 41 — Empty ORDER BY")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if not result.valid:
    print("PASS: Empty ORDER BY rejected.")
else:
    print("FAIL: Empty ORDER BY accepted.")


# --------------------------------------------------
# TEST 42 — Multiple ORDER BY fields
# --------------------------------------------------

sql = (
    "SELECT department_name, revenue_band, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "GROUP BY department_name, revenue_band "
    "ORDER BY department_name ASC, revenue_band DESC"
)

result = validator.validate(sql)

print()
print("TEST 42 — Multiple ORDER BY Fields")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if result.valid:
    print("PASS: Multiple ORDER BY fields accepted.")
else:
    print("FAIL: Multiple ORDER BY fields rejected.")


print()
print("=" * 60)
print("PHASE 3.6 VALIDATION COMPLETE")
print("=" * 60)

print()
print("=" * 60)
print("PHASE 3.7 — LIMIT VALIDATION")
print("=" * 60)


# --------------------------------------------------
# TEST 43 — Valid LIMIT
# --------------------------------------------------

sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "GROUP BY department_name "
    "LIMIT 10"
)

result = validator.validate(sql)

print()
print("TEST 43 — Valid LIMIT")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if result.valid:
    print("PASS: Valid LIMIT accepted.")
else:
    print("FAIL: Valid LIMIT rejected.")


# --------------------------------------------------
# TEST 44 — LIMIT 1
# --------------------------------------------------

sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "GROUP BY department_name "
    "LIMIT 1"
)

result = validator.validate(sql)

print()
print("TEST 44 — LIMIT 1")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if result.valid:
    print("PASS: LIMIT 1 accepted.")
else:
    print("FAIL: LIMIT 1 rejected.")


# --------------------------------------------------
# TEST 45 — Zero LIMIT
# --------------------------------------------------

sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "GROUP BY department_name "
    "LIMIT 0"
)

result = validator.validate(sql)

print()
print("TEST 45 — Zero LIMIT")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if not result.valid:
    print("PASS: LIMIT 0 rejected.")
else:
    print("FAIL: LIMIT 0 accepted.")


# --------------------------------------------------
# TEST 46 — Negative LIMIT
# --------------------------------------------------

sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "GROUP BY department_name "
    "LIMIT -1"
)

result = validator.validate(sql)

print()
print("TEST 46 — Negative LIMIT")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if not result.valid:
    print("PASS: Negative LIMIT rejected.")
else:
    print("FAIL: Negative LIMIT accepted.")


# --------------------------------------------------
# TEST 47 — Non-numeric LIMIT
# --------------------------------------------------

sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "GROUP BY department_name "
    "LIMIT abc"
)

result = validator.validate(sql)

print()
print("TEST 47 — Non-Numeric LIMIT")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if not result.valid:
    print("PASS: Non-numeric LIMIT rejected.")
else:
    print("FAIL: Non-numeric LIMIT accepted.")


# --------------------------------------------------
# TEST 48 — Empty LIMIT
# --------------------------------------------------

sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "GROUP BY department_name "
    "LIMIT"
)

result = validator.validate(sql)

print()
print("TEST 48 — Empty LIMIT")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if not result.valid:
    print("PASS: Empty LIMIT rejected.")
else:
    print("FAIL: Empty LIMIT accepted.")


# --------------------------------------------------
# TEST 49 — Full clause chain
# --------------------------------------------------

sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "WHERE department_name = 'Cardiology' "
    "GROUP BY department_name "
    "HAVING SUM(department_total_revenue) > 100000 "
    "ORDER BY department_total_revenue DESC "
    "LIMIT 10"
)

result = validator.validate(sql)

print()
print("TEST 49 — Full SQL Clause Chain")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if result.valid:
    print("PASS: Full clause chain accepted.")
else:
    print("FAIL: Full clause chain rejected.")


print()
print("=" * 60)
print("PHASE 3.7 VALIDATION COMPLETE")
print("=" * 60)

print()
print("=" * 60)
print("PHASE 3.8 — SQL SECURITY HARDENING")
print("=" * 60)


# --------------------------------------------------
# TEST 50 — Multiple statements
# --------------------------------------------------

sql = (
    "SELECT department_name "
    "FROM finance; "
    "DELETE FROM finance"
)

result = validator.validate(sql)

print()
print("TEST 50 — Multiple SQL Statements")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if not result.valid:
    print("PASS: Multiple statements rejected.")
else:
    print("FAIL: Multiple statements accepted.")


# --------------------------------------------------
# TEST 51 — Line comment
# --------------------------------------------------

sql = (
    "SELECT department_name "
    "FROM finance -- comment"
)

result = validator.validate(sql)

print()
print("TEST 51 — SQL Line Comment")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if not result.valid:
    print("PASS: SQL line comment rejected.")
else:
    print("FAIL: SQL line comment accepted.")


# --------------------------------------------------
# TEST 52 — Block comment
# --------------------------------------------------

sql = (
    "SELECT department_name "
    "FROM finance /* comment */"
)

result = validator.validate(sql)

print()
print("TEST 52 — SQL Block Comment")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if not result.valid:
    print("PASS: SQL block comment rejected.")
else:
    print("FAIL: SQL block comment accepted.")


# --------------------------------------------------
# TEST 53 — INSERT
# --------------------------------------------------

sql = (
    "INSERT INTO finance "
    "(department_name) VALUES ('Cardiology')"
)

result = validator.validate(sql)

print()
print("TEST 53 — INSERT")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if not result.valid:
    print("PASS: INSERT rejected.")
else:
    print("FAIL: INSERT accepted.")


# --------------------------------------------------
# TEST 54 — UPDATE
# --------------------------------------------------

sql = (
    "UPDATE finance "
    "SET department_name = 'Cardiology'"
)

result = validator.validate(sql)

print()
print("TEST 54 — UPDATE")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if not result.valid:
    print("PASS: UPDATE rejected.")
else:
    print("FAIL: UPDATE accepted.")


# --------------------------------------------------
# TEST 55 — TRUNCATE
# --------------------------------------------------

sql = "TRUNCATE TABLE finance"

result = validator.validate(sql)

print()
print("TEST 55 — TRUNCATE")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if not result.valid:
    print("PASS: TRUNCATE rejected.")
else:
    print("FAIL: TRUNCATE accepted.")


# --------------------------------------------------
# TEST 56 — EXECUTE
# --------------------------------------------------

sql = (
    "SELECT EXECUTE('dangerous_command') "
    "FROM finance"
)

result = validator.validate(sql)

print()
print("TEST 56 — EXECUTE"
)
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if not result.valid:
    print("PASS: EXECUTE rejected.")
else:
    print("FAIL: EXECUTE accepted.")


# --------------------------------------------------
# TEST 57 — Valid SELECT still works
# --------------------------------------------------

sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "FROM finance "
    "GROUP BY department_name"
)

result = validator.validate(sql)

print()
print("TEST 57 — Valid SELECT After Hardening")
print()
print("SQL:")
print(sql)
print()
print("Result:")
print(result)

if result.valid:
    print("PASS: Valid SELECT still accepted.")
else:
    print("FAIL: Valid SELECT rejected.")


print()
print("=" * 60)
print("PHASE 3.8 VALIDATION COMPLETE")
print("=" * 60)