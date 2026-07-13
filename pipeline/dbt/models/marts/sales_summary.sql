-- demo_sales_etl
{{ config(
    materialized='table',
    tags=['demo_sales_etl']
) }}

select
    user_id,
    sum(quantity) as total_quantity,
    max(sale_date) as last_sale
from {{ source('demo', 'raw_sales') }}
group by user_id
