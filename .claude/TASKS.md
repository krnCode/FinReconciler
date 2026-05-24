# TASKS.md — Task & Backlog List

**FinReconciler**
---

**Última atualização:** 2026-05-24  
**Próxima revisão:** Após primeira batch de tarefas completadas

---
### Overview
* Use este arquivo para especificar tarefas ao Claude Code. Siga o template abaixo para cada nova tarefa. 
* No topo da página, seção "Task & Backlog List" está a lista de tarefas ativas e backlog.
* Na seção "Exemplos" estão alguns exemplos de tarefas.
---

## Como Usar Este Arquivo

1. **Você escreve:** Uma tarefa usando o template abaixo
2. **Claude lê:** Entende requisitos, contexto, critério
3. **Claude sugere:** "Aqui está meu plano: [...]"
4. **Você aprova:** "Sim, pode executar" ou "Muda isso"
5. **Claude executa:** Cria arquivos, você roda `dbt run` etc
6. **Você marca:** Status como ✅ Concluído
7.  **Os status são:** 🆕 Novo, 🔄 Em Progresso, ✅ Concluído

---

## Tips

- **Seja específico:** "Cria modelo X" é vago. "Cria modelo X com FULL OUTER JOIN para encontrar Y" é bom.
- **Contexto é ouro:** Link para models existentes, referencias, assumptions.
- **Critério claro:** Como você valida se está pronto?
- **Uma tarefa por seção:** Não misture "cria modelo" com "refatora SQL antigo".

---

# Task & Backlog List

## Task List

| ID | Task | Priority | Status | Claude Approves? | Feedback 
|---|---|---|---|---|---|
| [1] | Create project folder structure | High | 🆕 | No | - |
| [2] | Generate/update the README.md | High | 🆕 | No | - | 
| [3] | 
| [4] | 
| [5] | 

## Backlog

- [ ] Create project folder structure
- [ ] Generate/update the README.md
- [ ] 
- [ ] 
- [ ] 

---

## Tasks

## Task 1 : Create project folder structure

**Prioridade:** High
**Categoria:** Project Setup  
**Status:** 🆕 Novo

### Descrição
Criar estrutura de pastas e arquivos para o projeto.

### Requisitos
- [ ] Folders that contain sensitive information, such as auths, passwords, tokens, etc, should be included in .gitignore.
- [ ] Pastas que são referente aos models do dbt devem ser criadas em models/, e conter as etapas staging, intermediate e marts.
- [ ] Folders that are related to dbt, such as tests, and documentation should be created in the finreconciler_dbt/ folder.
- [ ] Folders that are related to dbt models (models/) and tests (tests/) should be created in the finreconciler_dbt/models/ (staging, intermediate, marts)
- [ ] A estrutura deve ser intuitiva e fácil de entender.
- [ ] The folder structure should be organized in a way that makes it easy to read and understand.

### Contexto / Referências
Consider the project goal, as described in the CLAUDE.md file.
In the CLAUDE.md file, there is the initial project structure, with folders and files.
In this moment, only the folders should be created.
The project will be done in English.

### Critério de Aceitação
* Folders with sensitive information should be included in .gitignore.
* The folder structure should be well organized and easy to understand.
* The project is in an initial state, as if it were a new project.

### Notas
* Never assume anything. Ask for clarification if needed.
* You can use the CLAUDE.md file as a reference.
* Opt for clarity and simplicity

---

## Template


```markdown
## Task: [Nome Descritivo]

**Prioridade:** High / Medium / Low  
**Categoria:** Modelos | Testes | Dados | Docs | Debug  
**Status:** 🆕 Novo / 🔄 Em Progresso / ✅ Concluído

### Descrição
[O que precisa ser feito? Por quê?]

### Requisitos
- [ ] Requisito 1
- [ ] Requisito 2
- [ ] Requisito 3

### Contexto / Referências
[Links, exemplos, ou contexto necessário]

### Critério de Aceitação
[Como você vai validar se está pronto?]

### Notas
[Restrições, decisões já tomadas, etc]
```

---

# Exemplos


## Exemplo 1: Criar um Modelo dbt

```markdown
## Task: Create mart_ap_gl_match Model

**Prioridade:** High  
**Categoria:** Modelos  
**Status:** 🆕 Novo

### Descrição
Criar modelo Mart que reconcilia AP (Accounts Payable) com GL (General Ledger).
Este é o core de reconciliation do projeto — mostra padrões avançados de SQL.

### Requisitos
- [ ] Modelo deve usar FULL OUTER JOIN para encontrar matched/unmatched
- [ ] Deve agregizar por vendor + period (year/month)
- [ ] Deve calcular variance = ap_amount - gl_amount
- [ ] Deve marcar status como 'matched' (variance < 0.01) ou 'unmatched'
- [ ] Totalmente documentado em schema.yml
- [ ] Testes dbt (not_null, unique key, data quality)
- [ ] SQL comments explicativos

### Contexto
- Staging models ja existem: `stg_accounts_payable`, `stg_general_ledger`
- AP amounts devem ser somados por vendor_id + period
- GL amounts devem ser somados por department + period (filtrando contas 2010, 2020)
- Usar `coalesce()` no FULL JOIN para evitar nulls na chave
- Ver `docs/financial_logic.md` para entender lógica de contas
```

### Critério de Aceitação
```bash
dbt run -s mart_ap_gl_match      # Roda sem erro
dbt test -s mart_ap_gl_match     # Todos os testes passam
```

Resultado esperado:
- ~50K linhas (100K AP × GL agrupados por period)
- ~85% matched, ~15% unmatched (reflete desalinhamentos propositais nos dados)
- Variance range: -50K a +50K USD

### Notas
- Materializado como `table` (não view) — usado para BI
- Use macros `safe_divide()` se precisar calcular ratios
- Não colocar lógica de variância aqui — fica em `mart_variance_monthly`

---

## Exemplo 2: Gerar Dados de Teste

```markdown
## Task: Generate 100K AP Records with Realistic Variance

**Prioridade:** High  
**Categoria:** Dados  
**Status:** 🆕 Novo

### Descrição
Estender `scripts/generate_source_data.py` para criar dados de AP (Accounts Payable) 
com padrões financeiros realistas. Será usado para toda a pipeline de testes.

### Requisitos
- [ ] Gerar 100,000 registros de AP
- [ ] Campos: ap_id, vendor_id, invoice_num, amount, invoice_date, gl_date, status
- [ ] Vendor IDs: 20 vendors (V001-V020)
- [ ] Amounts: distribuição realista (100-50,000 USD)
- [ ] Datas: 90 dias de histórico (últimos 3 meses)
- [ ] Status: 70% paid, 20% pending, 10% disputed
- [ ] **Importante:** 5% dos records NÃO terão match no GL (intencionalmente)
- [ ] Full docstring (Google style) + type hints
- [ ] Logging informativo
- [ ] Seed parametrizável para reproducibilidade

### Contexto
- Código entra em `scripts/generate_source_data.py`
- Função deve retornar `pl.DataFrame`
- Dados serão salvos como CSV em `data/raw/accounts_payable.csv`
- Será chamado por `scripts/init_duckdb.py`
```

### Critério de Aceitação
```bash
python scripts/generate_source_data.py
# Output: "Generated 100,000 AP records in data/raw/"

# Validação local
df = pl.read_csv("data/raw/accounts_payable.csv")
df.shape  # (100000, 7)
df["status"].value_counts()  # ~70K paid, ~20K pending, ~10K disputed
df.filter(pl.col("amount") <= 0).height  # 0 (sem negatives)
```

### Notas
- Mismatched records: não incluir no GL (logic fica em `generate_general_ledger()`)
- Use `random.seed()` ou `pl.Series.shuffle(seed=)` para reproducibilidade
- Amounts devem ter variação realista (não distribuição normal — use choices com weights)

---

## Exemplo 3: Criar Testes dbt

```markdown
## Task: Add Data Quality Tests for mart_reconciliation_summary

**Prioridade:** Medium  
**Categoria:** Testes  
**Status:** 🆕 Novo

### Descrição
Adicionar 5+ testes dbt para validar integridade dos dados de reconciliação.
Foco em edge cases: totals match, status é válido, não há duplicatas, etc.

### Requisitos
- [ ] Test 1: `not_null` em colunas críticas (entity, ap_amount, gl_amount, status)
- [ ] Test 2: `unique` na composite key (entity + year + month)
- [ ] Test 3: Custom SQL assert — totals match between AP e GL (para matched items)
- [ ] Test 4: Custom SQL assert — status deve ser 'matched' ou 'unmatched' (no meio-termo)
- [ ] Test 5: Custom SQL assert — variance < 0.5% para status='matched'
- [ ] Todos os testes documentados em schema.yml
- [ ] Testes devem usar `{{ fail_calc() }}` ou `where` para indicar failure

### Contexto
- Modelo alvo: `marts.mart_reconciliation_summary`
- Schema.yml já existe em `models/marts/reconciliation/schema.yml`
- Testes custom ficam em `tests/sql/`
```

### Critério de Aceitação
```bash
dbt test -s mart_reconciliation_summary  # Todos os testes passam

# Se houver falha proposital (para validar teste):
dbt test -s mart_reconciliation_summary --select tag:assert  # Falha esperada
```

### Notas
- Não use `singular` tests (deprecated) — use modelos com `-- config(severity: warn)`
- Testes devem ser descritivos: `assert_variance_pct_within_tolerance`
- Se teste falhar, deve ser claro por quê (use comments no SQL)

---

## Exemplo 4: Documentação

```markdown
## Task: Write Comprehensive schema.yml for mart_variance_monthly

**Prioridade:** Medium  
**Categoria:** Docs  
**Status:** 🆕 Novo

### Descrição
Documentar completamente o modelo `mart_variance_monthly` seguindo padrão CLAUDE.md.
Deve incluir descrição detalhada, primary_key, todos os testes, e examples.

### Requisitos
- [ ] Descrição do modelo (multi-line, explicando propósito, uso, assumptions)
- [ ] Primary key declarada (entity + year + month)
- [ ] **Cada coluna documentada:**
  - name, description (uma frase concisa), data_type (se relevante), tests
- [ ] Tests incluídos:
  - not_null para colunas críticas
  - unique na composite key
  - accepted_values para variance_bucket
  - relationships se houver FK
- [ ] Exemplo de uso / consulta esperada
- [ ] Anotações de lógica financeira (variância é YTD? MoM? Rolling?)

### Contexto
- Template: `models/marts/reconciliation/schema.yml` (existe)
- Adicionar section novo para `mart_variance_monthly`
```

### Critério de Aceitação
- Schema.yml valida sem erro (`dbt parse`)
- Cada coluna tem descrição > 5 palavras
- Cada coluna tem ≥1 test
- Documentação é clara sem jargão técnico demais

### Notas
- Descrição deve explicar a **intenção**, não apenas o que é
- Exemplo: Ruim: "Month and year of transaction"
- Exemplo: Bom: "Fiscal year and month when variance was calculated. Used to join with calendar for reporting."

---

## Exemplo 5: Debug

```markdown
## Task: Debug Test Failure in test_variance_logic

**Prioridade:** High  
**Categoria:** Debug  
**Status:** 🔄 Em Progresso

### Descrição
Test `assert_variance_pct_within_tolerance` está falhando.
Investigar e sugerir correção.

### Contexto do Erro
Failure in tests/sql/assert_variance_pct_within_tolerance.sql:
Got 153 rows where variance_pct > 0.05 (5%)
Expected 0 rows.
```

Dados têm ~100K registros, 5% desalinhamentos propositais → variâncias legítimas.

### Requisitos
- [ ] Analisar se é bug no SQL ou na lógica de teste
- [ ] Se for teste muito restritivo, suggir ajuste
- [ ] Se for bug, sugerir correção no SQL da variance calc
- [ ] Validar que correção não quebra outros testes

### Critério de Aceitação
```bash
dbt test -s test_variance_logic  # Passa
```

### Notas
- Teste pode estar correto — talvez accuracy expectation precise ajuste
- Investigar se 5% de variance é aceitável ou não (pergunta: é bug ou feature?)

---

## Exemplo 6: Feature Streamlit

```markdown
## Task: Add Variance Anomaly Detection to Streamlit

**Prioridade:** Low  
**Categoria:** Modelos + Docs  
**Status:** 🆕 Novo

### Descrição
Criar página Streamlit (`pages/3_anomalies.py`) que mostra variâncias anômalas
(outliers). Usar dados de `mart_variance_monthly` para flagging.

### Requisitos
- [ ] Sidebar filter: variance_pct range (slider)
- [ ] Sidebar filter: variance_bucket (multiselect)
- [ ] Sidebar filter: entity (multiselect de vendors)
- [ ] Main: Tabela com anomalias (sorted by variance_pct desc)
- [ ] Visual: Scatter plot (amount vs variance_pct)
- [ ] Métrica top: Número de anomalias detadas, avg variance %

### Contexto
- Página entra em `app/pages/3_anomalies.py`
- Dados: `select * from marts.mart_variance_monthly where variance_pct > 0.05`
- Usar Altair para visualizações (consistente com projeto)
```

### Critério de Aceitação
```bash
streamlit run app/app.py
# Navigate to "Anomalies" → Deve mostrar dados + filters + charts
```

### Notas
- Não criar novas dependências (Altair já está no lock)
- Usar cache `@st.cache_data` para queries
- Responsivo em mobile

---


