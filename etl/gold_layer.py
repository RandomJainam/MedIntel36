"""
=========================================================
MedIntel360
Gold Layer Builder
=========================================================

Creates Analytics Ready Gold Tables

Outputs
-------
gold_patient_analytics
gold_finance_analytics
gold_operations_analytics
gold_medical_analytics

Author : Jainam Gada
"""
import logging
import pandas as pd
import numpy as np

from pathlib import Path

from config import GOLD_DIR

from utils.database_manager import DatabaseManager
from utils.validators import DataValidator


from analytics_engine.kpi_engine import KPIEngine
from analytics_engine.business_rules import BusinessRules

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


class GoldLayer(DatabaseManager):

    def __init__(self):

        super().__init__()

        logger.info("=" * 70)
        logger.info("Starting Gold Layer Builder")
        logger.info("=" * 70)

        self.gold = {}

    # ==================================================

    def load_tables(self):

        logger.info("=" * 70)
        logger.info("Loading Tables")
        logger.info("=" * 70)

        # ==================================================
        # Feature Store
        # ==================================================

        self.feature_store = self.load_table(
            "feature_store_v1"
        )

        # ==================================================
        # Dimension Tables
        # ==================================================

        self.patient_insurance = self.load_table(
            "patient_insurance"
        )

        self.insurance_provider = self.load_table(
            "insurance_provider"
        )

        self.department = self.load_table(
            "dim_department"
        )

        self.disease = self.load_table(
            "dim_disease"
        )

        self.doctor = self.load_table(
            "dim_doctor"
        )

        self.ward = self.load_table(
            "dim_ward"
        )

        self.insurance = self.load_table(
            "dim_insurance"
        )

        self.billing_detail = self.load_table(
            "billing_detail"
        )

        # ==================================================
        # Operational Tables
        # ==================================================

        self.admission = self.load_table(
            "admission"
        )

        self.bed = self.load_table(
            "bed"
        )

        self.employee = self.load_table(
            "employee"
        )

        self.staff_assignment = self.load_table(
            "staff_assignment"
        )

        # ==================================================
        # Clinical Tables
        # ==================================================

        self.patient_diagnostic = self.load_table(
            "patient_diagnostic"
        )

        self.diagnostic_test = self.load_table(
            "diagnostic_test"
        )

        self.prescription = self.load_table(
            "prescription"
        )

        self.drug = self.load_table(
            "drug"
        )

        logger.info("All Tables Loaded Successfully")

    # ==================================================

    def validate(self, dataframe, primary_key=None):

        DataValidator.check_empty(
            dataframe
        )

        report = DataValidator.validation_report(
            dataframe
        )

        if primary_key:
            duplicates = DataValidator.check_duplicate_primary_key(dataframe, primary_key)
            logger.info(f"Duplicate Primary Keys : {duplicates}")

        logger.info("\n" + report)

    # ==================================================

    def save_gold_table(
        self,
        dataframe,
        table_name
    ):

        self.validate(dataframe)

        self.save_table(
            dataframe,
            table_name
        )

        self.export_csv(
            dataframe,
            table_name,
            GOLD_DIR
        )

        self.gold[table_name] = len(dataframe)

        logger.info(
            "%s created successfully.",
            table_name
        )

    # ==================================================

    def merge_department(self, df):

        return df.merge(

            self.department,

            on="department_id",

            how="left"

        )

    # ==================================================

    def merge_disease(self, df):

        return df.merge(

            self.disease,

            on="disease_id",

            how="left"

        )

    # ==================================================

    def merge_doctor(self, df):

        if "doctor_id" not in df.columns:

            return df

        return df.merge(

            self.doctor,

            on="doctor_id",

            how="left"

        )

    # ==================================================

    def merge_ward(self, df):

        ward = self.ward.drop(columns=["department_id"])

        # print("\nWard Columns")
        #print(ward.columns.tolist())

        merged = df.merge(
            ward,
            on="ward_id",
            how="left"
        )

        #print("\nMerged Columns")
       # print(merged.columns.tolist())

        return merged
    
    # ==================================================
    # Patient Analytics Mart
    # ==================================================
    def enrich_patient_data(self, df):

        df = self.merge_department(df)
        df = self.merge_disease(df)
        df = self.merge_ward(df)

        return df
    
    def build_patient_gold(self):

        logger.info("=" * 60)
        logger.info("Building Patient Analytics Mart")
        logger.info("=" * 60)

        patient = self.feature_store.copy()
        patient = self.enrich_patient_data(patient)

        patient = KPIEngine.build_patient_kpis(patient)
        patient = BusinessRules.build_patient_rules(patient)
        self.validate(patient, "patient_id")
        self.save_gold_table(
            patient,
            "gold_patient_analytics"
        )

        logger.info(

            "Patient Analytics Mart Created."

        )
    
    # ==================================================
    # Finance Enrichment
    # ==================================================

    def enrich_finance_data(self, df):

        logger.info("Enriching Finance Dataset...")
        #print("=" * 60)
        #print("feature_store", len(df))

        # Department

        df = self.merge_department(df)
       # print("\nAfter merge_department", len(df))

        # Billing Detail


        df = df.merge(

            self.billing_detail,

            on="bill_id",

            how="left"

        )
        #print("\nAfter merge_billing_detail", len(df))

        # ----------------------------------------------- 
        # Insurance Summary
        # -----------------------------------------------

        self.patient_insurance
        self.insurance_provider
        insurance_summary = self.build_insurance_summary()
        #print("\nInsurance Summary", len(insurance_summary))
        #print("duplicate patient_ids in insurance_summary:", insurance_summary["patient_id"].duplicated().sum())

        df = df.merge(

            insurance_summary,

            on="patient_id",

            how="left"

        )

        #print("\nAfter merge_insurance_summary", len(df))
        #print("=" * 60)
        return df

    
    def build_finance_gold(self):

        logger.info("=" * 60)
        logger.info("Building Finance Analytics Mart")
        logger.info("=" * 60)

        finance = self.feature_store.copy()

        finance = self.enrich_finance_data(finance)

        finance = KPIEngine.build_finance_kpis(finance)
        finance = BusinessRules.build_finance_rules(finance)
        self.validate(finance, "bill_id")

        self.save_gold_table(

            finance,

            "gold_finance_analytics"

        )

        logger.info(

            "Finance Analytics Mart Created Successfully"

        )

    # ==================================================
    # Operations Enrichment
    # ==================================================
    
    def enrich_operations_data(self, df):

        logger.info("Enriching Operations Dataset...")

       # print("\nBefore merge_ward")
        #print(df.columns.tolist())

        # Ward
        df = self.merge_ward(df)

        #print("\nAfter merge_ward")
        #print(df.columns.tolist())

        # Department
        df = self.merge_department(df)

        #print("\nAfter merge_department")
        #print(df.columns.tolist())

        # Bed
        bed = self.bed.drop(columns=["ward_id"])

        df = df.merge(
            bed,
            on="bed_id",
            how="left"
        )

        # -----------------------------------------------
        # Staff Summary
        # -----------------------------------------------

        staff_summary = self.build_staff_summary()

        df = df.merge(

            staff_summary,

            on="ward_id",

            how="left"

        )

        return df

    def build_operations_gold(self):

        logger.info("=" * 60)
        logger.info("Building Operations Analytics Mart")
        logger.info("=" * 60)

        operations = self.feature_store.copy()

        operations = self.enrich_operations_data(operations)

        operations = KPIEngine.build_operations_kpis(operations)
        operations = BusinessRules.build_operations_rules(operations)
        self.validate(operations, "admission_id")
        self.save_gold_table(
            operations,
            "gold_operations_analytics"
        )

        logger.info(
            "Operations Analytics Mart Created Successfully"
        )

    # ==================================================
    # Medical Enrichment
    # ==================================================

    def enrich_medical_data(self, df):

        logger.info("Enriching Medical Dataset...")

        # Disease
        disease_cols = [
            "disease_id",
            "disease_name",
            "disease_category"
        ]

        df = df.merge(
            self.disease[disease_cols],
            on="disease_id",
            how="left"
        )

        # Admission
        admission_cols = [
            "admission_id",
            "discharge_date"
        ]

        df = df.merge(
            self.admission[admission_cols],
            on="admission_id",
            how="left"
        )

        # Remove duplicate admission_date
        if "admission_date_adm" in df.columns:  
            df.drop(columns=["admission_date_adm"], inplace=True)

        # Patient Diagnostic
        diagnostic_cols = [
            "patient_diagnostic_id",
            "admission_id",
            "test_date",
            "result_status",
            "test_id",
            "doctor_id"
        ]

        df = df.merge(
            self.patient_diagnostic[diagnostic_cols],
            on="admission_id",
            how="left"
        )

        # Diagnostic Test
        test_cols = [
            "test_id",
            "test_name",
            "test_category",
            "standard_cost"
        ]

        df = df.merge(
            self.diagnostic_test[test_cols],
            on="test_id",
            how="left"
        )

        # Prescription
        prescription_cols = [
            "prescription_id",
            "admission_id",
            "drug_id",
            "dosage",
            "frequency",
            "duration_days"
        ]

        df = df.merge(
            self.prescription[prescription_cols],
            on="admission_id",
            how="left"
        )

        # Drug
        drug_cols = [
            "drug_id",
            "drug_name",
            "brand_name",
            "drug_category",
            "unit_cost",
            "manufacturer_id"
        ]

        df = df.merge(
            self.drug[drug_cols],
            on="drug_id",
            how="left"
        )
        # Doctor
        doctor_cols = [
            "doctor_id",
            "employee_id",
            "employee_name",
            "gender",
            "role",
            "department_id",
            "specialization",
            "qualification",
            "experience_years"
        ]

        doctor_df = (
            self.doctor[doctor_cols]
            .rename(columns={
                "gender": "doctor_gender",
                "department_id": "doctor_department_id"
            })
        )

        df = df.merge(
            doctor_df,
            on="doctor_id",
            how="left"
        )

        logger.info("Medical Dataset Enriched Successfully")
        return df
        # ==================================================
        # Medical Analytics Mart
        # ==================================================

    def build_medical_gold(self):

        logger.info("=" * 60)
        logger.info("Building Medical Analytics Mart")
        logger.info("=" * 60)

        medical = self.feature_store.copy()

        medical = self.enrich_medical_data(medical)

        # Disease Case Count
        medical["disease_case_count"] = (
            medical.groupby("disease_name")["admission_id"]
            .transform("nunique")
        )

        # Diagnostic Test Usage
        medical["test_usage_count"] = (
            medical.groupby("test_name")["test_id"]
            .transform("count")
        )

        # Drug Usage
        medical["drug_usage_count"] = (
            medical.groupby("drug_name")["drug_id"]
            .transform("count")
        )

        # Doctor Patient Count
        medical["doctor_patient_count"] = (
            medical.groupby("doctor_id")["patient_id"]
            .transform("nunique")
        )

        # Average LOS
        medical["average_los_by_disease"] = (
            medical.groupby("disease_name")["los"]
            .transform("mean")
            .round(2)
        )

        # Average Revenue
        medical["average_revenue_by_disease"] = (
            medical.groupby("disease_name")["total_amount"]
            .transform("mean")
            .round(2)
        )

        threshold = medical["disease_case_count"].median()

        medical["high_volume_disease_flag"] = np.where(
            medical["disease_case_count"] >= threshold,
            1,
            0
        )

        self.validate(medical, "patient_diagnostic_id")
        self.save_gold_table(
            medical,
            "gold_medical_analytics"
        )

        logger.info(
            "Medical Analytics Mart Created Successfully"
        )
        
        medical = BusinessRules.build_medical_rules(medical)
        
    # -----------------------------------------------
    # Build Staff Summary
    # -----------------------------------------------

    def build_staff_summary(self):
        logger.info("Building Staff Summary...")

        # -----------------------------------------------
        # Merge Staff Assignment with Employee
        # -----------------------------------------------

        staff = self.staff_assignment.merge(

            self.employee,

            on="employee_id",

            how="left"

        )

        # -----------------------------------------------
        # Create Role Flags
        # -----------------------------------------------

        staff["doctor_flag"] = (staff["role"] == "Doctor").astype(int)

        staff["nurse_flag"] = (staff["role"] == "Nurse").astype(int)

        staff["technician_flag"] = (
            staff["role"] == "Technician"
        ).astype(int)

        # -----------------------------------------------
        # Night Shift Flag
        # -----------------------------------------------

        staff["night_shift_flag"] = (

            staff["shift"]

            .str.lower()

            .eq("night")

            .astype(int)

        )

        # -----------------------------------------------
        # Aggregate
        # -----------------------------------------------

        staff_summary = (

            staff

            .groupby("ward_id")

            .agg(

                staff_count=("employee_id", "count"),

                doctor_count=("doctor_flag", "sum"),

                nurse_count=("nurse_flag", "sum"),

                technician_count=("technician_flag", "sum"),

                shift_count=("shift", "nunique"),

                night_shift_count=("night_shift_flag", "sum")

                ).reset_index()

        )

        logger.info("Staff Summary Created Successfully")

        return staff_summary


    # -----------------------------------------------
    # Insurance Summary
    # -----------------------------------------------

    def build_insurance_summary(self):
        logger.info("Building Insurance Summary...")

        # -----------------------------------------------
        # Load Insurance Provider
        # -----------------------------------------------

        provider = self.insurance_provider.copy()

        # -----------------------------------------------
        # Merge Provider
        # -----------------------------------------------

        insurance = self.patient_insurance.merge(

            provider,

            on="insurance_provider_id",

            how="left"

        )

        # -----------------------------------------------
        # Multiple Policy Flag
        # -----------------------------------------------

        insurance["multiple_policy_flag"] = 1

        # -----------------------------------------------
        # Aggregate
        # -----------------------------------------------

        insurance_summary = (

            insurance

            .groupby("patient_id")

            .agg(

               policy_count=("patient_insurance_id", "count"),
               provider_count=("insurance_provider_id", "nunique"),
               average_coverage_percentage=("coverage_percentage", "mean"),
               maximum_coverage_percentage=("coverage_percentage", "max"),

                ).reset_index()

        )
        # -----------------------------------------------
        # Multiple Policy Flag
        # -----------------------------------------------

        insurance_summary["multiple_policy_flag"] = np.where(

            insurance_summary["policy_count"] > 1,

            1,

            0

        )

        insurance_summary["average_coverage_percentage"] = (

            insurance_summary["average_coverage_percentage"]

            .round(2)

        )    

        logger.info("Insurance Summary Created Successfully")

        return insurance_summary

    
    def build_insurance_gold(self):

        logger.info("=" * 60)
        logger.info("Building Insurance Analytics Mart")
        logger.info("=" * 60)

        insurance = self.patient_insurance.merge(

            self.insurance_provider,

            on="insurance_provider_id",

            how="left"

        )

        self.save_gold_table(

            insurance,

            "gold_insurance_analytics"

        )

        logger.info("Insurance Analytics Mart Created Successfully")
    
    
    # ==================================================
    # Build Complete Gold Layer
    # ==================================================

    def build(self):

        logger.info("=" * 70)
        logger.info("Building Complete Gold Layer")
        logger.info("=" * 70)

        # Load all required tables
        self.load_tables()

        # Build Gold Tables
        self.build_patient_gold()

        self.build_finance_gold()

        self.build_insurance_gold()

        self.build_operations_gold()

        self.build_medical_gold()

        logger.info("=" * 70)
        logger.info("Gold Layer Built Successfully")
        logger.info("=" * 70)

        logger.info("Generated Gold Tables:")

        for table, rows in self.gold.items():

            logger.info(f"{table:<35} {rows} rows")

if __name__ == "__main__":

    GoldLayer().build()