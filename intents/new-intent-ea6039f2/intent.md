# Intent: Customer Staging Model

## Business Context
Create a foundational staging model for customer data to enable downstream analytics and reporting.

## Goals
- Establish a clean, typed staging layer for raw customer data
- Provide a standardized view of customer records for downstream models

## Business Rules
- Customer ID is the primary key
- All records from raw customers table are included
- Standard naming conventions and data types applied

## Sources
- **Raw Schema**: `raw.customers` table

## Models to Build
- `stg_customers` - Staging view with typed columns

## Acceptance Criteria
- [x] Source YAML defined for raw.customers
- [x] Staging model created with proper column types
- [ ] Model compiles successfully
- [ ] Model runs without errors
