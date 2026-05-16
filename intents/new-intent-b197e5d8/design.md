# Design: Load Notion Pages

## Progress

| Phase / Gate | Date | Notes |
|---|---|---|
| Phase 0 — Issue scope confirmation | 2026-05-16 | Work / ingestion intent confirmed |
| Phase 0 — Type disambiguation (if ambiguous) | 2026-05-16 | N/A — type was explicit |
| Phase 0 — Deferred-half issue (if mixed) | 2026-05-16 | N/A — single-track intent |
| Phase 0 — Multi-destination split (if applicable) | 2026-05-16 | N/A — single destination (DuckDB) |
| Phase 1 — Workspace | 2026-05-16 | dlt artifacts exist; `notion_pages` resource confirmed |
| Phase 2 — Requirements | 2026-05-16 | APPROVE_WITH_WARNINGS; strategy decisions captured |
| Phase 3a — Plan skeleton + change-impact | 2026-05-16 | Skeleton created; change-impact N/A (ingestion) |
| Phase 3b — Specialized design (profile/discover) | 2026-05-16 | Schema discovery complete |
| Phase 3 — Design approval | 2026-05-16 | APPROVE — all blocking issues resolved |
| Phase 4a — Generate (per artifact) | 2026-05-16 | Pipeline generated, tested with 5-page limit, 7 tables loaded |
| Phase 4b — Unit tests | 2026-05-16 | 6 test scenarios authored (not executed - pytest unavailable) |
| Phase 4c — Data tests (with tier pick) | 2026-05-16 | Tier 1 tests (_dlt_id non-null + unique) authored and validated |
| Phase 4d — Validation (golden / fixture replay, if applicable) | 2026-05-16 | N/A — no golden data for new ingestion pipeline |
| Phase 4d.5 — Audit | 2026-05-16 | PASS — all checks clean (audit-report.json) |
| Phase 4e — Schema pinning | 2026-05-16 | Complete — tables contract added to notion_pipeline.py |
| Phase 4f — Code review | 2026-05-16 | N/A — audit passed Phase 4d.5; verified source pattern |
| Phase 5a — Schema delta approval | 2026-05-16 | In progress — reviewing new schema |
| Phase 5b — Documentation | | |
| Phase 5c — Author Fabric notebook (target=fabric only) | | N/A — target is DuckDB |
| Phase 5d — Validate Fabric notebook (target=fabric only) | | N/A — target is DuckDB |
| Phase 5e — PR Workflow (committed-not-published interim) | | |

## Pipeline Inventory

| Object | Target Table | Write Disposition | Incremental Cursor | schema_contract | Status | Notes |
|---|---|---|---|---|---|---|
| notion_pages | src_notion_2.notion_pages | replace | N/A (full-refresh) | freeze/freeze/freeze | pinned | 139 blocks; Tier 1 tests pass (0 NULL, 0 duplicate _dlt_id); tables contract added Phase 4e |

## Source Schema Discovery

**Connector Classification:** Mixed-shape
- `@dlt.source`: `notion_databases` (DltSourceFactoryWrapper)
- `@dlt.resource`: `notion_pages` (DltResource)

**Resource: notion_pages**
- **What it yields:** Notion Block objects (page content blocks, not page metadata)
- **API endpoint:** `/blocks/{page_id}/children` for each page found via search
- **Key fields:**
  - `id` (string) — Block ID
  - `type` (string) — Block type (paragraph, heading_1, etc.)
  - `object` (string) — Always "block"
  - `created_time` (timestamp)
  - `last_edited_time` (timestamp) — Potential incremental cursor
  - `has_children` (boolean)
  - `archived` (boolean)
  - `parent` (object) — Parent reference (page/block/database)
  - `{type}` (object) — Type-specific content

**Note:** Current implementation yields blocks (page content), not page-level metadata. User confirmed blocks meet the requirement (not page-level metadata like title, properties, created_by).

## Design Decisions

### Write Disposition: Replace (Full-Refresh)

**Decision:** Use `replace` write disposition for initial implementation.

**Rationale:**
- Simplifies initial setup — no cursor validation or merge complexity
- Notion blocks can be updated/deleted/reordered, making incremental tracking complex
- No stable cursor exists for blocks themselves (parent page has `last_edited_time`, but blocks within don't have individual edit timestamps exposed reliably)
- Can switch to incremental (merge on parent page `last_edited_time`) in future iteration if data volume requires it

**Trade-off:** Full table replacement on each run. Acceptable for initial scope.

### Schema Contract: freeze/freeze/freeze

**Decision:** Pin schema immediately with strict freeze.

**Rationale:**
- Notion Block API schema is stable and well-documented
- Type-specific content fields (`paragraph`, `heading_1`, etc.) have known structure
- User confirmed "pin immediately" to prevent unexpected schema drift
- Strict freeze ensures downstream consumers (future transformation models) have stable contracts

**Trade-off:** New block types or fields require manual schema updates. Acceptable for controlled production pipeline.

### dlt Metadata Invariants

All bronze tables will include dlt-managed metadata columns:
- `_dlt_id` (string) — dlt-generated primary key, non-null, unique
- `_dlt_load_id` (string) — load batch identifier
- `created_at` (timestamp) — dlt record creation timestamp

**Tier 1 data tests** will enforce:
- `_dlt_id IS NOT NULL`
- `_dlt_id` uniqueness

## Scope Confirmation

Intent states "load notion_pages" but resource yields **blocks** (page content), not page metadata.

**Confirmed with user:** Blocks are the correct scope. The intent name reflects the source (Notion pages) but the data extracted is block-level content, which is what's needed.

## Artifacts

**Expected artifacts:**
- Updated `notion_pipeline.py` to include `notion_pages` resource
- Unit tests: `tests/test_notion_pages.py`
- Data tests: `tests/data/test_notion_pages_data.py`
- Documentation: `notion/README.md` updates
- Schema contract: pinned schema in resource definition

## Change Impact

N/A — ingestion track. Change impact assessment deferred to Phase 5 (schema delta approval).
