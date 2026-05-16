"""
notion_pages resource skeleton — schema contract pinning.

Phase 4a (generating-dlt-pipeline) will complete the implementation by
binding the source connection and configuring any resource-specific parameters.
"""

import dlt
from notion import notion_pages as notion_pages_resource


@dlt.resource(
    name="notion_pages",
    write_disposition="append",
    schema_contract={
        "tables": "freeze",      # Single table expected; block unexpected child tables
        "columns": "evolve",     # Notion API may add properties; auto-track new columns
        "data_type": "freeze",   # Type coercion would break downstream; require explicit migration
        # Rationale:
        # - tables=freeze: notion_pages yields a single flat structure (blocks); no child tables expected
        # - columns=evolve: Notion workspace properties can change; new fields should land without pipeline breaks
        # - data_type=freeze: Type drift (e.g., string→int) indicates API contract change; surface explicitly
    },
)
def notion_pages():
    """
    Loads page blocks from all accessible Notion pages.

    Phase 4a implementation will:
    - Pass api_key via section="notion_4" (auto-injected from dlt.secrets)
    - Optional: add page_ids filter if scope narrows in future
    """
    # Placeholder — Phase 4a fills in the full implementation
    yield from notion_pages_resource(
        # api_key auto-injected from dlt.secrets["sources.notion_4.notion.credentials"]
        page_ids=None  # Load all accessible pages
    )
