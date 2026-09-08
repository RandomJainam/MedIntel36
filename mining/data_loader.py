"""
=========================================================
MedIntel360
Data Loader
=========================================================

Centralized loader for Gold Analytics datasets.

Author : Jainam Gada
"""

from pathlib import Path

import pandas as pd


class DataLoader:

    """
    Loads Gold Layer datasets.
    """

    GOLD_PATH = Path("data/gold")

    # -----------------------------------------------------

    @classmethod
    def patient(cls):

        return pd.read_csv(

            cls.GOLD_PATH / "gold_patient_analytics.csv"

        )

    # -----------------------------------------------------

    @classmethod
    def finance(cls):

        return pd.read_csv(

            cls.GOLD_PATH / "gold_finance_analytics.csv"

        )

    # -----------------------------------------------------

    @classmethod
    def operations(cls):

        return pd.read_csv(

            cls.GOLD_PATH / "gold_operations_analytics.csv"

        )

    # -----------------------------------------------------

    @classmethod
    def medical(cls):

        return pd.read_csv(

            cls.GOLD_PATH / "gold_medical_analytics.csv"

        )

    # -----------------------------------------------------

    @classmethod
    def load(cls, dataset):

        datasets = {

            "patient": cls.patient,

            "finance": cls.finance,

            "operations": cls.operations,

            "medical": cls.medical

        }

        if dataset not in datasets:

            raise ValueError(f"Unknown dataset : {dataset}")

        return datasets[dataset]()