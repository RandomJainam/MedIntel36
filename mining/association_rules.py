"""
=========================================================
MedIntel360
Association Rule Mining
=========================================================

Performs Association Rule Mining using the Apriori
algorithm on hospital transactions.

Author : Jainam Gada
"""

import pandas as pd
import numpy as np

from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules


from mining.data_loader import DataLoader


class AssociationRules:

    """
    Association Rule Mining Engine
    """

    def __init__(

        self,

        min_support=0.001,

        min_confidence=0.02,

        min_lift=1.05

    ):

        self.min_support = min_support
        self.min_confidence = min_confidence
        self.min_lift = min_lift

        self.df = None
        self.transactions = None
        self.encoded_df = None
        self.itemsets = None
        self.rules = None

    # =====================================================
    # Load Data
    # =====================================================

    def load_data(self):

        self.df = DataLoader.medical()

        return self.df

    # =====================================================
    # Build Transactions
    # =====================================================

    def build_transactions(self):

        transactions = []

        grouped = self.df.groupby("admission_id")

        for _, group in grouped:

            basket = set()

            # Disease

            if "disease_name" in group.columns:

                basket.update(

                    "Disease:" + x

                    for x in

                    group["disease_name"]

                    .dropna()

                    .astype(str)

                    .unique()

                )

            # Diagnostic Test

            if "test_name" in group.columns:

                basket.update(

                    "Test:" + x

                    for x in

                    group["test_name"]

                    .dropna()

                    .astype(str)

                    .unique()

                )

            # Drug

            if "drug_name" in group.columns:

                basket.update(

                    "Drug:" + x

                    for x in

                    group["drug_name"]

                    .dropna()

                    .astype(str)

                    .unique()

                )

            # Department

            if "department_name" in group.columns:

                basket.update(

                    "Department:" + x

                    for x in

                    group["department_name"]

                    .dropna()

                    .astype(str)

                    .unique()

                )

            transactions.append(list(basket))

        self.transactions = transactions


        return transactions

    # =====================================================
    # Encode Transactions
    # =====================================================

    def encode_transactions(self):

        encoder = TransactionEncoder()

        encoded = encoder.fit(

            self.transactions

        ).transform(

            self.transactions

        )

        self.encoded_df = pd.DataFrame(

            encoded,

            columns=encoder.columns_

        )

        return self.encoded_df

    # =====================================================
    # Frequent Itemsets
    # =====================================================

    def generate_itemsets(self):

        self.itemsets = apriori(

            self.encoded_df,

            min_support=self.min_support,

            use_colnames=True,
            max_len=2

        )


        return self.itemsets

    # =====================================================
    # Association Rules
    # =====================================================

    def generate_rules(self):

        self.rules = association_rules(

            self.itemsets,

            metric="confidence",

            min_threshold=self.min_confidence

        )

        self.rules = self.rules[

            self.rules["lift"] >= self.min_lift

        ]

        self.rules = self.rules.sort_values(

            ["lift", "confidence", "support"],

            ascending=[False, False, False]

        ).reset_index(drop=True)

        self.rules["antecedents"] = self.rules["antecedents"].apply(

            lambda x: ", ".join(sorted(list(x)))

        )

        self.rules["consequents"] = self.rules["consequents"].apply(

            lambda x: ", ".join(sorted(list(x)))

        )

        self.rules["rule_strength"] = np.where(

            self.rules["lift"] >= 2,

            "Very Strong",

            np.where(

                self.rules["lift"] >= 1.5,

                "Strong",

                np.where(

                    self.rules["lift"] >= 1.2,

                    "Moderate",

                    "Weak"

                )

            )

        )

        self.rules = self.rules[

            [

                "antecedents",

                "consequents",

                "support",

                "confidence",

                "lift",

                "rule_strength"

            ]

        ]

        return self.rules
    # =====================================================
    # Top Rules
    # =====================================================

    def top_rules(

        self,

        top_n=20

    ):

        if self.rules is None:

            return None

        return self.rules.head(top_n)

    # =====================================================
    # Export
    # =====================================================

    def export_results(

        self,

        path="data/processed/association_rules.csv"

    ):

        if self.rules is not None:

            self.rules.to_csv(

                path,

                index=False

            )

    # =====================================================
    # Complete Pipeline
    # =====================================================

    def run(self):

        self.load_data()

        self.build_transactions()

        self.encode_transactions()

        self.generate_itemsets()

        self.generate_rules()

        return self.top_rules()