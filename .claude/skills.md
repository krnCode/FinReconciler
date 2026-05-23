# skills.md — Claude Code Capabilities & Checklist

**FinReconciler | Paulo Santana**

---

## 1. O Que Claude FAZ ✅

### 1.1 Testes dbt

- ✅ Criar testes SQL genéricos (assert queries)
- ✅ Adicionar testes standard dbt (not_null, unique, relationships, accepted_values)
- ✅ Documentar testes em schema.yml
- ✅ Criar fixtures de dados para edge cases
- ✅ Debug falhas de testes (analisar logs, sugerir correções)

**Exemplo:**
```sql
-- Cria teste para validar que reconciliação é simétrica
select * from {{ ref('mart_reconciliation_summary') }}
where (ap_amount is null and gl_amount is not null)
   or (ap_amount is not null and gl_amount is null)
-- Se retorna linhas, teste falha (desejado)
```

### 1.2 Dados para Reconciliação

- ✅ Gerar 100K registros realistas via Polars
- ✅ Incluir padrões financeiros reais (variação de valores, distribuição de datas)
- ✅ Criar desalinhamentos **propositais** (5-10% de registros unmatched)
- ✅ Documentar lógica de geração (seed, distribuições)
- ✅ Type hints + docstrings completas

**Exemplo:**
```python
def generate_accounts_payable(
    n_records: int = 100_000,
    mismatched_pct: float = 0.05,
    seed: int | None = None
) -> pl.DataFrame:
    """Generate AP data with intentional mismatches for testing recon."""
    # 5% não terão match no GL → testa unmatched detection
```

### 1.3 Documentação

- ✅ Escrever docstrings (Google style, completo)
- ✅ Comentários SQL explicativos
- ✅ README com setup, arquitetura, exemplos
- ✅ Documentação dbt em schema.yml (completa, uma-info-por-linha)
- ✅ Guias de desenvolvimento (dbt_guide.md, sql_patterns.md)
- ✅ Exemplos de código (com outputs esperados)

**Exemplo schema.yml:**
```yaml
models:
  - name: mart_variance_monthly
    description: |
      Month-over-month variance analysis with trend detection.
      Uses LAG window function to calculate prior month amounts.
      Primary key: entity + year + month.
    primary_key:
      - entity
      - year
      - month
    columns:
      - name: variance_pct
        description: Percentage change from prior month (variance / prior * 100).
        tests:
          - not_null
```

### 1.4 Debug & Troubleshooting

- ✅ Analisar erros dbt (model falhas, teste falhas)
- ✅ Sugerir correções (SQL logic, data issues)
- ✅ Revisar logs DuckDB
- ✅ Identificar problemas de performance (índices faltando, joins ineficientes)
- ✅ Validar lógica financeira (se variância está correta, se matches fazem sentido)

**Exemplo:**
```
Erro: Test `unique_ap_id` failed
→ Motivo: generate_source_data.py permite duplicatas
→ Solução: Adicionar deduplicação ou aumentar n_records
```

### 1.5 Geração de Código

- ✅ Criar scripts Python (data generation, initialization)
- ✅ Setup Streamlit pages (básico)

---

## 2. O Que Claude NÃO FAZ ❌

### 2.1 Executar Código

- ❌ **Não Gera macros dbt** (custom SQL functions) — Claude avalia e sugere alterações quando necessário
- ❌ **Não escreve SQL** (queries complexas, window functions, CTEs) — Claude avalia e sugere alterações quando necessário
- ❌ **Não cria** modelos dbt (staging, intermediate, marts) — Claude apenas sugere e você valida
- ❌ **Não roda** `dbt run`, `dbt test`, `python scripts/...`
- ❌ **Você executa** — Claude apenas sugere e você valida

### 2.2 Decisões Arquiteturais

- ❌ Não muda schema structure sem aprovação
- ❌ Não adiciona novas dependências sem OK
- ❌ Não propõe refactoring "por diversão"
- ❌ Não cria features Streamlit extras (fora do spec)

### 2.3 Conhecimento de Domínio Financeiro Profundo

- ❌ Não explica regras IFRS/CPC (você faz isso)
- ❌ Não questiona lógica contábil (assume que está correta)
- ❌ Não sugere regras de negócio (você especifica)

**Mas:**
- ✅ Implementa lógica conforme você especifica
- ✅ Valida se SQL reflete a lógica correta

### 2.4 Análise de Dados

- ❌ Não descobre insights (você faz exploração)
- ❌ Não sugere novos marts "por iniciativa própria"

---

## 3. Armadilhas Conhecidas & Como Evitar

### 3.1 SQL Window Functions

**Armadilha:** LAG() sem ORDER BY resulta em dados aleatórios
```sql
-- ❌ Errado
select vendor_id, amount, lag(amount) over (partition by vendor_id) as prior
from staging.ap

-- ✅ Correto
select vendor_id, amount, lag(amount) over (partition by vendor_id order by invoice_date) as prior
from staging.ap
```

**Claude checklist:** Sempre incluir ORDER BY em window functions

### 3.2 FULL OUTER JOIN Sem Coalesce

**Armadilha:** Linhas aparecem null quando deveriam ter valor
```sql
-- ❌ Resultado pode ter vendor_id nulo
select ap.vendor_id, gl.department, ap.amount, gl.amount
from ap_summary ap
full outer join gl_summary gl on ap.vendor_id = gl.department

-- ✅ Correto
select coalesce(ap.vendor_id, gl.department) as entity, ap.amount, gl.amount
from ap_summary ap
full outer join gl_summary gl on ap.vendor_id = gl.department
```

**Claude checklist:** FULL OUTER JOIN sempre com COALESCE

### 3.3 Desalinhamentos Propositais vs Bugs

**Importante:** Quando gerar dados, deixar claro quais desalinhamentos são **intencionais** (para testar recon):
```python
# ✅ Claro e documentado
if random.random() < 0.05:  # 5% mismatched (intentional)
    exclude_from_gl = True
```

**Claude checklist:** Documentar % de desalinhamento, por quê, e como testa

### 3.4 Tipos de Dados em DuckDB

**Armadilha:** Somas retornam diferentes tipos
```sql
-- DuckDB coloca decimals automaticamente
select sum(amount) from ap  -- Retorna DECIMAL(18,4), não FLOAT
```

**Claude checklist:** Sempre usar `cast` se precisar de tipo específico

### 3.5 Documentação Incompleta em schema.yml

**Armadilha:** Deixar sem PK ou description
```yaml
# ❌ Incompleto
columns:
  - name: vendor_id
    tests: [not_null, unique]

# ✅ Completo (conforme CLAUDE.md)
columns:
  - name: vendor_id
    description: Unique vendor identifier from AP system. Used to match against GL department codes.
    tests:
      - not_null
      - unique
```

**Claude checklist:** Toda coluna tem descrição + testes + PK declarada

---

## 4. Checklist Pré-Submissão

**Claude SEMPRE responde com este checklist antes de executar:**

```markdown
## Checklist Pré-Submissão

### Código
- [ ] Type hints em TODAS funções Python
- [ ] Docstrings Google style (completo com Args, Returns, Raises, Example)
- [ ] SQL lowercase com comentários `--`
- [ ] Aliases curtos e mnemonicôs (ap, ar, gl)
- [ ] Sem hardcoded values (parametrizados)

### dbt
- [ ] schema.yml: TODAS as colunas documentadas (uma-info-por-linha)
- [ ] TODOS os modelos têm primary_key ou unique_id
- [ ] TODOS os modelos têm tests (not_null + unique/relationships mínimo)
- [ ] Nenhum CREATE TABLE direto — tudo via {{ ref() }} ou {{ source() }}

### Dados
- [ ] 100K registros gerados (para demonstrar escalabilidade)
- [ ] Variância realista (valores min/max apropriados)
- [ ] Desalinhamentos documentados (X% sem GL match)
- [ ] Seed para reproducibilidade

### Logging & Error Handling
- [ ] Usando `logging` module (não print)
- [ ] Trata exceções com try/except se necessário
- [ ] Mensagens informativas (não técnicas para usuário)

### Testes
- [ ] Testes dbt rodam sem erro (ou falham com propósito)
- [ ] Edge cases cobertos (zero amounts, null values, datas inválidas)
- [ ] Assert queries explicadas (por que falha se OK)

### Documentação
- [ ] README atualizado (se necessário)
- [ ] Exemplos funcionam (testarei localmente)
- [ ] Links corretos (models, tables, etc)
- [ ] Sem typos

### Conformidade
- [ ] Segue CLAUDE.md padrões
- [ ] Linguagem: código em English, comunicação em Português
- [ ] Sem features extras (scope creep)
```

---

## 5. Padrões Obrigatórios

### 5.1 Python

```python
# SEMPRE
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def my_function(param1: int, param2: str | None = None) -> dict:
    """
    Complete description.
    
    Args:
        param1: What is this.
        param2: Optional. Defaults to None.
    
    Returns:
        Dictionary with keys 'x' and 'y'.
    
    Raises:
        ValueError: If param1 < 0.
    
    Example:
        >>> my_function(10, "test")
        {'x': 10, 'y': 'test'}
    """
    logger.info(f"Called with param1={param1}, param2={param2}")
    
    if param1 < 0:
        raise ValueError("param1 must be >= 0")
    
    return {'x': param1, 'y': param2}
```

### 5.2 SQL (dbt models)

```sql
-- config + description + staging logic
{{ config(
    materialized='view',  -- ou table
    schema='staging',
    tags=['critical']  -- opcional
) }}

-- CTE-based structure
with source as (
    select
        id,
        name,
        amount,
        created_at
    from {{ source('raw', 'my_table') }}
    where is_valid = true  -- Validação
),

transformed as (
    select
        id,
        name,
        upper(name) as name_clean,
        cast(amount as decimal(10, 2)) as amount,
        created_at
    from source
)

select * from transformed
```

### 5.3 dbt schema.yml

```yaml
version: 2

models:
  - name: my_model
    description: |
      What this model does.
      Where it's used.
      Key assumptions.
    primary_key:
      - id
    tests:
      - dbt_expectations.expect_table_row_count_to_be_between:
          min_value: 1000
          max_value: 10000000
    columns:
      - name: id
        description: Primary key. Unique identifier from source system.
        tests:
          - not_null
          - unique
      - name: name
        description: Entity name. Used for grouping in reports.
        tests:
          - not_null
          - accepted_values:
              values: ['A', 'B', 'C']
      - name: amount
        description: Monetary amount in USD. Null means not applicable.
        tests:
          - not_null
```

---

## 6. Escalation & Questions

**Claude deve perguntar se:**
- Não sabe exatamente o que fazer
- Precisa tomar decisão que afete arquitetura
- Avaliou 2+ formas e quer seu input
- Descobriu bug/issue que precisa sua análise

**Nunca assume.**

---

## 7. Performance Expectations

| Tarefa | Tempo Estimado | Volume |
|---|---|---|
| Criar modelo dbt simples | 2-5 min | N/A |
| Gerar dados 100K records | ~5 min | 100K |
| Adicionar 5 testes | 3-5 min | N/A |
| Debug erro dbt | 5-10 min | Depende |
| Documentação completa | 10-15 min | N/A |

**Lembrete:** Claude NÃO executa. Você roda localmente e valida.

---

## 8. Diferença: Local Testing vs Production

| Aspecto | Local | Production |
|---|---|---|
| Volume | 100K (demo) | 1M+ (real) |
| Frequência dbt run | On-demand | Scheduled (GitHub Actions) |
| CI/CD | N/A (manual) | GitHub Actions (testes automáticos) |
| Alertas | N/A | Slack/email se testes falharem |

Claude cria para **local testing** (100K). Produção você escala conforme necessário.

---

## 9. Referência Rápida

| Preciso de... | Claude Faz? | Comando |
|---|---|---|
| 100K dados | ✅ | Tarefa em TASKS.md |
| Testes SQL | ✅ | Tarefa em TASKS.md |
| Documentação | ✅ | Tarefa em TASKS.md |
| Corrigir erro | ✅ | Mostra erro, Claude sugere |
| Feature Streamlit | ✅ (básico) | Tarefa em TASKS.md |
| Novo modelo dbt | ❌ (sem solicitar) | Tarefa em TASKS.md |
| Refactor SQL | ❌ (sem solicitar) | Tarefa em TASKS.md |
| Execução | ❌ | Você roda |
| Análise de insights | ❌ | Você faz |

---

## 10. Histórico de Melhorias

**v1.0** (2026-05-23): Documento inicial criado.

---

**Dúvidas? Abra issue no GitHub ou comunique em TASKS.md.**
