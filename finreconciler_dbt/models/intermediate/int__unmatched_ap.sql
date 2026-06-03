with

accounts_payable as (
    select * from {{ ref('accounts_payable') }}
),

general_ledger as (
    select * from {{ ref('general_ledger') }}
),

joined as (
    select
        ap.*,
        gl.*

    from
        accounts_payable as ap

    full outer join general_ledger as gl
        on ap.invoice_num = gl.document_ref
),

unmatched as (
    select
        ap_id,
        vendor_id,
        invoice_num,
        amount,
        invoice_date,
        status as ap_invoice_status
    from joined
    where gl_id is null
)

select * from unmatched
