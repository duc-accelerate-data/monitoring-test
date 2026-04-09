{{
    config(
        materialized='view'
    )
}}

SELECT
    1 AS id,
    'test' AS name
