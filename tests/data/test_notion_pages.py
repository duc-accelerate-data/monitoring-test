"""
Tier 1 data tests for src_notion_2.notion_pages bronze table.

These tests validate the minimum integrity requirements:
- _dlt_id is NOT NULL on all rows
- _dlt_id is UNIQUE across the table
"""

import pytest


def test_notion_pages_dlt_id_not_null(duckdb_conn):
    """
    Verify _dlt_id is NOT NULL on all rows.

    Every row must have a valid _dlt_id to ensure deduplication and lineage tracking.
    """
    result = duckdb_conn.execute(
        "SELECT COUNT(*) FROM src_notion_2.notion_pages WHERE _dlt_id IS NULL"
    ).fetchone()[0]

    assert result == 0, f"Found {result} rows with null _dlt_id in notion_pages"


def test_notion_pages_dlt_id_unique(duckdb_conn):
    """
    Verify _dlt_id is UNIQUE across the table.

    No duplicate _dlt_id values should exist — this is the deduplication invariant.
    """
    result = duckdb_conn.execute(
        """
        SELECT COUNT(*) AS duplicate_count
        FROM (
            SELECT _dlt_id, COUNT(*) AS n
            FROM src_notion_2.notion_pages
            GROUP BY _dlt_id
            HAVING COUNT(*) > 1
        ) duplicates
        """
    ).fetchone()[0]

    assert result == 0, f"Found {result} duplicate _dlt_id values in notion_pages"
