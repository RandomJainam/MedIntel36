"""
============================================================
MedIntel360
Data Validation Utilities
============================================================

Provides reusable validation methods for ETL pipelines.
"""

import pandas as pd


class DataValidator:

    @staticmethod
    def check_empty(df: pd.DataFrame):
        """
        Ensure dataframe is not empty.
        """
        if df.empty:
            raise ValueError("❌ Validation Failed: DataFrame is empty.")

    @staticmethod
    def check_duplicate_rows(df: pd.DataFrame):
        """
        Returns total duplicate rows.
        """
        return int(df.duplicated().sum())

    @staticmethod
    def check_missing_values(df: pd.DataFrame):
        """
        Returns missing values per column.
        """
        return df.isnull().sum()

    @staticmethod
    def check_duplicate_primary_key(df: pd.DataFrame, primary_key: str):
        """
        Checks duplicate values for a primary key.
        """
        if primary_key not in df.columns:
            return 0

        return int(df[primary_key].duplicated().sum())

    @staticmethod
    def validation_report(df: pd.DataFrame):

        report = [
            "=" * 70,
            "DATA VALIDATION REPORT",
            "=" * 70,
            f"Rows                 : {len(df):,}",
            f"Columns              : {len(df.columns)}",
            f"Duplicate Rows       : {DataValidator.check_duplicate_rows(df):,}",
            f"Total Missing Values : {df.isnull().sum().sum():,}",
            "=" * 70
        ]

        return "\n".join(report)