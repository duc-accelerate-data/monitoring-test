{{
    config(
        materialized='view'
    )
}}

with source as (

    select * from {{ source('raw', 'customers') }}

),

renamed as (

    select
        customer_id::integer as customer_id,
        name::text as name,
        email::text as email,
        created_at::timestamp as created_at

    from source

)

select * from renamed
