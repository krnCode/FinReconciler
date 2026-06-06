with

accounts_receivable as (
    select * from {{ ref('stg__accounts_receivable') }}
),

general_ledger as (
    select *

    from
        {{ ref('stg__general_ledger') }}

    where
        source_system = 'AR'
),

joined as (
    select
        ar.*,
        gl.gl_id

    from
        accounts_receivable as ar

    left join general_ledger as gl
        on ar.invoice_num = gl.document_ref
),

unmatched as (
    select
        ar_id,
        vendor_id,
        invoice_num,
        amount as ar_amount,
        invoice_date,
        status as ar_invoice_status

    from
        joined

    where
        gl_id is null
)

select * from unmatched
