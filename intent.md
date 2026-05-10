# Intent: Salesforce Account and Contact Bronze Ingestion

## Goal

Build a dlt ingestion pipeline to land Salesforce Account and Contact objects into DuckDB bronze tables. This establishes the foundational data layer for downstream transformation and analytics on core CRM entities.

## Source System

**Salesforce** (connection: `may_10_3`)

## Target

**DuckDB** bronze layer (schema TBD — typically `raw_salesforce` or similar)

## Objects in Scope

1. Account
2. Contact

## Success Criteria

- Bronze tables created in DuckDB with standard dlt metadata (`_dlt_id`, `_dlt_load_id`, etc.)
- `_dlt_id` columns are non-null and unique (Tier 1 data tests passing)
- Pipeline runs successfully with `schema_contract` set to appropriate strictness level
- All field mappings documented in pipeline documentation

## Out of Scope

- Transformation models (staging, marts, metrics)
- Other Salesforce objects beyond Account and Contact
- Incremental loading strategy (will be determined during discovery phase)
- Data quality tests beyond Tier 1 (to be scoped separately if needed)

## Open Questions

1. What is the target DuckDB schema name for bronze tables?
2. Should incremental loading be enabled, and if so, what is the appropriate cursor field for each object?
3. Are there specific field mappings or transformations required at ingestion time, or should all fields be passed through?
4. What is the desired write disposition for each object (replace, append, merge)?
