"""
=========================================================
MedIntel360
Anomaly Detection
=========================================================

Detects abnormal patient admissions using
Isolation Forest.

Author : Jainam Gada
"""

import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from mining.data_loader import DataLoader


class AnomalyDetection:

    """
    Detect abnormal patient admissions.
    """

    def __init__(

        self,

        contamination=0.02

    ):

        self.contamination = contamination

        self.df = None

        self.features = None

        self.scaled_features = None

        self.model = None

    # =====================================================
    # Load Data
    # =====================================================

    def load_data(self):

        self.df = DataLoader.patient()

        return self.df

    # =====================================================
    # Prepare Features
    # =====================================================

    def prepare_features(self):

        columns = [

            "age",

            "los",

            "total_amount",

            "patient_visit_count",

            "patient_lifetime_revenue"

        ]

        self.features = self.df[columns].copy()

        return self.features

    # =====================================================
    # Scale Features
    # =====================================================

    def scale_features(self):

        scaler = StandardScaler()

        self.scaled_features = scaler.fit_transform(

            self.features

        )

        return self.scaled_features

    # =====================================================
    # Build Isolation Forest
    # =====================================================

    def build_model(self):

        self.model = IsolationForest(

            contamination=self.contamination,

            random_state=42

        )

        prediction = self.model.fit_predict(

            self.scaled_features

        )

        self.df["anomaly"] = prediction

        self.df["anomaly_flag"] = self.df["anomaly"].map(

            {

                1: "Normal",

                -1: "Outlier"

            }

        )

        self.df["anomaly_score"] = self.model.decision_function(

            self.scaled_features

        )

        return self.df

    # =====================================================
    # Summary
    # =====================================================

    def anomaly_summary(self):

        summary = (

            self.df

            .groupby("anomaly_flag")

            .agg(

                admissions=("admission_id", "count"),

                average_revenue=("total_amount", "mean"),

                average_los=("los", "mean")

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

        path="data/processed/patient_anomalies.csv"

    ):

        self.df.to_csv(

            path,

            index=False

        )

    # =====================================================
    # Pipeline
    # =====================================================

    def run(self):

        self.load_data()

        self.prepare_features()

        self.scale_features()

        self.build_model()

        return self.anomaly_summary()