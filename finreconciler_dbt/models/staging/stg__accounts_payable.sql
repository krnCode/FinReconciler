with

source as (
    select * from {{ source('finreconciler_duckdb', 'accounts_payable') }}
)

select * from source
