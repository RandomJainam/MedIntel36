# test_schema.py

from database.schema import SchemaManager

schema = SchemaManager()

print(schema.get_tables())

print()

print(schema.get_schema_context())