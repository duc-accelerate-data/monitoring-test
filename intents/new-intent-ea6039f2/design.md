# Design: Customer Staging Model

## Source Mapping

```
raw.customers → stg_customers (staging view)
```

## Model Architecture

```
Source: raw.customers
   ↓
stg_customers (view)
   ↓
(available for downstream marts)
```

## Materialization Strategy

- **stg_customers**: View - Standard for staging models, 1:1 with source table, minimal transformation

## Model Specifications

### stg_customers
- **Grain**: One row per customer
- **Primary Key**: customer_id
- **Columns**:
  - customer_id (integer) - Unique customer identifier
  - name (text) - Customer name
  - email (text) - Customer email address
  - created_at (timestamp) - Account creation timestamp

## Validation Approach
- Verify model compiles
- Check primary key uniqueness
- Validate row count matches source

## Change Log
- 2026-04-06: Initial design - single staging model for customers
