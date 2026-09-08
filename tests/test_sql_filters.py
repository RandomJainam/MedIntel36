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
print("SQL FILTER TEST")
print("=" * 60)


result = DataUnderstandingResult(

    query=(
        "Show revenue by department "
        "for Cardiology"
    ),

    intent=(
        "Show revenue by department "
        "for Cardiology"
    ),

    selected_dataset="finance",

    dataset_confidence=1.0,

    metrics=[
        "department_total_revenue"
    ],

    dimensions=[
        "department_name"
    ],

    filters=[
        {
            "dimension": "department_name",
            "operator": "=",
            "value": "Cardiology"
        }
    ],

    requires_clarification=False,

    clarification_question=None
)


sql_result = generator.generate(
    result
)


print()
print("Generated SQL:")
print(sql_result.sql)


expected_sql = (
    "SELECT department_name, "
    "SUM(department_total_revenue) "
    "AS department_total_revenue "
    "FROM finance "
    "WHERE department_name = 'Cardiology' "
    "GROUP BY department_name"
)


print()
print("Expected SQL:")
print(expected_sql)


print()
print("=" * 60)
print("VALIDATION")
print("=" * 60)


if sql_result.sql == expected_sql:

    print(
        "PASS: Filter SQL generated correctly."
    )

else:

    print(
        "FAIL: Generated SQL does not match "
        "expected SQL."
    )