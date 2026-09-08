"""
=========================================================
MedIntel360
Database Manager
=========================================================
Central Database Utility

Author: Jainam Gada
Project: MedIntel360
"""

from pathlib import Path

import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import text

from config import (
    DATABASE_URI,
    WAREHOUSE_DIR
)


class DatabaseManager:

    """
    Common database manager used across the project.

    Responsibilities
    ----------------
    • Read tables
    • Save tables
    • Execute SQL
    • Export CSV
    • Validation
    """

    def __init__(self):

        self.engine = create_engine(DATABASE_URI)

        self.inspector = inspect(self.engine)

    # ----------------------------------------------------

    def load_table(self, table_name: str) -> pd.DataFrame:

        print(f"📥 Loading table : {table_name}")

        return pd.read_sql_table(
            table_name,
            self.engine
        )

    # ----------------------------------------------------

    def save_table(
        self,
        dataframe: pd.DataFrame,
        table_name: str
    ):

        dataframe.to_sql(
            table_name,
            self.engine,
            if_exists="replace",
            index=False
        )

        print(f"💾 Saved : {table_name}")

    # ----------------------------------------------------

    def export_csv(
        self,
        dataframe: pd.DataFrame,
        filename: str,
        folder: Path = WAREHOUSE_DIR
    ):

        folder.mkdir(
            parents=True,
            exist_ok=True
        )

        dataframe.to_csv(
            folder / f"{filename}.csv",
            index=False
        )

        print(f"📄 Exported : {filename}.csv")

    # ----------------------------------------------------

    def save_and_export(
        self,
        dataframe: pd.DataFrame,
        table_name: str,
        folder: Path = WAREHOUSE_DIR
    ):

        self.save_table(
            dataframe,
            table_name
        )

        self.export_csv(
            dataframe,
            table_name,
            folder
        )

    # ----------------------------------------------------

    def execute_query(
        self,
        query: str
    ) -> pd.DataFrame:

        return pd.read_sql(
            text(query),
            self.engine
        )

    # ----------------------------------------------------

    def execute_sql(
        self,
        query: str
    ):

        with self.engine.begin() as connection:

            connection.execute(
                text(query)
            )

    # ----------------------------------------------------

    def table_exists(
        self,
        table_name: str
    ) -> bool:

        return self.inspector.has_table(
            table_name
        )

    # ----------------------------------------------------

    def list_tables(self):

        return self.inspector.get_table_names()

    # ----------------------------------------------------

    def get_table_columns(
        self,
        table_name: str
    ):

        return [

            column["name"]

            for column in

            self.inspector.get_columns(
                table_name
            )

        ]

    # ----------------------------------------------------

    def dataframe_summary(
        self,
        dataframe: pd.DataFrame
    ):

        print()

        print("=" * 60)

        print("DATAFRAME SUMMARY")

        print("=" * 60)

        print(f"Rows        : {len(dataframe)}")

        print(f"Columns     : {len(dataframe.columns)}")

        print(f"Duplicates  : {dataframe.duplicated().sum()}")

        print(
            f"Missing     : {dataframe.isnull().sum().sum()}"
        )

        print("=" * 60)

        print()

    # ----------------------------------------------------

    def close(self):

        self.engine.dispose()