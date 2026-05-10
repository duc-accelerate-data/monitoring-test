# Intent: Salesforce Account and Contact Bronze Ingestion

## Goal

Build a bronze-layer ingestion pipeline to land Salesforce Account and Contact objects into DuckDB. This establishes the raw data foundation for downstream transformation work, ensuring a reliable source-of-truth copy of Salesforce data with full lineage tracking via dlt metadata columns.

## Source System

Salesforce Sales Cloud (via `test_dlt_1` connection configured in `.dlt/config.toml`)

## Target

DuckDB database, bronze layer (schema to be determined)

## Objects in Scope

- **Account** — Salesforce standard object representing companies/organizations
- **Contact** — Salesforce standard object representing individual people

## Success Criteria

1. Bronze tables `account` and `contact` successfully landed in DuckDB
2. All rows have non-null, unique `_dlt_id` values (dlt-generated primary key)
3. Tier 1 data tests passing:
   - `_dlt_id` is not null
   - `_dlt_id` is unique
4. Pipeline executes successfully via `dlt pipeline {pipeline_name} run`
5. Schema contracts pinned (`schema_contract` set appropriately)
6. Pipeline documented with source-to-target mapping

## Out of Scope

- Transformation work (staging, marts, or semantic layers)
- Other Salesforce objects beyond Account and Contact
- Data quality rules beyond Tier 1 tests (unless explicitly requested)
- Real-time or streaming ingestion (batch-based pipeline)

## Open Questions

1. **Target schema name:** Should bronze tables land in `raw_salesforce`, `bronze`, or another schema?
2. **Incremental strategy:** Should we use incremental loads based on `LastModifiedDate` or `SystemModstamp`, or full-refresh on each run?
3. **Field selection:** Should we ingest all fields from Account and Contact, or exclude any specific fields (e.g., system fields, sensitive data)?
4. **Write disposition:** Should we use `merge` (upsert), `replace` (full refresh), or `append` for these tables?
5. **Load frequency:** How often should this pipeline run? (Daily, hourly, on-demand?)
