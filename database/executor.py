"""
database/executor.py
--------------------

Safe SQL execution layer for MedIntel360.

Responsibilities
----------------
- Execute SELECT queries.
- Return structured database results.
- Handle database execution errors.
- Limit the number of returned rows.
- Keep SQLAlchemy objects out of the rest of the application.

Author: Jainam Gada
"""

from dataclasses import dataclass, field
from typing import Any

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from database.connection import DatabaseConnection


# ==================================================
# DATABASE EXECUTION RESULT
# ==================================================

@dataclass
class DatabaseExecutionResult:

    success: bool

    columns: list[str] = field(
        default_factory=list
    )

    rows: list[dict[str, Any]] = field(
        default_factory=list
    )

    row_count: int = 0

    error: str | None = None

    truncated: bool = False


# ==================================================
# DATABASE EXECUTOR
# ==================================================

class DatabaseExecutor:

    def __init__(
        self,
        max_rows: int = 1000
    ):

        if max_rows <= 0:

            raise ValueError(
                "max_rows must be greater than zero."
            )

        self.max_rows = max_rows

        self.engine = (
            DatabaseConnection.get_engine()
        )

    # --------------------------------------------------
    # EXECUTE SQL
    # --------------------------------------------------

    def execute(
        self,
        sql: str
    ) -> DatabaseExecutionResult:

        # ----------------------------------------------
        # Basic input validation
        # ----------------------------------------------

        if not sql or not sql.strip():

            return DatabaseExecutionResult(

                success=False,

                error="SQL cannot be empty."
            )

        # ----------------------------------------------
        # Defensive SELECT check
        # ----------------------------------------------

        if not sql.strip().upper().startswith("SELECT"):

            return DatabaseExecutionResult(

                success=False,

                error=(
                    "Only SELECT queries may be executed."
                )
            )

        # ----------------------------------------------
        # Execute query
        # ----------------------------------------------

        try:

            with self.engine.connect() as connection:

                result = connection.execute(
                    text(sql)
                )

                columns = list(
                    result.keys()
                )

                # --------------------------------------
                # Read only max_rows + 1 rows.
                #
                # The extra row tells us whether the
                # result was larger than the safety limit.
                # --------------------------------------

                fetched_rows = []

                for row in result:

                    fetched_rows.append(row)

                    if len(fetched_rows) > self.max_rows:

                        break

                truncated = (
                    len(fetched_rows)
                    > self.max_rows
                )

                if truncated:

                    fetched_rows = (
                        fetched_rows[:self.max_rows]
                    )

                rows = [
                    dict(zip(columns, row))
                    for row in fetched_rows
                ]

                return DatabaseExecutionResult(

                    success=True,

                    columns=columns,

                    rows=rows,

                    row_count=len(rows),

                    truncated=truncated
                )

        except SQLAlchemyError as error:

            return DatabaseExecutionResult(

                success=False,

                error=str(error)
            )