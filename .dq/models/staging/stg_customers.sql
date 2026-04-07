{{ config(materialized='view') }}

with source as (
    select
        customer_id,
        name,
        email,
        created_at
    from {{ source('raw', 'customers') }}
)

select * from source
