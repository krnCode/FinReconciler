# CLAUDE.md — FinReconciler Claude Code Manual

**Last Updated:** 2026-05-23  
**Project:** FinReconciler  
**Stack:** DuckDB | dbt | Python | Streamlit | SQL

---

## 1. Visão Geral & Propósito

FinReconciler é um pipeline **production-grade** de reconciliação e análise de variância financeira que demonstra:
- Proficiência em **SQL moderno** (window functions, CTEs, FULL OUTER JOIN)
- Arquitetura de dados **escalável** (staging → intermediate → marts)
- **Automação de testes** em toda a pipeline
- **Documentação técnica completa** para transferência de conhecimento

**Claude's Role:**
- ✅ Gerar testes dbt e dados de teste
- ✅ Criar/revisar documentação (docstrings, comentários SQL, guias)
- ✅ Debug e troubleshooting (análise de erros, logs)
- ✅ Gerar dados realistas para reconciliação (via Polars)
- ❌ Não tomar decisões arquiteturais sem aprovação
- ❌ Não executar código — apenas sugerir e você executa

---

## 2. Estrutura do Projeto

```
finreconciler/
├── models/              → dbt models (staging, intermediate, marts)
├── scripts/             → Python (geração de dados, inicialização)
├── app/                 → Streamlit frontend
├── data/                → CSVs (raw/, seeds/)
├── tests/               → dbt tests (SQL + generic)
├── macros/              → Custom SQL functions
├── docs/                → Markdown documentation
├── pyproject.toml       → Dependências (uv)
├── dbt_project.yml      → Config dbt
├── profiles.yml         → DuckDB connection
├── CLAUDE.md            → Este arquivo
├── skills.md            → Capabilities & checklist
└── TASKS.md             → Task template
```

---

## 3. Padrões & Convenções

### 3.1 SQL

**Estilo:** lowercase (padrão dbt)  
**Formatação:**
```sql
-- Bom ✅
with ap_summary as (
    select
        vendor_id,
        extract(year from invoice_date) as year,
        sum(amount) as total_amount,
        count(*) as record_count
    from {{ ref('stg_accounts_payable') }}
    group by vendor_id, year
),

gl_summary as (
    select
        department,
        extract(year from journal_date) as year,
        sum(amount) as total_amount
    from {{ ref('stg_general_ledger') }}
    where account_code in ('2010', '2020')
    group by department, year
)

select
    ap.vendor_id as entity,
    ap.year,
    ap.total_amount as ap_amount,
    gl.total_amount as gl_amount,
    ap.total_amount - gl.total_amount as variance
from ap_summary ap
full outer join gl_summary gl
    on ap.vendor_id = gl.department
    and ap.year = gl.year
```

**Comentários:** Single-line `-- explanation`
```sql
-- Agrupa por vendor e período fiscal
select vendor_id, sum(amount) as total
from staging.ap
group by vendor_id
```

**Aliases:** Curtos, mnemonicôs (ap, ar, gl, int, stg)
```sql
from {{ ref('stg_accounts_payable') }} ap
inner join {{ ref('dim_dates') }} d on ap.invoice_date = d.date_id
```

### 3.2 Python

**Type Hints:** SEMPRE
```python
def generate_accounts_payable(
    n_records: int,
    seed: int | None = None
) -> pl.DataFrame:
    """Generate synthetic AP data."""
    ...
```

**Logging:** Use `logging` module, não `print()`
```python
import logging

logger = logging.getLogger(__name__)
logger.info(f"Generated {n_records} AP records")
logger.warning("Duplicate invoice numbers detected")
logger.error("Failed to connect to database")
```

**Docstrings:** Google Style (completo, com exemplos)
```python
def safe_divide(numerator: float, denominator: float) -> float:
    """
    Safely divide two numbers, handling zero denominator.
    
    Returns 0 if denominator is zero to avoid division by zero exceptions.
    
    Args:
        numerator: The dividend (number to be divided).
        denominator: The divisor (number to divide by).
    
    Returns:
        Result of numerator/denominator, or 0.0 if denominator is 0.
    
    Raises:
        TypeError: If inputs are not numeric types.
    
    Example:
        >>> safe_divide(10, 2)
        5.0
        >>> safe_divide(10, 0)
        0.0
    """
    if not isinstance(numerator, (int, float)) or not isinstance(denominator, (int, float)):
        raise TypeError("Both arguments must be numeric")
    return numerator / denominator if denominator != 0 else 0.0
```

### 3.3 dbt

**YAML Documentation:** Completo, uma informação por linha, máxima descrição possível

```yaml
# models/marts/reconciliation/schema.yml
models:
  - name: mart_ap_gl_match
    description: |
      Reconciliation between Accounts Payable (AP) system and General Ledger (GL).
      Matches AP invoices to GL postings using FULL OUTER JOIN to identify unmatched items.
      Used by Finance team for monthly close process and variance investigation.
    columns:
      - name: entity
        description: Vendor ID from AP system or Department from GL (coalesced in FULL JOIN).
        tests:
          - not_null
          - unique
      - name: ap_amount
        description: Total AP invoices for the entity-period combination.
        tests:
          - not_null
      - name: gl_amount
        description: Total GL postings for the entity-period combination (accounts 2010, 2020).
        tests:
          - not_null
      - name: variance
        description: Difference between AP amount and GL amount (ap_amount - gl_amount).
        tests:
          - not_null
      - name: status
        description: Reconciliation status - either 'matched' (variance < 0.01) or 'unmatched'.
        tests:
          - accepted_values:
              values: ['matched', 'unmatched']

  - name: mart_variance_monthly
    description: |
      Month-over-month variance analysis showing trends and anomalies.
      Calculates percentage variance using LAG window function.
      Primary key: entity + year + month.
    primary_key:
      - entity
      - year
      - month
    columns:
      - name: entity
        description: Business entity or cost center.
      - name: variance_pct
        description: Percentage change from prior month (variance_amount / prior_amount * 100).
      - name: variance_bucket
        description: Categorized variance range (0-5%, 5-10%, 10%+, etc).
```

**Tests:** Standard dbt tests (not_null, unique, accepted_values, relationships)

```yaml
tests:
  - not_null_critical:
      columns:
        - vendor_id
        - invoice_date
        - amount
  - unique:
      column_name: ap_id
  - accepted_values:
      column_name: status
      values: ['paid', 'pending', 'disputed']
```

---

## 4. Fluxo de Trabalho

### 4.1 Como Você Trabalha com Claude

1. **Você escreve uma task** em `TASKS.md` (template fornecido)
   ```markdown
   ## Task: Create mart_variance_by_department
   
   - Add window function LAG() for month-over-month comparison
   - Include variance_bucket macro
   - Add dbt tests for data quality
   - Document fully in schema.yml
   ```

2. **Claude sugere solução** (código, documentação, testes)
   - Mostra o que vai fazer
   - Aponta eventuais decisões

3. **Você aprova ou pede ajustes**
   - "Looks good, go ahead"
   - "Add more test coverage"
   - "Change this logic"

4. **Claude executa** (se aprovado)
   - Cria arquivos
   - Você roda localmente (`dbt run`, `dbt test`, etc)

### 4.2 Antes de Submeter (Claude's Checklist)

Claude SEMPRE responde com:

```markdown
## Proposta: [Nome da tarefa]

### O que vou fazer:
- [ ] Criar model X
- [ ] Adicionar tests Y
- [ ] Documentar em schema.yml

### Decisões:
- Usando FULL OUTER JOIN para unmatched detection
- Window function LAG para variance YTD
- Materializado como table (não view)

### Você quer alguma mudança antes eu executar?
```

---

## 5. Dados & Ambiente

### 5.1 Volume de Teste

**Padrão: 100,000 registros por tabela**
- Suficiente para demonstrar escalabilidade
- DuckDB colunaris roda em <500ms
- Mostra que SQL é otimizado mesmo com volume

**Geração:**
```python
# scripts/generate_source_data.py
def generate_accounts_payable(n_records: int = 100_000) -> pl.DataFrame:
    # Cria 100K registros com variância realista
    ...
```

### 5.2 Ambiente

**Python:** 3.13+  
**DuckDB:** Latest (não pinned)  
**uv:** Para dependency management  

**Como rodar:**
```bash
uv sync                               # Install deps
python scripts/generate_source_data.py  # Generate 100K records
python scripts/init_duckdb.py         # Init DB + dbt
dbt run                               # Execute models
dbt test                              # Validate
streamlit run app/app.py              # Visualize
```

### 5.3 Dados de Teste

Claude gera dados realistas via **Polars**:
- Variação de valores (AP: 100-50K, AR: 500-100K)
- Datas distribuídas (90 dias de histórico)
- Status variados (paid, pending, disputed)
- **Desalinhamentos propositais** (algumas invoices sem GL match — para testar recon)

Exemplo:
```python
# 5% dos registros não têm match no GL (realista para testes)
if random.random() < 0.05:
    # Não incluir no GL → unmatched detection
    pass
```

---

## 6. Documentação Esperada

### 6.1 Código SQL

**Sempre comentado:**
```sql
-- Staging: limpeza e validação de AP raw
-- Remova negatives (não são invoices válidas)
-- Mantenha histórico para SCD Type 1 (status mudanças)
with cleaned as (
    select
        ap_id,
        vendor_id,
        invoice_num,
        amount,
        invoice_date,
        gl_date,
        status,
        current_timestamp() as dbt_loaded_at
    from {{ source('raw', 'accounts_payable') }}
    where amount > 0  -- Exclui débitos negativos
)

select * from cleaned
```

### 6.2 Python

**Docstrings Google Style + Type Hints:**
```python
def generate_accounts_payable(
    n_records: int = 100_000,
    mismatched_pct: float = 0.05,
    seed: int | None = None
) -> pl.DataFrame:
    """
    Generate synthetic Accounts Payable data with realistic variance.
    
    Creates a dataset with vendors, invoices, amounts, and dates.
    Intentionally includes some mismatched records (not in GL) to test
    reconciliation logic.
    
    Args:
        n_records: Number of AP records to generate. Default 100_000.
        mismatched_pct: Percentage of records intentionally not in GL (0-1).
        seed: Random seed for reproducibility. If None, non-deterministic.
    
    Returns:
        Polars DataFrame with columns: ap_id, vendor_id, invoice_num,
        amount, invoice_date, gl_date, status.
    
    Raises:
        ValueError: If n_records < 1 or mismatched_pct not in [0, 1].
    
    Example:
        >>> df = generate_accounts_payable(n_records=10_000, seed=42)
        >>> df.shape
        (10000, 7)
        >>> df.filter(pl.col("status") == "pending").shape[0]
        3333
    """
    if n_records < 1:
        raise ValueError("n_records must be >= 1")
    if not 0 <= mismatched_pct <= 1:
        raise ValueError("mismatched_pct must be between 0 and 1")
    
    logger.info(f"Generating {n_records} AP records with {mismatched_pct*100}% mismatch")
    ...
```

### 6.3 README & Documentação

Completa com:
- Arquitetura (diagrama, fluxo)
- Setup (passo-a-passo)
- SQL patterns usados
- Lógica financeira explicada

---

## 7. Áreas Fora de Escopo

**Claude NÃO deve:**
- Mudar arquitetura sem aprovação (ex: adicionar nova schema)
- Criar features Streamlit extras (fora do spec)
- Adicionar dependências novas (sem seu OK)
- Fazer refactoring "por diversão" (apenas se solicitado)

**Claude DEVE:**
- Sugerir antes de executar
- Manter padrões consistentes
- Documentar tudo o que faz
- Testar o que cria

---

## 8. Como Claude Comunica

**Sempre em inglês quando falando com você.**  
**Código em inglês (comentários, docstrings, variáveis).**

**Exemplo de comunicação:**

```
Hi Boss! I created a task for mart_variance_by_department.

What I will do:
- Create model with LAG() for MoM comparison
- Add tests for data quality
- Document in schema.yml with complete exposition for each column

Deciosions:
- Materialzed as table (not view) because we use it for BI
- Include variance_bucket for categorizing ranges
- Use CASE to avoid division by zero

Do you want me to change something before I run?
```

---

## 9. Referências Rápidas

**Configurar novo modelo dbt:**
1. Criar arquivo `models/path/model_name.sql`
2. Adicionar config no topo (materialized, schema, tests)
3. Documentar em `schema.yml` (completo)
4. Adicionar testes dbt (not_null, unique, accepted_values)
5. Rodar `dbt run && dbt test`

**Gerar dados Polars:**
1. Criar função em `scripts/generate_source_data.py`
2. Return `pl.DataFrame` com type hints
3. Documentar função (Google style)
4. Usar em `scripts/init_duckdb.py`

**Criar teste dbt:**
```sql
-- tests/assert_recon_totals_match.sql
select * from {{ ref('mart_reconciliation_summary') }}
where abs(ap_amount - gl_amount) > 0.01
and status = 'matched'  -- Should not happen
```

---

## 10. Contato & Esclarecimentos

Se Claude tiver dúvidas:
- Pergunta sempre (melhor pedir do que adivinhar)
- Comunica em português
- Mostra opções e deixa você decidir

Se você tiver feedback:
- "Esse padrão não é que gosto" → Claude aprende
- "Isso ficou muito verboso" → Claude ajusta
- "Faltou X" → Claude adiciona

---

**Este documento é vivo.** Atualizará conforme o projeto evolui.

**Última atualização:** 2026-05-23  
**Próxima revisão:** Após primeiros 5 tasks
