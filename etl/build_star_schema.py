"""
=========================================================
MedIntel360
Star Schema Builder
=========================================================
Builds Data Warehouse Star Schema from Bronze Layer
"""

import pandas as pd
import time

from sqlalchemy import create_engine
from pathlib import Path
from datetime import datetime


from config import (
    DATABASE_URI,
    WAREHOUSE_DIR
)


class DataExtractor:

    def __init__(self):

        self.engine = create_engine(DATABASE_URI)

        WAREHOUSE_DIR.mkdir(parents=True, exist_ok=True)

        print("=" * 70)
        print("🏥 MedIntel360 - Star Schema Builder")
        print("=" * 70)
        

    # --------------------------------------------------

    def load_table(self, table_name):

        print(f"Loading {table_name}...")

        pd.read_sql_table(
            table_name,
            self.engine
        )
        df = pd.read_sql_table(
            table_name,
            self.engine
        )

        print(f"✓ Loaded {table_name}")
        print(f"Rows    : {len(df)}")
        print(f"Columns : {len(df.columns)}")
        print()

        return df
    # --------------------------------------------------

    def save_table(self, dataframe, table_name):

        dataframe.to_sql(
            table_name,
            self.engine,
            if_exists="replace",
            index=False
        )

        dataframe.to_csv(
            WAREHOUSE_DIR / f"{table_name}.csv",
            index=False
        )
        print(f"Rows Saved : {len(dataframe)}")
        print(f"Columns    : {len(dataframe.columns)}")
        print()

        print(f"✅ Saved {table_name}")

    # --------------------------------------------------

    def calculate_los(self, df):

        df["admission_date"] = pd.to_datetime(df["admission_date"])

        df["discharge_date"] = pd.to_datetime(df["discharge_date"])

        df["los"] = (
            df["discharge_date"]
            -
            df["admission_date"]
        ).dt.days

        return df

    # --------------------------------------------------

    def validate_dataframe(self, df, table_name):

        print()

        print(f"Validation Report : {table_name}")

        print("-" * 40)

        print("Rows :", len(df))

        print("Columns :", len(df.columns))

        print("Duplicates :", df.duplicated().sum())

        print("Missing Values :", df.isnull().sum().sum())

        print("-" * 40)
        print("Column-wise Missing Values")

        missing = df.isnull().sum()

        for column, count in missing.items():

            if count > 0:

                print(f"{column:<25}: {count}")

           

        print()

    # --------------------------------------------------

    def export(self, df, table_name):

        self.validate_dataframe(df, table_name)

        self.save_table(df, table_name)


class DimensionBuilder(DataExtractor):

    def build_dim_patient(self):

        patient = self.load_table("patient")

        dim_patient = patient.copy()

        self.export(dim_patient, "dim_patient")

        return dim_patient

    # --------------------------------------------------

    def build_dim_department(self):

        department = self.load_table("department")

        dim_department = department.copy()

        self.export(dim_department, "dim_department")

        return dim_department

    # --------------------------------------------------

    def build_dim_disease(self):

        disease = self.load_table("disease")

        dim_disease = disease.copy()

        self.export(dim_disease, "dim_disease")

        return dim_disease

    # --------------------------------------------------

    def build_dim_ward(self):

        ward = self.load_table("ward")

        dim_ward = ward.copy()

        self.export(dim_ward, "dim_ward")

        return dim_ward

    # --------------------------------------------------

    def build_dim_insurance(self):

        insurance = self.load_table("insurance_provider")

        dim_insurance = insurance.copy()

        self.export(dim_insurance, "dim_insurance")

        return dim_insurance

    # --------------------------------------------------

    def build_dim_doctor(self):

        doctor = self.load_table("doctor")

        employee = self.load_table("employee")

        dim_doctor = doctor.merge(

            employee,

            on="employee_id",

            how="left"

        )

        dim_doctor = dim_doctor[[

            "doctor_id",

            "employee_id",

            "employee_name",

            "gender",

            "role",

            "department_id",

            "specialization",

            "qualification",

            "experience_years"

        ]]

        self.export(dim_doctor, "dim_doctor")

        return dim_doctor

    # --------------------------------------------------

    def build_dimensions(self):

        print("\n")

        print("=" * 70)

        print("Building Dimension Tables")

        print("=" * 70)

        self.build_dim_patient()

        self.build_dim_department()

        self.build_dim_disease()

        self.build_dim_ward()

        self.build_dim_insurance()

        self.build_dim_doctor()

        print("\n✅ All Dimension Tables Created")
        print("Total Dimensions Created : 6")
        print()


class FactBuilder(DataExtractor):

    # --------------------------------------------------

    def build_fact_admission(self):

        print("\nBuilding Fact Admission...")

        admission = self.load_table("admission")
        print("✓ Length of Stay Calculated")
        print()

        admission = self.calculate_los(admission)

        fact_admission = admission[[

            "admission_id",
            "patient_id",
            "department_id",
            "ward_id",
            "bed_id",
            "disease_id",
            "admission_date",
            "discharge_date",
            "admission_type",
            "admission_status",
            "los"

        ]].copy()

        self.export(
            fact_admission,
            "fact_admission"
        )

        return fact_admission

    # --------------------------------------------------

    def build_fact_billing(self):

        print("\nBuilding Fact Billing...")

        billing = self.load_table("billing")
        print(f"Billing Records : {len(billing)}")
        print()

        fact_billing = billing[[

            "bill_id",
            "admission_id",
            "bill_date",
            "total_amount",
            "insurance_covered_amount",
            "patient_payable_amount",
            "payment_status",
            "payment_mode"

        ]].copy()

        self.export(
            fact_billing,
            "fact_billing"
        )

        return fact_billing

    # --------------------------------------------------

    def build_facts(self):

        print("\n")

        print("=" * 70)
        print("Building Fact Tables")
        print("=" * 70)
        print("Creating Analytical Fact Tables...")
        print()
        self.build_fact_admission()

        self.build_fact_billing()

        print("\n✅ All Fact Tables Created")
        print("Total Fact Tables : 2")
        print()


class StarSchemaBuilder:

  

    def __init__(self):

        self.dimension_builder = DimensionBuilder()
        self.fact_builder = FactBuilder()

    def build(self):

        print()

        print("=" * 70)
        print("Building Star Schema...")
        print("=" * 70)
        print("Pipeline Started")
        print()
        start = time.time()
        self.dimension_builder.build_dimensions()

        self.fact_builder.build_facts()
        end = time.time()

        print()
        print(f"Execution Time : {end-start:.2f} seconds")
        print()

        print("=" * 70)
        print("⭐ Star Schema Created Successfully")
        print("=" * 70)
        print()
        print("Summary")
        print("-" * 40)

        print("✓ Dimension Tables Built")
        print("✓ Fact Tables Built")
        print("✓ Validation Completed")
        print("✓ CSV Export Completed")

if __name__ == "__main__":
    builder = StarSchemaBuilder()
    builder.build()