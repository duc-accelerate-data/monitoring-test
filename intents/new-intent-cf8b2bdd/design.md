# Customer Staging Design

## Source Mapping

| Source Table | Staging Model     | Status |
|-------------|-------------------|---------|
| raw.customers | stg_customers.sql | ✅ Built |

## Model Architecture

```
raw.customers → stg_customers (view)
```

## Materialization Strategy

- **stg_customers**: View (1:1 with source, no transformation needed)

## Change Log

- 2026-04-03: Initial staging model created
