"""
=========================================================
MedIntel360
Time Series Analysis
=========================================================

Performs monthly trend analysis for hospital admissions,
revenue and LOS.

Author : Jainam Gada
"""

import pandas as pd

from mining.data_loader import DataLoader


class TimeSeriesAnalysis:

    """
    Hospital Time Series Analytics.
    """

    def __init__(self):

        self.df = None

    # =====================================================
    # Load Data
    # =====================================================

    def load_data(self):

        self.df = DataLoader.patient()

        return self.df

    # =====================================================
    # Prepare Dates
    # =====================================================

    def prepare_data(self):

        self.df["admission_date"] = pd.to_datetime(

            self.df["admission_date"]

        )

        self.df["year_month"] = (

            self.df["admission_date"]

            .dt.to_period("M")

            .astype(str)

        )

        return self.df

    # =====================================================
    # Monthly Summary
    # =====================================================

    def monthly_summary(self):

        summary = (

            self.df

            .groupby("year_month")

            .agg(

                admissions=("admission_id","count"),

                patients=("patient_id","nunique"),

                revenue=("total_amount","sum"),

                average_los=("los","mean")

            )

            .round(2)

            .reset_index()

        )

        return summary

    # =====================================================
    # Export
    # =====================================================

    def export_results(

        self,

        path="data/processed/monthly_trends.csv"

    ):

        summary = self.monthly_summary()

        summary.to_csv(

            path,

            index=False

        )

    # =====================================================
    # Pipeline
    # =====================================================

    def run(self):

        self.load_data()

        self.prepare_data()

        return self.monthly_summary()