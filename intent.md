# Intent: Salesforce Pipeline with dlt_test_3

## Goal

Build a dlt ingestion pipeline that extracts data from Salesforce using the `dlt_test_3` connection and loads it into DuckDB bronze tables. This establishes the foundational raw data layer for downstream transformation and analytics.

## Source System

**Salesforce** (via dlt-verified connector, connection ID: `dlt_test_3`)

## Target

**DuckDB**, schema: `src_dlt_test_3`

## Objects in Scope

- **Opportunity** — Sales pipeline opportunities
- **Account** — Customer and prospect accounts
- **Contact** — Individual contacts
- **Lead** — Potential customers

## Success Criteria

1. Bronze tables successfully landed in DuckDB schema `src_dlt_test_3`
2. Each table has `_dlt_id` column (non-null + unique)
3. Tier 1 data tests pass:
   - `_dlt_id` is non-null
   - `_dlt_id` is unique
4. Pipeline executes without errors in dry-run mode
5. Documentation generated for each resource

## Configuration Decisions

**Using dlt verified source settings (reconciled with initial preferences):**

- **Opportunity:** merge mode, incremental on `SystemModstamp` (system field, more reliable than LastModifiedDate)
- **Account:** merge mode, incremental on `LastModifiedDate`
- **Contact:** replace mode, full refresh (no incremental)
- **Lead:** replace mode, full refresh (no incremental)
- **Field exclusions:** None
- **Schema contract:** freeze (strict — no silent schema changes)

## Out of Scope

- Data transformation (staging/marts) — ingestion only
- Cross-object joins or business logic
- Data quality rules beyond Tier 1 tests
- Custom Salesforce objects (standard objects only)
