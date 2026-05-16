"""
notion_2_bronze — dlt ingestion pipeline for notion → DuckDB.

Mixed-shape verified source: notion exports both `@dlt.source` and
standalone `@dlt.resource` symbols at the top level (no single
`notion_source`). A custom `@dlt.source` wrapper binds every loose
resource to the connection's section so dlt resolves credentials against
`[sources.notion_2.notion.credentials]` in
`.dlt/secrets.toml` instead of the resource's bare module-level section.

Configuration & secrets contract
--------------------------------
- Connection metadata is declared in `.dlt/config.toml` under
  `[studio.sources.notion_2]` plus the matching
  `[sources.notion_2.notion]` block that carries
  connector-native config.
- Credentials live in `.dlt/secrets.toml` under
  `[sources.notion_2.notion.credentials]` and resolve
  through dlt's stock provider chain (env override → secrets.toml → KV provider).
- The wrapper below forwards `api_key` (or the equivalent credential field)
  into each loose resource by name. dlt resolves `dlt.secrets.value` on the
  wrapper's parameter first, so the credential reaches the resource already
  bound to the connection-scoped section.
- Never read credentials from process environment or filesystem directly.
"""

import dlt

# Import only the resources in scope for this intent.
# notion_databases excluded due to upstream IndexError on empty titles.
from notion import notion_pages


@dlt.source(section="notion_2", name="notion")
def notion_2_source(api_key: str = dlt.secrets.value):
    """Bind every loose @dlt.resource to the connection's section.

    Each entry in the returned list is either a `@dlt.source` invoked with the
    forwarded credential, or a `@dlt.resource` invoked the same way. dlt walks
    `("sources", "notion_2", "notion")` to resolve any
    field marked `dlt.secrets.value` on the wrapper's signature above.
    """
    return [
        notion_pages(api_key=api_key)
    ]


def run():
    pipeline = dlt.pipeline(
        pipeline_name="notion_2_bronze",
        destination="duckdb",
        dataset_name="src_notion_2",
    )

    # Select only notion_pages resource for this intent
    source = notion_2_source()

    # Apply schema contract: freeze all aspects after successful initial load
    # Tables loaded successfully in Phase 4a, now pinning tables contract
    source.resources["notion_pages"].apply_hints(
        write_disposition="replace",
        schema_contract={
            "tables": "freeze",    # Block new tables (schema is stable)
            "columns": "freeze",   # Block new/renamed columns (schema is stable)
            "data_type": "freeze", # Block type coercions (schema is stable)
        },
    ).add_limit(5)  # Limit to first 5 pages for testing

    load_info = pipeline.run(source.with_resources("notion_pages"))
    print(load_info)


if __name__ == "__main__":
    run()
