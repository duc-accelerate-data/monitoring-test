"""Shared fixtures for unit tests."""

import pytest
import duckdb


@pytest.fixture
def duckdb_conn():
    """In-memory DuckDB connection for testing."""
    conn = duckdb.connect(database=":memory:")
    yield conn
    conn.close()
