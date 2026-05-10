# Intent: Salesforce Pipeline with dlt_test_3

## Goal

Build a dlt ingestion pipeline that extracts data from Salesforce using the `dlt_test_3` connection and loads it into DuckDB bronze tables. This establishes the foundational raw data layer for downstream transformation and analytics.

## Source System

**Salesforce** (via dlt-verified connector, connection ID: `dlt_test_3`)

## Target

**DuckDB**, schema: `src_dlt_test_3`

## Objects in Scope

To be determined — awaiting user input on which Salesforce objects (e.g., Opportunity, Account, Contact, Lead, Campaign) should be included in this pipeline.

## Success Criteria

1. Bronze tables successfully landed in DuckDB schema `src_dlt_test_3`
2. Each table has `_dlt_id` column (non-null + unique)
3. Tier 1 data tests pass:
   - `_dlt_id` is non-null
   - `_dlt_id` is unique
4. Pipeline executes without errors in dry-run mode
5. Documentation generated for each resource

## Out of Scope

- Data transformation (staging/marts) — ingestion only
- Cross-object joins or business logic
- Incremental load configuration (unless explicitly requested)
- Data quality rules beyond Tier 1 tests

## Open Questions

1. **Which Salesforce objects should be ingested?** (e.g., Opportunity, Account, Contact, Lead, etc.)
2. **Should incremental loading be configured?** If yes, which cursor field (e.g., LastModifiedDate, SystemModstamp)?
3. **Are there specific fields to exclude** from any objects?
4. **Write disposition preference:** merge (update existing rows) or replace (full refresh)?
