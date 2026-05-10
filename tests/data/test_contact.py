"""Tier 1 data tests for src_salesforce_1.contact table.

Tests the structural integrity of the contact bronze table:
- _dlt_id is non-null on every row (deduplication key integrity)
- _dlt_id is unique across the table (deduplication invariant)
"""

import pytest


def test_contact_dlt_id_not_null(duckdb_conn):
    """Verify _dlt_id is non-null on every row in contact table."""
    result = duckdb_conn.execute(
        "SELECT COUNT(*) FROM src_salesforce_1.contact WHERE _dlt_id IS NULL"
    ).fetchone()[0]
    assert result == 0, f"Found {result} rows with null _dlt_id in contact table"


def test_contact_dlt_id_unique(duckdb_conn):
    """Verify _dlt_id is unique across the contact table."""
    result = duckdb_conn.execute(
        """
        SELECT COUNT(*) - COUNT(DISTINCT _dlt_id) AS duplicate_count
        FROM src_salesforce_1.contact
        """
    ).fetchone()[0]
    assert result == 0, f"Found {result} duplicate _dlt_id values in contact table"
