"""Unit tests for the notion_pages dlt resource.

These tests verify the resource's behavior across various scenarios:
- Happy path with multiple pages and blocks
- Empty search results
- Pages with zero blocks
- Page filtering via page_ids parameter
- Mixed scenarios (some pages with blocks, some without)
"""

from unittest.mock import MagicMock, patch

import pytest

from notion import notion_pages


def test_notion_pages_happy_path_multiple_pages_with_blocks():
    """
    Given: Notion search returns 2 pages, each with 3 child blocks
    When: resource is executed without page_ids filter
    Then: 2 block lists are yielded, each containing 3 blocks
    """
    mock_client = MagicMock()

    # Mock search to return 2 pages
    mock_client.search.return_value = [
        {"id": "page-1", "object": "page"},
        {"id": "page-2", "object": "page"},
    ]

    # Mock fetch_resource to return 3 blocks for each page
    mock_client.fetch_resource.side_effect = [
        {"results": [{"id": "block-1-1"}, {"id": "block-1-2"}, {"id": "block-1-3"}]},
        {"results": [{"id": "block-2-1"}, {"id": "block-2-2"}, {"id": "block-2-3"}]},
    ]

    with patch("notion.NotionClient", return_value=mock_client):
        results = list(notion_pages(api_key="test-key"))

    assert len(results) == 2, (
        f"Expected 2 block lists to be yielded, got {len(results)}"
    )
    assert len(results[0]) == 3, (
        f"Expected first page to yield 3 blocks, got {len(results[0])}"
    )
    assert len(results[1]) == 3, (
        f"Expected second page to yield 3 blocks, got {len(results[1])}"
    )
    assert results[0][0]["id"] == "block-1-1"
    assert results[1][0]["id"] == "block-2-1"


def test_notion_pages_empty_search_response():
    """
    Given: Notion search returns zero pages
    When: resource is executed
    Then: no blocks are yielded and no exception is raised
    """
    mock_client = MagicMock()
    mock_client.search.return_value = []

    with patch("notion.NotionClient", return_value=mock_client):
        results = list(notion_pages(api_key="test-key"))

    assert len(results) == 0, (
        f"Expected zero block lists for empty search, got {len(results)}"
    )
    mock_client.fetch_resource.assert_not_called()


def test_notion_pages_page_with_zero_blocks():
    """
    Given: Notion search returns 1 page with zero child blocks
    When: resource is executed
    Then: no blocks are yielded because the if blocks: guard prevents empty yields
    """
    mock_client = MagicMock()
    mock_client.search.return_value = [{"id": "page-1", "object": "page"}]
    mock_client.fetch_resource.return_value = {"results": []}

    with patch("notion.NotionClient", return_value=mock_client):
        results = list(notion_pages(api_key="test-key"))

    assert len(results) == 0, (
        f"Expected zero block lists for page with no blocks, got {len(results)}"
    )
    mock_client.fetch_resource.assert_called_once_with(
        "blocks", "page-1", "children"
    )


def test_notion_pages_page_ids_filter_matches():
    """
    Given: Notion search returns 3 pages but page_ids=['page-1'] is provided
    When: resource is executed with page_ids filter
    Then: only the blocks from page-1 are yielded
    """
    mock_client = MagicMock()
    mock_client.search.return_value = [
        {"id": "page-1", "object": "page"},
        {"id": "page-2", "object": "page"},
        {"id": "page-3", "object": "page"},
    ]

    # All pages have blocks, but only page-1 should be yielded
    mock_client.fetch_resource.side_effect = [
        {"results": [{"id": "block-1-1"}]},
        {"results": [{"id": "block-2-1"}]},
        {"results": [{"id": "block-3-1"}]},
    ]

    with patch("notion.NotionClient", return_value=mock_client):
        results = list(notion_pages(page_ids=["page-1"], api_key="test-key"))

    assert len(results) == 1, (
        f"Expected 1 block list for page_ids=['page-1'], got {len(results)}"
    )
    assert results[0][0]["id"] == "block-1-1", (
        f"Expected block from page-1, got: {results[0][0]['id']}"
    )


def test_notion_pages_page_ids_filter_no_match():
    """
    Given: Notion search returns 2 pages but page_ids=['non-existent-id'] is provided
    When: resource is executed with page_ids filter
    Then: no blocks are yielded
    """
    mock_client = MagicMock()
    mock_client.search.return_value = [
        {"id": "page-1", "object": "page"},
        {"id": "page-2", "object": "page"},
    ]

    mock_client.fetch_resource.side_effect = [
        {"results": [{"id": "block-1-1"}]},
        {"results": [{"id": "block-2-1"}]},
    ]

    with patch("notion.NotionClient", return_value=mock_client):
        results = list(notion_pages(page_ids=["non-existent-id"], api_key="test-key"))

    assert len(results) == 0, (
        f"Expected zero block lists for non-matching page_ids, got {len(results)}"
    )


def test_notion_pages_mixed_pages_with_and_without_blocks():
    """
    Given: Notion search returns 3 pages: page-1 has 2 blocks, page-2 has 0 blocks, page-3 has 1 block
    When: resource is executed without filter
    Then: 2 block lists are yielded (page-1 and page-3), page-2 is skipped due to empty blocks
    """
    mock_client = MagicMock()
    mock_client.search.return_value = [
        {"id": "page-1", "object": "page"},
        {"id": "page-2", "object": "page"},
        {"id": "page-3", "object": "page"},
    ]

    mock_client.fetch_resource.side_effect = [
        {"results": [{"id": "block-1-1"}, {"id": "block-1-2"}]},
        {"results": []},  # page-2 has no blocks
        {"results": [{"id": "block-3-1"}]},
    ]

    with patch("notion.NotionClient", return_value=mock_client):
        results = list(notion_pages(api_key="test-key"))

    assert len(results) == 2, (
        f"Expected 2 block lists (page-1 and page-3), got {len(results)}"
    )
    assert len(results[0]) == 2, (
        f"Expected page-1 to yield 2 blocks, got {len(results[0])}"
    )
    assert len(results[1]) == 1, (
        f"Expected page-3 to yield 1 block, got {len(results[1])}"
    )
    assert results[0][0]["id"] == "block-1-1"
    assert results[1][0]["id"] == "block-3-1"
