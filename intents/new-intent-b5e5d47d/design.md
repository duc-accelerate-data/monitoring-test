# Customer Staging Design

## Source Mapping

| Source Table   | Staging Model    | Status      |
|---------------|------------------|-------------|
| raw.customers | stg_customers    | Building    |

## Model Architecture

```
raw.customers → stg_customers (view)
```

## Materialization Strategy

- **stg_customers**: View — staging models are lightweight pass-throughs with minimal transformation

## Validation Approach

1. Row count match between source and staging
2. Primary key uniqueness on customer_id
3. No nulls in customer_id
4. Data type casting validation

## Validation Results

_Not yet run_

## Change Log

- 2026-04-02: Initial design and implementation of customer staging model
