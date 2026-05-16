# Intent: Load Notion Pages

## Goal

Build a dlt ingestion pipeline to extract Notion pages data from the `notion_2` connection and land it in the bronze layer of DuckDB. This enables downstream analytics and transformation work on Notion content.

## Source System

**Notion** (connection: `notion_2`)
- Connector: `notion` (dlt-verified source)
- Authentication: Configured via `notion_2` connection

## Target

**DuckDB**
- Schema: `src_notion_2`
- Location: `./data/test.duckdb` (dev), `test.duckdb` (prod)

## Objects in Scope

- `notion_pages` — Primary resource for loading Notion page content

## Success Criteria

1. Bronze table `src_notion_2.notion_pages` successfully landed
2. All rows have non-null `_dlt_id` (dlt-managed primary key)
3. `_dlt_id` values are unique
4. Tier 1 data tests passing (non-null + unique on `_dlt_id`)
5. Pipeline schema pinned with `schema_contract` to prevent unintended schema drift

## Out of Scope

- Other Notion resources (`notion_databases`, blocks, comments, users)
- Transformation models (staging, marts) — deferred to future transformation intent
- Notion database-specific content extraction

## Open Questions

1. **Incremental strategy:** Should the pipeline use incremental loading (merge with cursor) or full-refresh (replace)? What is the appropriate cursor field if incremental?
2. **Filters:** Are there specific workspaces, date ranges, or page types to filter?
3. **Schema evolution:** What properties/metadata from Notion pages are critical to capture? Should we freeze the schema immediately or allow evolution during initial discovery?
