-- Simple staging model with mock order data

with mock_orders as (
    select 1 as order_id, 101 as customer_id, 150.00 as amount
    union all
    select 2 as order_id, 102 as customer_id, 250.50 as amount
    union all
    select 3 as order_id, 101 as customer_id, 75.25 as amount
    union all
    select 4 as order_id, 103 as customer_id, 500.00 as amount
    union all
    select 5 as order_id, 102 as customer_id, 125.75 as amount
)

select
    order_id,
    customer_id,
    amount
from mock_orders
