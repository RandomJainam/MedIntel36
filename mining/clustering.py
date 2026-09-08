"""
=========================================================
MedIntel360
Patient Clustering
=========================================================

Performs Patient Segmentation using K-Means Clustering.

Author : Jainam Gada
"""

import pandas as pd

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from mining.data_loader import DataLoader


class PatientClustering:

    """
    Patient Segmentation using K-Means.
    """

    def __init__(self, n_clusters=4):

        self.n_clusters = n_clusters

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
    # Feature Scaling
    # =====================================================

    def scale_features(self):

        scaler = StandardScaler()

        self.scaled_features = scaler.fit_transform(

            self.features

        )

        return self.scaled_features

    # =====================================================
    # Build Model
    # =====================================================

    def build_model(self):

        self.model = KMeans(

            n_clusters=self.n_clusters,

            random_state=42,

            n_init=10

        )

        self.df["cluster"] = self.model.fit_predict(

            self.scaled_features

        )
        cluster_names = {
            0: "Short Stay",
            1: "High Revenue",
            2: "Long Stay",
            3: "Frequent Patients"
        }

        self.df["cluster_name"] = self.df["cluster"].map(cluster_names)
        return self.df

    # =====================================================
    # Cluster Summary
    # =====================================================

    def cluster_summary(self):

        summary = (

            self.df

            .groupby("cluster")

            .agg(

                patients=("patient_id","nunique"),

                average_age=("age","mean"),

                average_los=("los","mean"),

                average_revenue=("total_amount","mean"),

                average_visits=("patient_visit_count","mean")

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

        path="data/processed/patient_clusters.csv"

    ):

        self.df.to_csv(

            path,

            index=False

        )

    # =====================================================
    # Complete Pipeline
    # =====================================================

    def run(self):

        self.load_data()

        self.prepare_features()

        self.scale_features()

        self.build_model()

        return self.cluster_summary()