from ai_engine.schema_manager import SchemaManager

schema = SchemaManager()

print(schema.get_metric_names("finance"))

print(schema.get_dimension_names("patient"))

print(schema.search_metrics("finance", "revenue"))

print(schema.search_dimensions("operations", "doctor"))

print(schema.search_glossary("los"))