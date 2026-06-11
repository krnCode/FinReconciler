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
        and status = 'posted'
        and entry_type = 'debit'
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

    inner join general_ledger as gl
        on
            ar.invoice_num = gl.document_ref
            and ar.vendor_id = gl.gl_vendor_id
            and cast(ar.invoice_date as date) = cast(gl.gl_invoice_date as date)
),

gl_match_count as (
    select
        ar_id,
        count(gl_id) as gl_match_count

    from
        joined

    group by
        ar_id
),

value_comparison as (
    select
        j.*,
        glm.gl_match_count,
        j.ar_amount - j.gl_amount as value_difference,
        case
            when (j.ar_amount - j.gl_amount > 0.01) then 'mismatch'
            when (j.ar_amount - j.gl_amount < -0.01) then 'mismatch'
            else 'match'
        end as value_status

    from
        joined as j

    left join gl_match_count as glm
        on
            j.ar_id = glm.ar_id

)

select * from value_comparison
