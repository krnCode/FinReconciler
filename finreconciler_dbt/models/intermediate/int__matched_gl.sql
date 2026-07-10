with

general_ledger as (
    select * from {{ ref('stg__general_ledger') }}
),

matched_gl as (
    select *

    from general_ledger

    where
        document_ref is not null
)

select * from matched_gl
