{{ config(materialized='view') }}

with source as (
    select * from {{ source('raw', 'example_table') }}
),

renamed as (
    select
        id as example_id,
        name as example_name,
        created_at
    from source
)

select * from renamed
