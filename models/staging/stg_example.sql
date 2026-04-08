with source as (
    select * from {{ source('example_source', 'example_table') }}
),

renamed as (
    select
        *
    from source
)

select * from renamed
