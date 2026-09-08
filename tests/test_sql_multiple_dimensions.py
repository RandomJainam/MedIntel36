from ai_engine.sql_generator import SQLGenerator
from ai_engine.data_understanding_agent import DataUnderstandingResult
from ai_engine.schema_manager import SchemaManager


print()
print("=" * 60)
print("SQL MULTIPLE DIMENSION TEST")
print("=" * 60)


result = DataUnderstandingResult(
    query="Show revenue by department and revenue band",

    intent="Show revenue by department and revenue band",

    selected_dataset="finance",

    dataset_confidence=1.0,

    metrics=[
        "department_total_revenue"
    ],

    dimensions=[
        "department_name",
        "revenue_band"
    ],

    filters=[]
)


schema = SchemaManager()

generator = SQLGenerator(
    schema_manager=schema
)


generated = generator.generate(result)

sql = generated.sql


print()
print("Generated SQL:")
print(sql)


expected_sql = (
    "SELECT department_name, revenue_band, "
    "SUM(department_total_revenue) AS department_total_revenue "
    "FROM gold_finance_analytics "
    "GROUP BY department_name, revenue_band"
)


print()
print("Expected SQL:")
print(expected_sql)


print()
print("=" * 60)
print("VALIDATION")
print("=" * 60)


if sql == expected_sql:

    print("PASS: Multiple dimension SQL generated correctly.")

else:

    print("FAIL: SQL does not match expected output.")