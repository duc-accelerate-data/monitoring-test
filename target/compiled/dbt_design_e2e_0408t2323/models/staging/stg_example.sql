

with source as (
    select * from ai_fork_lake_new_intent_e4a66f9b.dbo.example_table
),

renamed as (
    select
        id as example_id,
        name as example_name,
        created_at
    from source
)

select * from renamed