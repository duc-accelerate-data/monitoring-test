# Design: Q1 Sales Performance Analysis

**Intent ID:** 76192409-4d8d-4a61-934b-40b52d94760d
**Type:** Transformation
**Status:** Design Draft
**Updated:** 2026-04-13

---

## 1. Source Mapping

### Layer Flow: Bronze → Silver → Gold

| Source Table | Staging Model | Mart Model | Build Status |
|--------------|---------------|------------|--------------|
| `salesforce.Opportunity` | `stg_salesforce__opportunity` | `fct_sales` | **new** |
| `salesforce.Account` | `stg_salesforce__account` | `dim_account` | **new** |

### Build Sequence

1. **Source Profiling:** Profile `salesforce.Opportunity` and `salesforce.Account` tables to get actual column names/types
2. **Source Definition:** Create `_salesforce.yml` with source configurations
3. **Staging (Silver):** `stg_salesforce__opportunity`, `stg_salesforce__account`
4. **Marts (Gold):** `dim_account` → `fct_sales`

All models are new — no existing models to modify.

---

## 2. Model Architecture

### Dependency Flow

```
salesforce.Opportunity ──> stg_salesforce__opportunity ──┐
                                                           ├──> fct_sales
salesforce.Account ────────> stg_salesforce__account ──> dim_account ──┘
```

### Layer Assignments

- **Staging (`models/staging/salesforce/`):** 1:1 source mapping, column renaming, basic filters
- **Marts (`models/marts/sales/`):** Business logic, star schema, aggregations

---

## 3. Grain Specification

### `stg_salesforce__opportunity`
**Grain:** One row per opportunity
**Primary Key:** `opportunity_id`

### `stg_salesforce__account`
**Grain:** One row per account
**Primary Key:** `account_id`

### `dim_account`
**Grain:** One row per account (SCD Type 1 — current state only)
**Primary Key:** `account_id`
**Attributes:** `account_name`

### `fct_sales`
**Grain:** One row per closed-won opportunity (detail-level, not aggregated)
**Primary Key:** `opportunity_id` (degenerate dimension)
**Foreign Keys:** `account_id` → `dim_account`
**Measures:** `close_amount`, `days_to_close`
**Dates:** `close_date`, `created_date`
**Rationale:** Detail grain enables flexible aggregation by any dimension (date, account, month, quarter) without rebuilding

---

## 4. Join Plan

### `fct_sales` ← `dim_account`

**Join Key:** `fct_sales.account_id = dim_account.account_id`
**Join Type:** LEFT JOIN (preserve orphaned opportunities if account deleted)
**Cardinality:** Many opportunities : One account
**Fan-out Risk:** None (account_id is unique in dim_account)

**Validation:**
```sql
-- Verify no duplication from join
SELECT opportunity_id, COUNT(*) as cnt
FROM fct_sales
GROUP BY opportunity_id
HAVING cnt > 1
-- Should return 0 rows
```

---

## 5. Materialization Strategy

| Model | Materialization | Rationale |
|-------|----------------|-----------|
| `stg_salesforce__opportunity` | **view** | Lightweight, always fresh, no aggregation |
| `stg_salesforce__account` | **view** | Small dimension, always fresh |
| `dim_account` | **table** | Dimension table for star schema, stable reference |
| `fct_sales` | **incremental** | Large fact table, grows over time, filter on `close_date` with 7-day lookback for late updates |

### Incremental Strategy (`fct_sales`)

```sql
{{ config(
    materialized='incremental',
    unique_key='opportunity_id',
    incremental_strategy='merge'
) }}

{% if is_incremental() %}
-- 7-day lookback window handles late-arriving updates (backdated close dates)
WHERE close_date >= DATEADD(day, -7, (SELECT MAX(close_date) FROM {{ this }}))
{% endif %}
```

**Rationale:** Salesforce allows backdating opportunity close dates. The 7-day lookback ensures late updates are captured during incremental runs.

---

## 6. Testing Plan

### Schema Tests (Generic)

**Staging Models:**
- `stg_salesforce__opportunity`: `unique` + `not_null` on `opportunity_id`
- `stg_salesforce__account`: `unique` + `not_null` on `account_id`

**Marts:**
- `dim_account`: `unique` + `not_null` on `account_id`
- `fct_sales`:
  - `unique` + `not_null` on `opportunity_id`
  - `relationships` to `dim_account(account_id)`
  - `accepted_values` on derived `is_closed_won` (should always be TRUE in staging before fact filter)

### Unit Tests

Defer to sub-agent. Key scenarios:
- Revenue calculation with NULL amounts
- Filtering soft-deleted records
- Date boundary logic (Q1 cutoff)

### Data Quality Tests (Elementary)

**`fct_sales` tests:**
```yaml
models:
  - name: fct_sales
    tests:
      - elementary.volume_anomalies:
          timestamp_column: close_date
          time_bucket:
            period: day
            count: 1
      - elementary.freshness_anomalies:
          timestamp_column: close_date
    columns:
      - name: close_amount
        tests:
          - elementary.column_anomalies
      - name: days_to_close
        tests:
          - elementary.column_anomalies
```

---

## 7. Data Quality Rules

### **Needing Attention**

| Model | Rule | Package | Rationale |
|-------|------|---------|-----------|
| `fct_sales` | `close_amount > 0` | dbt-expectations | Business requirement: zero/negative amounts excluded from revenue |
| `fct_sales` | `days_to_close >= 0` | dbt-utils (expression_is_true) | Data integrity: close_date cannot precede created_date |
| `fct_sales` | `close_date >= '2020-01-01' AND close_date <= CURRENT_DATE` | dbt-expectations (accepted_range) | Data founded 2020; prevent future dates. Confirmed with business |

### **Default (Schema)**

unique + not_null on all PKs; relationships on FKs (`fct_sales_daily.account_id` → `dim_account.account_id`)

---

## 8. Unit Test Scenarios (Brief)

| Model | Scenario | What It Tests |
|-------|----------|---------------|
| `stg_salesforce__opportunity` | Soft-deleted record (`is_deleted=TRUE`) → excluded | Filter logic |
| `fct_sales` | NULL `close_date` → excluded | Date filter handles NULLs |
| `fct_sales` | `is_closed=FALSE` → excluded | Only closed-won deals |
| `fct_sales` | `amount=0` → excluded | Revenue threshold filter |
| `fct_sales` | `close_date < created_date` → `days_to_close` negative | Edge case for data integrity test |

---

## 9. Validation Approach

### Reconciliation Checks

**Row Count:**
```sql
-- Source vs Staging
SELECT COUNT(*) FROM salesforce.Opportunity WHERE is_deleted = FALSE;
SELECT COUNT(*) FROM {{ ref('stg_salesforce__opportunity') }};
-- Should match ±2%
```

**Revenue Total (Q1 2026):**
```sql
-- Fact table
SELECT SUM(close_amount) FROM {{ ref('fct_sales') }}
WHERE close_date >= '2026-01-01' AND close_date < '2026-04-01';
-- Compare to Salesforce report (±2% acceptable)
```

**Grain Validation:**
```sql
-- Verify one row per opportunity in fact
SELECT opportunity_id, COUNT(*)
FROM {{ ref('fct_sales') }}
GROUP BY opportunity_id
HAVING COUNT(*) > 1;
-- Should return 0 rows
```

### Acceptance Criteria Mapping

| Criterion | Validation Query |
|-----------|------------------|
| Q1 revenue ±2% of source | SUM(close_amount) WHERE close_date IN Q1 |
| Top 10 accounts accurate | JOIN to dim_account, GROUP BY, ORDER BY SUM(close_amount) DESC LIMIT 10 |
| Win rate matches manual | Requires additional pipeline metrics (out of scope for initial build) |
| Daily refresh | Check `max(close_date)` advances daily after scheduled run |

---

## 10. Key SQL Transformations

### `stg_salesforce__opportunity`

```sql
SELECT
    id AS opportunity_id,
    account_id,
    name AS opportunity_name,
    amount,
    close_date,
    created_date,
    stage_name,
    is_closed,
    is_won,
    CASE
        WHEN is_closed = TRUE AND is_won = TRUE THEN TRUE
        ELSE FALSE
    END AS is_closed_won,
    is_deleted
FROM {{ source('salesforce', 'opportunity') }}
WHERE is_deleted = FALSE
```

### `fct_sales`

```sql
{{ config(
    materialized='incremental',
    unique_key='opportunity_id',
    incremental_strategy='merge'
) }}

SELECT
    opportunity_id,
    account_id,
    close_date,
    created_date,
    amount AS close_amount,
    DATEDIFF(day, created_date, close_date) AS days_to_close
FROM {{ ref('stg_salesforce__opportunity') }}
WHERE is_closed_won = TRUE
  AND amount > 0
  AND close_date IS NOT NULL
  AND close_date >= '2020-01-01'  -- Company founding year
  AND close_date <= CURRENT_DATE

{% if is_incremental() %}
  -- 7-day lookback for late-arriving updates
  AND close_date >= DATEADD(day, -7, (SELECT MAX(close_date) FROM {{ this }}))
{% endif %}
```

---

## Next Steps

1. Spawn `vd-agent:requirements-reviewer` to validate intent.md
2. Spawn `vd-agent:design-reviewer` to validate this design.md
3. Address blocking feedback
4. Get user approval
5. Initialize dbt project (`dbt_project.yml`, `profiles.yml`)
6. Profile source tables to get actual column names/types
7. Build models bottom-up: staging → dim → fact
8. Spawn test generation sub-agents
9. Code review and commit
