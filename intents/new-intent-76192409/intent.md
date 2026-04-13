# Intent: Q1 Sales Performance Analysis

**Intent ID:** 76192409-4d8d-4a61-934b-40b52d94760d
**Type:** Transformation
**Status:** Requirements Draft
**Created:** 2026-04-13

---

## Business Context

Stakeholders need visibility into Q1 2026 (Jan-Mar) sales performance to:
- Evaluate revenue achievement against targets
- Identify top-performing accounts and opportunities
- Understand pipeline conversion metrics
- Support quarterly business reviews and forecasting

This analysis will serve sales leadership, revenue operations, and executive reporting.

---

## Goals

1. **Revenue Reporting:** Calculate total closed-won revenue for Q1 2026
2. **Pipeline Metrics:** Analyze opportunity conversion rates and average deal size
3. **Account Performance:** Identify top accounts by revenue and opportunity count
4. **Trend Analysis:** Enable month-over-month comparison within Q1
5. **Reusable Infrastructure:** Build models that support ongoing sales analysis beyond Q1

---

## Business Rules

### Revenue Recognition

- Only `is_closed_won = TRUE` opportunities count toward revenue
- `close_date` determines which quarter/month revenue is attributed to
- Exclude deleted/archived records (`is_deleted = FALSE`)
- Amount must be > 0

```sql
WHERE is_closed_won = TRUE
  AND is_deleted = FALSE
  AND amount > 0
  AND close_date >= '2026-01-01'
  AND close_date < '2026-04-01'
```

### Pipeline Metrics

- **Win Rate:** (Closed Won Count) / (Total Closed Count) where Total Closed = Won + Lost
- **Average Deal Size:** SUM(amount) / COUNT(opportunities) for closed-won only
- **Pipeline Velocity:** Days from created_date to close_date for closed-won deals

### Account Aggregations

- Group by `account_id` to roll up opportunity-level metrics
- Include accounts with zero Q1 revenue if they had active opportunities in Q1

---

## Acceptance Criteria

- [ ] Query returns total Q1 2026 closed-won revenue within ±2% of source system
- [ ] Top 10 accounts by revenue are accurate and ranked correctly
- [ ] Win rate calculation matches sales ops manual reports
- [ ] Data refreshes daily to include prior-day closes
- [ ] Results available via dbt Semantic Layer for BI tool consumption
- [ ] All models compile and pass schema tests (unique, not_null, relationships)
- [ ] Documentation includes column descriptions and metric definitions

---

## Open Questions

1. **Data Source:** Which CRM system contains opportunity data? (Salesforce, HubSpot, other?)
2. **Source Availability:** Has the source already been ingested into the lakehouse, or do we need to set up ingestion first?
3. **Account Dimension:** Do we need account attributes (industry, segment, region) or just IDs?
4. **Historical Scope:** Should models support analysis beyond Q1, or is this Q1-specific?
5. **Workspace/Lakehouse:** Which Fabric workspace and lakehouse should we target? (AGENTS.md mentions "1323_MAIN" and "1323_LH" — confirm these are correct)
6. **Existing Models:** Are there any existing staging models for opportunities/accounts we should build on?

---

## Sources

### Required Source Tables

**Opportunity Data:**
- Table: `{source_schema}.opportunity` (or equivalent)
- Key Fields: `opportunity_id`, `account_id`, `amount`, `close_date`, `stage_name`, `is_closed`, `is_won`, `is_deleted`, `created_date`

**Account Data (optional, for enrichment):**
- Table: `{source_schema}.account`
- Key Fields: `account_id`, `account_name`, `industry`, `region`

**Data Source:** TBD — awaiting user confirmation on CRM system and ingestion status.

---

## Next Steps

1. User confirms data source and lakehouse configuration
2. Verify source tables are available or set up ingestion if needed
3. Proceed to design.md with source mapping and model architecture
4. Spawn requirements-reviewer for validation
