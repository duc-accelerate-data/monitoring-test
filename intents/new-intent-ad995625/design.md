# Customer Data Pipeline Design

## Source Mapping
- **Source:** `raw.customers`
- **Staging Model:** `stg_customers` (view) ✓ Created

## Model Architecture
```
raw.customers → stg_customers
```

## Materialization Strategy
- `stg_customers`: **view** (standard for staging models, 1:1 with source)

## Change Log
- 2026-04-03: Initial creation of customer staging model with customer_id, name, email, created_at columns
