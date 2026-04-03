# Customer Staging Model

## Business Context
Create a staging layer for customer data from the raw schema to support downstream analytics and reporting.

## Goals
- Establish a clean staging layer for customer data
- Standardize column naming and data types
- Provide foundation for customer-related analytics

## Sources
- Raw schema: `raw.customers` table

## Business Rules
- Customer ID serves as the primary key
- All source columns are passed through with standard transformations

## Acceptance Criteria
- [x] Staging model created with specified columns
- [ ] Model compiles successfully
- [ ] Source YAML defined
