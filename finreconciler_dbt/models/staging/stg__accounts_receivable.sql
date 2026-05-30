with

source as (
    select * from {{ source('finreconciler_duckdb', 'accounts_receivable') }}
)

select * from source
