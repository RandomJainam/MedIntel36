"""
database/connection.py
----------------------

Centralized SQLAlchemy engine manager for MedIntel360.
All database access must go through this module.

Author: Jainam Gada
"""

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from config import DATABASE_URI


class DatabaseConnection:
    """
    Singleton SQLAlchemy engine manager.
    """

    _engine: Engine | None = None

    @classmethod
    def get_engine(cls) -> Engine:
        """
        Returns a singleton SQLAlchemy engine.
        """

        if cls._engine is None:
            cls._engine = create_engine(
                DATABASE_URI,
                future=True,
                echo=False
            )

        return cls._engine

    @classmethod
    def dispose(cls) -> None:
        """
        Dispose the engine.
        """

        if cls._engine is not None:
            cls._engine.dispose()
            cls._engine = None