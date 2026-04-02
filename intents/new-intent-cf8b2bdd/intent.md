# Customer Staging Model

## Business Context

Create a staging model for customer data from the raw schema to enable downstream analytics and reporting.

## Goals

- Provide a clean, consistent interface to raw customer data
- Enable downstream mart models to reference customer information
- Establish naming conventions for the staging layer

## Sources

- Raw schema: `customers` table

## Acceptance Criteria

- [x] Staging model created with standardized naming
- [x] Source YAML definition created
- [x] Model uses dbt source() macro
