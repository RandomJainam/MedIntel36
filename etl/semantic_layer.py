import pandas as pd
from sqlalchemy import create_engine

from config import DATABASE_URI, WAREHOUSE_DIR


class SemanticLayer:

    def __init__(self):

        self.engine = create_engine(DATABASE_URI)

        print("=" * 70)
        print("🏥 Building Semantic Layer")
        print("=" * 70)

    # --------------------------------------------------

    def load(self, table):

        return pd.read_sql_table(
            table,
            self.engine
        )

    # --------------------------------------------------

    def save(self, df, table):

        df.to_sql(
            table,
            self.engine,
            if_exists="replace",
            index=False
        )

        df.to_csv(
            WAREHOUSE_DIR / f"{table}.csv",
            index=False
        )

        print(f"✅ {table}")

    # --------------------------------------------------

    def build_patient_semantic(self):

        patient = self.load("dim_patient")

        patient = patient.rename(columns={

            "patient_id": "Patient ID",

            "gender": "Gender",

            "date_of_birth": "Date Of Birth",

            "blood_group": "Blood Group",

            "city": "City"

        })

        self.save(
            patient,
            "semantic_patient"
        )

    # --------------------------------------------------

    def build_department_semantic(self):

        department = self.load("dim_department")

        department = department.rename(columns={

            "department_id": "Department ID",

            "department_name": "Department",

            "department_type": "Department Type",

            "floor_number": "Floor"

        })

        self.save(
            department,
            "semantic_department"
        )

    # --------------------------------------------------

    def build_disease_semantic(self):

        disease = self.load("dim_disease")

        disease = disease.rename(columns={

            "disease_id": "Disease ID",

            "disease_name": "Disease",

            "disease_category": "Category"

        })

        self.save(
            disease,
            "semantic_disease"
        )

    # --------------------------------------------------

    def build_doctor_semantic(self):

        doctor = self.load("dim_doctor")

        doctor = doctor.rename(columns={

            "doctor_id": "Doctor ID",

            "employee_name": "Doctor",

            "specialization": "Specialization",

            "qualification": "Qualification",

            "experience_years": "Experience"

        })

        self.save(
            doctor,
            "semantic_doctor"
        )

    # --------------------------------------------------

    def build_finance_semantic(self):

        billing = self.load("fact_billing")

        billing = billing.rename(columns={

            "bill_id": "Bill ID",

            "admission_id": "Admission ID",

            "bill_date": "Bill Date",

            "total_amount": "Total Revenue",

            "insurance_covered_amount": "Insurance Covered",

            "patient_payable_amount": "Patient Payment",

            "payment_status": "Payment Status",

            "payment_mode": "Payment Mode"

        })

        self.save(
            billing,
            "semantic_finance"
        )

    # --------------------------------------------------

    def build_admission_semantic(self):

        admission = self.load("fact_admission")

        admission = admission.rename(columns={

            "admission_id": "Admission ID",

            "patient_id": "Patient ID",

            "department_id": "Department ID",

            "ward_id": "Ward ID",

            "bed_id": "Bed ID",

            "disease_id": "Disease ID",

            "admission_date": "Admission Date",

            "discharge_date": "Discharge Date",

            "admission_type": "Admission Type",

            "admission_status": "Admission Status",

            "los": "Length Of Stay"

        })

        self.save(
            admission,
            "semantic_admission"
        )

    # --------------------------------------------------

    def build(self):

        self.build_patient_semantic()

        self.build_department_semantic()

        self.build_disease_semantic()

        self.build_doctor_semantic()

        self.build_finance_semantic()

        self.build_admission_semantic()

        print()

        print("=" * 70)

        print("Semantic Layer Created Successfully")

        print("=" * 70)


if __name__ == "__main__":

    SemanticLayer().build()