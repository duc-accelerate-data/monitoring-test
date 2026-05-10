# Design: Salesforce Data Ingestion Pipeline

## Progress

| Phase / Gate | Date | Notes |
|---|---|---|
| Phase 0 — Issue scope confirmation | 2026-05-10 | Classification: work / ingestion |
| Phase 0 — Type disambiguation (if ambiguous) | N/A | Type clear from request |
| Phase 0 — Deferred-half issue (if mixed) | N/A | Single-type intent |
| Phase 0 — Multi-destination split (if applicable) | N/A | Single destination (DuckDB) |
| Phase 1 — Workspace | 2026-05-10 | Scaffold complete, dbt debug passed, dlt env verified |
| Phase 2 — Requirements | 2026-05-10 | Requirements captured in intent.md |
| Phase 3a — Plan skeleton + change-impact | 2026-05-10 | Complete |
| Phase 3b — Specialized design (profile/discover) | 2026-05-10 | Schema discovery complete. Contact uses replace mode (not merge). |
| Phase 3 — Design approval | 2026-05-10 | Approved for build |
| Phase 4a — Generate (per artifact) | 2026-05-10 | Pipeline generated, 3/4 tables loaded (opportunity_line_item has no source records) |
| Phase 4b — Unit tests | | |
| Phase 4c — Data tests (with tier pick) | | |
| Phase 4d — Validation (golden / fixture replay, if applicable) | | |
| Phase 4d.5 — Audit | | |
| Phase 4e — Contract authoring | | |
| Phase 4f — Code review | | |
| Phase 5a — Schema delta approval | | |
| Phase 5b — Documentation | | |
| Phase 5c — PR Workflow (committed-not-published interim) | | |

## Pipeline Inventory

| Object | Target Table | Write Disposition | Incremental Cursor | schema_contract | Status | Notes |
|---|---|---|---|---|---|---|
| opportunity | src_salesforce_1.opportunity | merge | SystemModstamp | evolve (pending freeze) | generated | Sales opportunities with deal tracking. 38 rows loaded. |
| account | src_salesforce_1.account | merge | LastModifiedDate | evolve (pending freeze) | generated | Customer organizations and individuals. 33 rows loaded. |
| contact | src_salesforce_1.contact | replace | N/A (full refresh) | evolve (pending freeze) | generated | Individual people associated with accounts. Full refresh on each run. 35 rows loaded. |
| opportunity_line_item | src_salesforce_1.opportunity_line_item | merge | SystemModstamp | N/A | skipped | Line items/products for each opportunity. No source records found. |

**Note:** Schema introspection complete. All resources use freeze/freeze/freeze contract for initial pinning to prevent unplanned schema evolution.

## Artifacts

The following files will be created or modified by this intent:

### dlt Pipeline
- `dlt/pipeline.py` - Main pipeline runner (scaffolded, will be updated with resource selection)
- `dlt/resources/<object>.py` - Individual resource files (generated in Phase 4a)

### Tests
- `tests/unit/test_<object>_resource.py` - Unit tests for each resource (Phase 4b)
- `tests/data/test_<object>_data.py` - Data tests for landed tables (Phase 4c)

### Documentation
- `dlt/README.md` - Pipeline documentation (Phase 5b)
- `models/staging/sources.yml` - dbt source definitions (updated in Phase 5b)

### Configuration
- `.dlt/config.toml` - Read-only, managed by Studio `/add-source` (no changes planned)
- `.dlt/secrets.toml` - Read-only, managed by Studio (no changes planned)

## Change Impact

Ingestion track — change impact analysis deferred to Phase 5 (schema delta approval).
