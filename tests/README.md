# Test Suite

Unit tests for dlt resources and dbt models.

## Setup

Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

## Running Tests

Run all tests:

```bash
pytest tests/
```

Run specific test file:

```bash
pytest tests/unit/test_notion_pages.py -v
```

Run specific test function:

```bash
pytest tests/unit/test_notion_pages.py::test_notion_pages_happy_path_multiple_pages_with_blocks -v
```

## Test Structure

- `tests/unit/` - Unit tests for dlt resources
- `tests/unit/conftest.py` - Shared fixtures (DuckDB connection, etc.)

## Writing Tests

Each test follows the Given-When-Then pattern:

```python
def test_resource_scenario():
    """
    Given: Initial state and test fixtures
    When: Action being tested
    Then: Expected outcome
    """
    # Arrange
    mock_client = MagicMock()
    mock_client.method.return_value = test_data
    
    # Act
    with patch("module.Client", return_value=mock_client):
        results = list(resource_function(api_key="test"))
    
    # Assert
    assert len(results) == expected_count, (
        f"Expected {expected_count}, got {len(results)}"
    )
```

## Test Scenarios

All test scenarios are documented in `test-spec.json` at the project root.
