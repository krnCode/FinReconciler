with

general_ledger as (
    select * from {{ ref('stg__general_ledger') }}
),

orphans as (
    select *

    from
        general_ledger

    where
        source_system = 'MANUAL'
)

select * from orphans
