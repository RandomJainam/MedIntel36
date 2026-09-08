from ai_engine.schema_manager import SchemaManager
from ai_engine.sql_generator import SQLGenerator

from ai_engine.data_understanding_agent import (
    DataUnderstandingResult
)


schema = SchemaManager()

generator = SQLGenerator(
    schema_manager=schema
)


print()
print("=" * 60)
print("SQL GENERATOR TEST")
print("=" * 60)


result = DataUnderstandingResult(

    query="Show revenue by department",

    intent="Show revenue by department",

    selected_dataset="finance",

    dataset_confidence=1.0,

    metrics=[
        "department_total_revenue"
    ],

    dimensions=[
        "department_name"
    ],

    filters=[],

    requires_clarification=False,

    clarification_question=None
)


print()
print("Understanding Result:")
print(result)


sql_result = generator.generate(
    result
)


print()
print("=" * 60)
print("GENERATED SQL")
print("=" * 60)

print(
    sql_result.sql
)


print()
print("=" * 60)
print("SQL GENERATION RESULT")
print("=" * 60)

print(sql_result)


print()
print("=" * 60)
print("VALIDATION")
print("=" * 60)


expected_sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "AS department_total_revenue "
    "FROM finance "
    "GROUP BY department_name"
)


if sql_result.sql == expected_sql:

    print("PASS: SQL generated correctly.")

else:

    print("FAIL: SQL does not match expected output.")

    print()
    print("Expected:")
    print(expected_sql)

    print()
    print("Actual:")
    print(sql_result.sql)