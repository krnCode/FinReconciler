with

accounts_payable as (
    select * from {{ ref('stg__accounts_payable') }}
),

general_ledger as (
    select
        *,
        string_split(string_split(entry_description, '|')[2], ' ')[3]
            as gl_vendor_id,
        string_split(entry_description, '|')[3] as gl_invoice_date

    from
        {{ ref('stg__general_ledger') }}

    where
        source_system = 'AP'
        and account_code = '2100'
        and status = 'posted'
        and entry_type = 'credit'
),

joined as (
    select
        ap.ap_id,
        gl.gl_id,
        ap.vendor_id as ap_vendor_id,
        gl.gl_vendor_id,
        ap.invoice_num,
        gl.document_ref,
        ap.amount as ap_amount,
        gl.amount as gl_amount,
        cast(ap.invoice_date as date) as invoice_date,
        cast(gl.gl_invoice_date as date) as gl_invoice_date,
        cast(gl.posting_date as date) as posting_date,
        ap.status as ap_invoice_status,
        gl.account_code,
        gl.account_name,
        gl.department,
        gl.entry_type,
        gl.entry_description,
        gl.source_system,
        gl.status as gl_status

    from
        accounts_payable as ap

    left join general_ledger as gl
        on
            ap.invoice_num = gl.document_ref
            and ap.vendor_id = gl.gl_vendor_id
            and cast(ap.invoice_date as date) = cast(gl.gl_invoice_date as date)
),

unmatched as (
    select
        ap_id,
        gl_id,
        ap_vendor_id,
        invoice_num,
        ap_amount,
        invoice_date,
        ap_invoice_status

    from
        joined

    where
        gl_id is null
)

select * from unmatched
