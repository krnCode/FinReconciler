with

accounts_payable as (
    select * from {{ ref('stg__accounts_payable') }}
),

general_ledger as (
    select *

    from
        {{ ref('stg__general_ledger') }}

    where
        source_system = 'AP'
),

joined as (
    select
        ap.*,
        gl.gl_id

    from
        accounts_payable as ap

    left join general_ledger as gl
        on ap.invoice_num = gl.document_ref
),

unmatched as (
    select
        ap_id,
        vendor_id,
        invoice_num,
        amount as ap_amount,
        invoice_date,
        status as ap_invoice_status

    from
        joined

    where
        gl_id is null
)

select * from unmatched
