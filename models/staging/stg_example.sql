{{ config(
    materialized='view'
) }}

with source as (
    select * from {{ source('raw', 'example_table') }}
),

renamed as (
    select
        id as example_id,
        created_at,
        updated_at
    from source
)

select * from renamed
