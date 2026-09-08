"""
database/schema.py
------------------

Schema Manager for MedIntel360 AI Copilot.

Responsibilities
----------------
• Inspect the SQLite database.
• Discover tables, columns, primary keys and foreign keys.
• Provide AI-ready schema context.
• Serve as the single source of truth for database metadata.

Author: Jainam Gada
"""
from __future__ import annotations
import json
from pathlib import Path


from typing import Any, List

from sqlalchemy import inspect
from sqlalchemy.exc import SQLAlchemyError

from database.connection import DatabaseConnection


class SchemaManager:
    """
    Provides metadata about the MedIntel360 database.

    This class is used by:
        • SQL Generator
        • SQL Validator
        • AI Prompt Builder
        • Future Metadata Generator
    """

    def __init__(self) -> None:

        self.engine = DatabaseConnection.get_engine()
        self.inspector = inspect(self.engine)

        catalog_path = (
            Path(__file__).resolve().parent.parent
            / "metadata"
            / "ai_catalog.json"
        )

        with open(catalog_path, "r", encoding="utf-8") as file:
            self.ai_catalog = json.load(file)
    # ---------------------------------------------------------
    # TABLES
    # ---------------------------------------------------------

    def get_tables(self) -> list[str]:
        """
        Return all user tables.
        """

        tables = self.inspector.get_table_names()

        return sorted(self.get_ai_tables())
    # ---------------------------------------------------------
    # COLUMNS
    # ---------------------------------------------------------

    def get_columns(
        self,
        table_name: str
    ) -> list[dict[str, Any]]:
        """
        Return column metadata for a table.
        """

        columns = self.inspector.get_columns(table_name)

        result = []

        for column in columns:

            result.append(
                {
                    "name": column["name"],
                    "type": str(column["type"]),
                    "nullable": column["nullable"],
                    "default": column.get("default"),
                }
            )

        return result

    # ---------------------------------------------------------
    # PRIMARY KEYS
    # ---------------------------------------------------------

    def get_primary_keys(
        self,
        table_name: str
    ) -> list[str]:

        pk = self.inspector.get_pk_constraint(table_name)

        return pk.get("constrained_columns", [])

    # ---------------------------------------------------------
    # FOREIGN KEYS
    # ---------------------------------------------------------

    def get_foreign_keys(
        self,
        table_name: str
    ) -> list[dict]:

        return self.inspector.get_foreign_keys(table_name)

    # ---------------------------------------------------------
    # COMPLETE DATABASE SCHEMA
    # ---------------------------------------------------------

    def get_database_schema(self) -> dict[str, Any]:
        """
        Return complete database schema.
        """

        schema = {}

        for table in self.get_tables():

            schema[table] = {
                "columns": self.get_columns(table),
                "primary_keys": self.get_primary_keys(table),
                "foreign_keys": self.get_foreign_keys(table),
            }

        return schema

    # ---------------------------------------------------------
    # AI CONTEXT
    # ---------------------------------------------------------

    def get_schema_context(self) -> str:
        """
        Returns a formatted schema description
        for the SQL generation prompt.
        """

        lines = []

        for table in self.get_tables():

            lines.append(f"Table: {table}")

            for column in self.get_columns(table):

                lines.append(
                    f"  - {column['name']} ({column['type']})"
                )

            lines.append("")

        return "\n".join(lines)

    # ---------------------------------------------------------
    # VALIDATION
    # ---------------------------------------------------------

    def table_exists(
        self,
        table_name: str
    ) -> bool:

        return table_name in self.get_tables()

    def column_exists(
        self,
        table_name: str,
        column_name: str
    ) -> bool:

        columns = self.get_columns(table_name)

        return any(
            col["name"] == column_name
            for col in columns
        )
    def get_available_datasets(self) -> list[dict]:
        """
        Returns all AI datasets.
        """

        return self.ai_catalog["datasets"]

    def get_dataset(self, dataset_id: str) -> dict | None:
        """
        Returns a dataset definition.
        """

        for dataset in self.ai_catalog["datasets"]:

            if dataset["id"] == dataset_id:
                return dataset

        return None

    def get_ai_tables(self) -> list[str]:
        """
        Returns only AI-approved tables.
        """

        return [
            dataset["table"]
            for dataset in self.ai_catalog["datasets"]
        ]

    def get_ai_schema(self) -> dict:
        """
        Returns schema only for AI datasets.
        """

        schema = {}

        for dataset in self.ai_catalog["datasets"]:

            table = dataset["table"]

            schema[dataset["id"]] = {

                "name": dataset["name"],

                "table": table,

                "description": dataset["description"],

                "columns": self.get_columns(table),

                "primary_keys": self.get_primary_keys(table),

                "foreign_keys": self.get_foreign_keys(table)
            }

        return schema

    def get_schema_context(self) -> str:
        """
        Returns an AI-friendly schema context.
        """

        context = []

        for dataset in self.ai_catalog["datasets"]:

            table = dataset["table"]

            context.append("=" * 70)

            context.append(
                f"DATASET : {dataset['name']}"
            )

            context.append(
                f"TABLE   : {table}"
            )

            context.append(
                f"PURPOSE : {dataset['description']}"
            )

            context.append("")

            context.append("Columns:")

            for column in self.get_columns(table):

                context.append(
                    f" - {column['name']} ({column['type']})"
                )

            context.append("")

        return "\n".join(context)