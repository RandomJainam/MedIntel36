"""
=========================================================
MedIntel360
Sequential Pattern Mining
=========================================================

Builds patient treatment sequences from admissions.

Author : Jainam Gada
"""

import pandas as pd

from mining.data_loader import DataLoader


class SequentialPatternMining:

    """
    Patient Treatment Sequence Mining.
    """

    def __init__(self):

        self.df = None

        self.sequences = None

    # =====================================================
    # Load Data
    # =====================================================

    def load_data(self):

        self.df = DataLoader.medical()

        return self.df

    # =====================================================
    # Prepare Data
    # =====================================================

    def prepare_data(self):

        self.df["admission_date"] = pd.to_datetime(

            self.df["admission_date"]

        )

        self.df = self.df.sort_values(

            [

                "patient_id",

                "admission_date"

            ]

        )

        return self.df

    # =====================================================
    # Build Patient Sequences
    # =====================================================

    def build_sequences(self):

        sequences = []

        grouped = self.df.groupby("patient_id")

        for patient_id, group in grouped:

            sequence = []

            for _, row in group.iterrows():

                if pd.notna(row["disease_name"]):

                    sequence.append(

                        "Disease:" + str(row["disease_name"])

                    )

                if pd.notna(row["test_name"]):

                    sequence.append(

                        "Test:" + str(row["test_name"])

                    )

                if pd.notna(row["drug_name"]):

                    sequence.append(

                        "Drug:" + str(row["drug_name"])

                    )

            if sequence:

                sequences.append(

                    {

                        "patient_id": patient_id,

                        "sequence": " -> ".join(sequence),

                        "sequence_length": len(sequence)

                    }

                )

        self.sequences = pd.DataFrame(

            sequences

        )

        return self.sequences

    # =====================================================
    # Sequence Summary
    # =====================================================

    def sequence_summary(self):

        summary = (

            self.sequences

            .groupby("sequence_length")

            .agg(

                patient_count=("patient_id","count")

            )

            .reset_index()

            .sort_values(

                "sequence_length"

            )

        )

        return summary

    # =====================================================
    # Export
    # =====================================================

    def export_results(

        self,

        path="data/processed/patient_sequences.csv"

    ):

        self.sequences.to_csv(

            path,

            index=False

        )

    # =====================================================
    # Pipeline
    # =====================================================

    def run(self):

        self.load_data()

        self.prepare_data()

        self.build_sequences()

        return self.sequence_summary()