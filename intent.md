# Intent: Salesforce Data Ingestion Pipeline

## Goal

Create a dlt ingestion pipeline to land Salesforce data into DuckDB bronze layer using the pre-configured salesforce_1 source connection. This provides a foundation for downstream transformation and analytics by establishing a raw data layer with change tracking and data quality controls.

## Source System

**Salesforce Sales Cloud** via the salesforce_1 connection configured in `.dlt/config.toml`.

## Target

**DuckDB** database, schema `src_salesforce_1`, located at the path specified in `vd-domain.yml` (dev: `./data/dev.duckdb`).

## Objects in Scope

Core sales objects (all incremental merge mode):

1. **Opportunity** - sales opportunities with deal tracking
2. **Account** - customer organizations and individuals
3. **Contact** - individual people associated with accounts
4. **OpportunityLineItem** - line items/products for each opportunity

All objects use **merge** write disposition with `LastModifiedDate` as the incremental cursor field.

## Success Criteria

1. Bronze tables landed in DuckDB schema `src_salesforce_1` with all selected Salesforce objects
2. Each table includes dlt metadata columns (`_dlt_id`, `_dlt_load_id`) with:
   - `_dlt_id` is non-null and unique (Tier 1 data tests passing)
3. Incremental objects (merge mode) configured with appropriate cursor field (typically `LastModifiedDate`)
4. Schema contract pinned with `freeze/freeze/freeze` to prevent unplanned evolution
5. Pipeline documentation covering source system, target tables, write disposition, and incremental strategy
6. Unit tests passing for resource extraction logic
7. Data tests (Tier 1 minimum) passing for all landed tables

## Out of Scope

- Transformation or modeling of bronze data (handled separately via dbt)
- Backfill strategies or historical data loads beyond standard incremental logic
- Custom field mappings or transformations (bronze layer is 1:1 with source)
- Integration with downstream marts or semantic layers

## Open Questions

1. **Data volume expectations** - are there any objects with especially large row counts that need special consideration?
2. **Tier 2 data tests** - are additional data quality tests needed beyond Tier 1 (e.g., referential integrity, value constraints)?
