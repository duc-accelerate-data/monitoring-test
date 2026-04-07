# Design: Simple Orders Staging Model

## Source Mapping
- No external source
- Mock data using VALUES or CTE

## Model Architecture
```
stg_orders (mock data) → [ready for downstream marts]
```

## Materialization Strategy
- `stg_orders`: View (standard for staging, minimal mock data)

## Validation Approach
- Compile check to verify syntax
- Row count validation (should return mock rows)

## Build Status
- [x] `stg_orders.sql` - Complete

## Change Log
- 2026-04-07: Initial design for mock orders model
- 2026-04-07: Created `stg_orders.sql` with 5 mock rows (order_id, customer_id, amount)
