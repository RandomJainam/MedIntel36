"""
=========================================================
MedIntel360
Feature Engineering v1
=========================================================

Creates reusable features for:

• Power BI
• Machine Learning
• Data Mining
• AI Agents

Output:
--------
feature_store_v1

Author : Jainam Gada
Project: MedIntel360
"""

from pathlib import Path

import numpy as np
import pandas as pd

from config import FEATURE_STORE_DIR

from utils.database_manager import DatabaseManager
from utils.logger import Logger
from utils.validators import DataValidator


logger = Logger.get_logger()


class FeatureEngineering(DatabaseManager):

    """
    Builds reusable business features
    from the Star Schema.
    """

    def __init__(self):

        super().__init__()

        logger.info("=" * 70)
        logger.info("Starting Feature Engineering v1")
        logger.info("=" * 70)

        FEATURE_STORE_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        self.feature_store = None

    # ==================================================
    # Load Required Tables
    # ==================================================

    def load_tables(self):

        logger.info("Loading Star Schema Tables...")

        self.fact_admission = self.load_table(
            "fact_admission"
        )

        self.fact_billing = self.load_table(
            "fact_billing"
        )

        self.dim_patient = self.load_table(
            "dim_patient"
        )

        self.patient_insurance = self.load_table(
            "patient_insurance"
        )

        logger.info("Tables Loaded Successfully")

    # ==================================================
    # Merge Tables
    # ==================================================

    def merge_tables(self):

        logger.info("Merging Tables...")

        df = self.fact_admission.merge(

            self.fact_billing,

            on="admission_id",

            how="left"

        )

        df = df.merge(

            self.dim_patient,

            on="patient_id",

            how="left"

        )

        insurance = self.patient_insurance[[
            "patient_id"
        ]].drop_duplicates()

        insurance["insurance_flag"] = 1

        df = df.merge(

            insurance,

            on="patient_id",

            how="left"

        )

        df["insurance_flag"] = df[
            "insurance_flag"
        ].fillna(0)

        self.feature_store = df

        logger.info(
            "Merged Dataset Shape : %s",
            self.feature_store.shape
        )

    # ==================================================
    # Utility Methods
    # ==================================================

    def calculate_age(self):

        logger.info("Calculating Age...")

        self.feature_store["date_of_birth"] = pd.to_datetime(

            self.feature_store["date_of_birth"]

        )

        self.feature_store["admission_date"] = pd.to_datetime(

            self.feature_store["admission_date"]

        )

        self.feature_store["age"] = (

            self.feature_store["admission_date"].dt.year

            -

            self.feature_store["date_of_birth"].dt.year

        )

    # --------------------------------------------------

    def calculate_age_group(self):

        logger.info("Calculating Age Group...")

        bins = [

            0,
            18,
            35,
            50,
            65,
            120

        ]

        labels = [

            "Child",

            "Young Adult",

            "Adult",

            "Middle Age",

            "Senior Citizen"

        ]

        self.feature_store["age_group"] = pd.cut(

            self.feature_store["age"],

            bins=bins,

            labels=labels,

            include_lowest=True

        )

    # --------------------------------------------------

    def calculate_month(self):

        logger.info("Extracting Admission Month...")

        self.feature_store["admission_month"] = (

            self.feature_store["admission_date"]

            .dt.month_name()

        )

    # --------------------------------------------------

    def calculate_quarter(self):

        logger.info("Extracting Quarter...")

        self.feature_store["admission_quarter"] = (

            self.feature_store["admission_date"]

            .dt.quarter

        )

    # --------------------------------------------------

    def calculate_weekday(self):

        logger.info("Extracting Weekday...")

        self.feature_store["admission_weekday"] = (

            self.feature_store["admission_date"]

            .dt.day_name()

        )
            # --------------------------------------------------

    def calculate_weekend_flag(self):

        logger.info("Calculating Weekend Admission...")

        self.feature_store["weekend_admission"] = np.where(

            self.feature_store["admission_date"].dt.dayofweek >= 5,

            1,

            0

        )

    # --------------------------------------------------

    def calculate_revenue_per_day(self):

        logger.info("Calculating Revenue Per Day...")

        los = self.feature_store["los"].replace(0, 1)

        self.feature_store["revenue_per_day"] = (

            self.feature_store["total_amount"]

            /

            los

        ).round(2)

    # --------------------------------------------------

    def calculate_revenue_category(self):

        logger.info("Calculating Revenue Category...")

        self.feature_store["revenue_category"] = pd.qcut(

            self.feature_store["total_amount"],

            q=3,

            labels=[

                "Low",

                "Medium",

                "High"

            ],

            duplicates="drop"

        )

    # --------------------------------------------------

    def calculate_long_stay_flag(self):

        logger.info("Calculating Long Stay Flag...")

        average_los = self.feature_store["los"].mean()

        self.feature_store["long_stay_flag"] = np.where(

            self.feature_store["los"] > average_los,

            1,

            0

        )

    # --------------------------------------------------

    def calculate_high_revenue_flag(self):

        logger.info("Calculating High Revenue Flag...")

        average_revenue = self.feature_store["total_amount"].mean()

        self.feature_store["high_revenue_flag"] = np.where(

            self.feature_store["total_amount"] > average_revenue,

            1,

            0

        )

    # --------------------------------------------------

    def calculate_senior_citizen_flag(self):

        logger.info("Calculating Senior Citizen Flag...")

        self.feature_store["senior_citizen_flag"] = np.where(

            self.feature_store["age"] >= 60,

            1,

            0

        )

    # --------------------------------------------------

    def calculate_length_of_stay_category(self):

        logger.info("Calculating Length of Stay Category...")

        self.feature_store["los_category"] = pd.cut(

            self.feature_store["los"],

            bins=[0, 3, 7, 15, 100],

            labels=[

                "Short",

                "Medium",

                "Long",

                "Critical"

            ],

            include_lowest=True

        )

    # --------------------------------------------------

    def calculate_payment_ratio(self):

        logger.info("Calculating Payment Ratio...")

        revenue = self.feature_store["total_amount"].replace(0, 1)

        self.feature_store["patient_payment_ratio"] = (

            self.feature_store["patient_payable_amount"]

            /

            revenue

        ).round(2)

    # --------------------------------------------------

    def calculate_insurance_coverage_ratio(self):

        logger.info("Calculating Insurance Coverage Ratio...")

        revenue = self.feature_store["total_amount"].replace(0, 1)

        self.feature_store["insurance_coverage_ratio"] = (

            self.feature_store["insurance_covered_amount"]

            /

            revenue

        ).round(2)

    # --------------------------------------------------

    def calculate_revenue_band(self):

        logger.info("Calculating Revenue Band...")

        self.feature_store["revenue_band"] = pd.cut(

            self.feature_store["total_amount"],

            bins=[

                0,

                5000,

                15000,

                30000,

                float("inf")

            ],

            labels=[

                "Very Low",

                "Low",

                "Medium",

                "High"

            ],

            include_lowest=True

        )

    # --------------------------------------------------

    def build_features(self):

        logger.info("=" * 60)

        logger.info("Building Business Features")

        logger.info("=" * 60)

        self.calculate_age()

        self.calculate_age_group()

        self.calculate_month()

        self.calculate_quarter()

        self.calculate_weekday()

        self.calculate_weekend_flag()

        self.calculate_revenue_per_day()

        self.calculate_revenue_category()

        self.calculate_long_stay_flag()

        self.calculate_high_revenue_flag()

        self.calculate_senior_citizen_flag()

        self.calculate_length_of_stay_category()

        self.calculate_payment_ratio()

        self.calculate_insurance_coverage_ratio()

        self.calculate_revenue_band()

        logger.info("Business Features Created Successfully")
        # ==================================================
    # Additional Features
    # ==================================================

    def calculate_admission_season(self):

        logger.info("Calculating Admission Season...")

        month = self.feature_store["admission_date"].dt.month

        conditions = [

            month.isin([12, 1, 2]),

            month.isin([3, 4, 5]),

            month.isin([6, 7, 8, 9]),

            month.isin([10, 11])

        ]

        seasons = [

            "Winter",

            "Summer",

            "Monsoon",

            "Autumn"

        ]

        self.feature_store["admission_season"] = np.select(

            conditions,

            seasons,

            default="Unknown"

        )

    # ==================================================
    # Validation
    # ==================================================

    def validate(self):

        logger.info("=" * 60)
        logger.info("Validating Feature Store")
        logger.info("=" * 60)

        DataValidator.check_empty(
            self.feature_store
        )

        report = DataValidator.validation_report(
            self.feature_store
        )

        logger.info(report)

    # ==================================================
    # Metadata
    # ==================================================

    def generate_feature_catalog(self):

        logger.info("Generating Feature Catalog...")

        catalog = pd.DataFrame({

            "feature_name": self.feature_store.columns,

            "data_type": [

                str(dtype)

                for dtype in self.feature_store.dtypes

            ]

        })

        catalog.to_csv(

            "metadata/feature_catalog.csv",

            index=False

        )

        logger.info("Feature Catalog Updated")

    # ==================================================
    # Save Feature Store
    # ==================================================

    def export(self):

        logger.info("=" * 60)
        logger.info("Saving Feature Store")
        logger.info("=" * 60)

        self.save_table(

            self.feature_store,

            "feature_store_v1"

        )

        self.export_csv(

            self.feature_store,

            "feature_store_v1",

            FEATURE_STORE_DIR

        )

    # ==================================================
    # Main Build Pipeline
    # ==================================================

    def build(self):

        logger.info("Starting Feature Store Pipeline")

        self.load_tables()

        self.merge_tables()

        self.build_features()

        self.calculate_admission_season()

        self.validate()

        self.generate_feature_catalog()

        self.export()

        logger.info("=" * 60)

        logger.info("Feature Store v1 Created Successfully")

        logger.info("=" * 60)   
        
if __name__ == "__main__":

    FeatureEngineering().build()