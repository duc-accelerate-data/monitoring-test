# Design: Salesforce Account and Contact Bronze Ingestion

## Progress

| Phase / Gate | Date | Notes |
|---|---|---|
| Phase 0 — Intake | 2026-05-10 | Intent approved |
| Phase 1 — Workspace | 2026-05-10 | dbt + dlt scaffolded, dbt debug passed |
| Phase 2 — Requirements | | In progress |
| Phase 3a — Plan skeleton + change-impact | | |
| Phase 3b — Specialized design (discover schema) | | In progress |
| Phase 3 — Design approval | | |
| Phase 4a — Generate pipeline | | |
| Phase 4b — Unit tests | | |
| Phase 4c — Data tests | | |
| Phase 4d — Validation | | |
| Phase 4d.5 — Audit | | |
| Phase 4e — Contract pinning | | |
| Phase 4f — Code review | | |
| Phase 5a — Schema delta approval | | N/A (fresh build) |
| Phase 5b — Documentation | | |
| Phase 5c — PR Workflow | | |

## Pipeline Inventory

| Source Object | Target Table | Parent / Child | Incremental | Write Disposition | schema_contract | Status | Notes |
|---|---|---|---|---|---|---|---|
| Account | src_dlt_test_1.account | parent | merge on `LastModifiedDate` | merge | freeze/freeze/freeze | pending | Salesforce standard object, mutable records |
| Contact | src_dlt_test_1.contact | parent | none (full refresh) | replace | freeze/freeze/freeze | pending | Salesforce standard object, non-incremental in verified source |

## Artifact List

- `dlt/pipeline.py` — dlt pipeline entry point
- `tests/test_account.py` — pytest unit tests for account resource
- `tests/test_contact.py` — pytest unit tests for contact resource
- `tests/data/test_account_bronze.py` — pytest data tests for account table
- `tests/data/test_contact_bronze.py` — pytest data tests for contact table

## Source Mapping

### Account

**Salesforce Object:** Account
**Target Table:** `src_dlt_test_1.account`
**Write Disposition:** merge (upsert on Id)
**Incremental Strategy:** LastModifiedDate cursor

Standard Salesforce object representing companies/organizations. Mutable records requiring incremental sync.

### Contact

**Salesforce Object:** Contact
**Target Table:** `src_dlt_test_1.contact`
**Write Disposition:** replace (full refresh)
**Incremental Strategy:** None

Standard Salesforce object representing individual people. Configured for full refresh in the verified source.
