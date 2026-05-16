"""
Shared fixtures for data tests.

Provides DuckDB connection to the bronze layer database.
"""

import os
from pathlib import Path

import duckdb
import pytest


@pytest.fixture(scope="session")
def duckdb_conn():
    """
    DuckDB connection to the bronze layer database.

    Yields a read-only connection for data integrity tests.
    """
    # Locate the bronze database relative to repo root
    repo_root = Path(__file__).parent.parent.parent
    db_path = repo_root / "notion_2_bronze.duckdb"

    if not db_path.exists():
        pytest.skip(f"Bronze database not found at {db_path}")

    conn = duckdb.connect(str(db_path), read_only=True)
    yield conn
    conn.close()
