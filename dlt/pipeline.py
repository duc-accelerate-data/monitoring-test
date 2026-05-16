"""
notion_bronze — dlt ingestion pipeline for notion → DuckDB.

Mixed-shape verified source: notion exports both `@dlt.source` and
standalone `@dlt.resource` symbols at the top level (no single
`notion_source`). A custom `@dlt.source` wrapper binds every loose
resource to the connection's section so dlt resolves credentials against
`[sources.notion_4.notion.credentials]` in
`.dlt/secrets.toml` instead of the resource's bare module-level section.

Configuration & secrets contract
--------------------------------
- Connection metadata is declared in `.dlt/config.toml` under
  `[studio.sources.notion_4]` plus the matching
  `[sources.notion_4.notion]` block that carries
  connector-native config.
- Credentials live in `.dlt/secrets.toml` under
  `[sources.notion_4.notion.credentials]` and resolve
  through dlt's stock provider chain (env override → secrets.toml → KV provider).
- The wrapper below forwards `api_key` (or the equivalent credential field)
  into each loose resource by name. dlt resolves `dlt.secrets.value` on the
  wrapper's parameter first, so the credential reaches the resource already
  bound to the connection-scoped section.
- Never read credentials from process environment or filesystem directly.
"""

import dlt

# Import every top-level decorated symbol the Pipeline Inventory needs.
from notion import notion_pages


@dlt.source(section="notion_4", name="notion")
def notion_4_source(api_key: str = dlt.secrets.value):
    """Bind every loose @dlt.resource to the connection's section.

    Each entry in the returned list is either a `@dlt.source` invoked with the
    forwarded credential, or a `@dlt.resource` invoked the same way. dlt walks
    `("sources", "notion_4", "notion")` to resolve any
    field marked `dlt.secrets.value` on the wrapper's signature above.
    """
    return [
        notion_pages(api_key=api_key)
    ]


def run():
    pipeline = dlt.pipeline(
        pipeline_name="notion_bronze",
        destination="duckdb",
        dataset_name="src_notion_4",
    )

    # Apply schema contract and write disposition hints
    src = notion_4_source()
    src.resources["notion_pages"].apply_hints(
        write_disposition="append",
        schema_contract={
            "columns": "evolve",
            "data_type": "freeze",
        },
    )

    load_info = pipeline.run(src.with_resources("notion_pages"))
    print(load_info)


if __name__ == "__main__":
    run()
