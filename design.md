# Design: Salesforce Pipeline with dlt_test_3

## Progress

| Phase / Gate | Date | Notes |
|---|---|---|
| Phase 0 — Issue scope confirmation | 2026-05-10 | ✅ User request classified as work/ingestion |
| Phase 0 — Type disambiguation (if ambiguous) | - | N/A — type was clear |
| Phase 0 — Deferred-half issue (if mixed) | - | N/A — ingestion only |
| Phase 0 — Multi-destination split (if applicable) | - | N/A — single destination (DuckDB) |
| Phase 1 — Workspace | 2026-05-10 | ✅ dbt + dlt scaffolded, debug passed |
| Phase 2 — Requirements | 2026-05-10 | ✅ Objects and config resolved |
| Phase 3a — Plan skeleton + change-impact | 2026-05-10 | In progress |
| Phase 3b — Specialized design (profile/discover) | | |
| Phase 3 — Design approval | | |
| Phase 4a — Generate (per artifact) | | |
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
| Opportunity | src_dlt_test_3.opportunity | merge | SystemModstamp | freeze | pending | Verified source uses SystemModstamp (system field) |
| Account | src_dlt_test_3.account | merge | LastModifiedDate | freeze | pending | Customer and prospect accounts |
| Contact | src_dlt_test_3.contact | replace | None (full refresh) | freeze | pending | Verified source uses replace mode |
| Lead | src_dlt_test_3.lead | replace | None (full refresh) | freeze | pending | Verified source uses replace mode |

## Change Impact

No existing artifacts impacted — fresh build target (no prior dlt pipelines in workspace).

## Artifact List

To be populated by Phase 3b (source schema discovery) and Phase 4a (pipeline generation):

- `dlt/pipeline.py` — Main pipeline orchestration (placeholder exists, will be populated with resource list)
- `sources/salesforce/` — dlt verified source tree (already present via Studio /add-source)
- `.dlt/config.toml` — Connection configuration (read-only, managed by Studio)
- `.dlt/secrets.toml` — Credentials (read-only, managed by Studio)
- `tests/ingestion/test_opportunity.py` — Unit tests (Phase 4b)
- `tests/ingestion/test_account.py` — Unit tests (Phase 4b)
- `tests/ingestion/test_contact.py` — Unit tests (Phase 4b)
- `tests/ingestion/test_lead.py` — Unit tests (Phase 4b)
- `tests/data/test_opportunity_data.py` — Data tests (Phase 4c)
- `tests/data/test_account_data.py` — Data tests (Phase 4c)
- `tests/data/test_contact_data.py` — Data tests (Phase 4c)
- `tests/data/test_lead_data.py` — Data tests (Phase 4c)

## Source Schema Discovery

**Completed:** 2026-05-10

Introspected `salesforce/__init__.py` verified source (dlt-verified connector).

### Resources Found

All 4 requested objects are available as dlt resources:

1. **opportunity** — `@dlt.resource(write_disposition="merge")` with incremental on `SystemModstamp`
2. **account** — `@dlt.resource(write_disposition="merge")` with incremental on `LastModifiedDate`
3. **contact** — `@dlt.resource(write_disposition="replace")` with no incremental (full refresh)
4. **lead** — `@dlt.resource(write_disposition="replace")` with no incremental (full refresh)

### Configuration Reconciliation

User originally requested `merge + LastModifiedDate` for all objects, but the verified source defines different settings for Opportunity, Contact, and Lead. **Decision:** Use verified source as-is (battle-tested by dlt team).

### Schema Contract

All objects set to `freeze` for initial pinning. This means:
- New columns in source → pipeline fails (explicit schema evolution required)
- Column type changes → pipeline fails
- Column removals → pipeline fails

This strict contract ensures no silent schema drift.
