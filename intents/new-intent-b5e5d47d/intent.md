# Customer Data Staging

## Business Context

Create a staging layer for customer data from the raw schema to enable downstream analytics and reporting.

## Goals

- Expose customer master data in a clean, consistent format
- Provide foundation for customer-centric analytics
- Enable joins to transactional data

## Business Rules

- All customers from source system included
- Standard column naming conventions applied
- No business logic transformations at this layer

## Acceptance Criteria

- [x] Staging model created with all required columns
- [x] Source YAML definition exists
- [ ] Model compiles successfully
- [ ] Model can be queried

## Sources

- **raw.customers** — customer master table

## Open Questions

None

## Clarifying Questions Asked

None — requirements were clear and complete.
