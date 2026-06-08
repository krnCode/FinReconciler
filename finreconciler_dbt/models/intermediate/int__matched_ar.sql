with

accounts_receivable as (
    select * from {{ ref('stg__accounts_receivable') }}
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
        source_system = 'AR'
        and account_code = '1100'
),

joined as (
    select
        ar.ar_id,
        gl.gl_id,
        ar.vendor_id as ar_vendor_id,
        gl.gl_vendor_id,
        ar.invoice_num,
        gl.document_ref,
        ar.amount as ar_amount,
        gl.amount as gl_amount,
        cast(ar.invoice_date as date) as invoice_date,
        cast(gl.gl_invoice_date as date) as gl_invoice_date,
        cast(gl.posting_date as date) as posting_date,
        ar.status as ar_invoice_status,
        gl.account_code,
        gl.account_name,
        gl.department,
        gl.entry_type,
        gl.entry_description,
        gl.source_system,
        gl.status as gl_status

    from
        accounts_receivable as ar

    left join general_ledger as gl
        on
            ar.invoice_num = gl.document_ref
            and ar.vendor_id = gl.gl_vendor_id
            and cast(ar.invoice_date as date) = cast(gl.gl_invoice_date as date)
),

value_comparison as (
    select
        *,
        ar_amount - gl_amount as value_difference,
        case
            when ar_amount != gl_amount then 'mismatch'
            else 'match'
        end as value_status

    from
        joined

    where
        gl_id is not null
)

select * from value_comparison
