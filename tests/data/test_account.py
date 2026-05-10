"""Tier 1 data tests for src_salesforce_1.account table.

These tests validate schema integrity invariants on the bronze table:
- _dlt_id is not null on every row
- _dlt_id is unique across the table

Tier 1 tests run on every pipeline load and are mandatory for every bronze table.
"""
import pytest


def test_account_dlt_id_not_null(duckdb_conn):
    """Test that _dlt_id is not null on every row in account table."""
    result = duckdb_conn.execute(
        "SELECT COUNT(*) FROM src_salesforce_1.account WHERE _dlt_id IS NULL"
    ).fetchone()[0]

    assert result == 0, f"Found {result} rows with null _dlt_id in src_salesforce_1.account"


def test_account_dlt_id_unique(duckdb_conn):
    """Test that _dlt_id is unique across the account table."""
    result = duckdb_conn.execute(
        """
        SELECT COUNT(*) - COUNT(DISTINCT _dlt_id) AS duplicates
        FROM src_salesforce_1.account
        """
    ).fetchone()[0]

    assert result == 0, f"Found {result} duplicate _dlt_id values in src_salesforce_1.account"
