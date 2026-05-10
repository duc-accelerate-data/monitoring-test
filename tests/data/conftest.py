"""Pytest fixtures for data tests."""

import os
import pytest
import duckdb


@pytest.fixture(scope="session")
def duckdb_conn():
    """Provide a DuckDB connection to the pipeline database.

    The database is expected to exist at the workspace root.
    Tests read from bronze tables created by the ingestion pipeline.
    """
    workspace_root = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    db_path = os.path.join(workspace_root, "salesforce_1_pipeline.duckdb")

    if not os.path.exists(db_path):
        pytest.skip(f"Pipeline database not found at {db_path}")

    conn = duckdb.connect(db_path, read_only=True)
    yield conn
    conn.close()
