with

source as (
    select * from {{ source('finreconciler_duckdb', 'general_ledger') }}
)

select * from source
