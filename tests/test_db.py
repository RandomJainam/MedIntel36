from utils.validators import DataValidator
from utils.database_manager import DatabaseManager

db = DatabaseManager()

patient = db.load_table("patient")

print(DataValidator.validation_report(patient))