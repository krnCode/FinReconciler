# TASKS.md — Task & Backlog List

**FinReconciler**
---

**Last Update:** 2026-06-02 
**Next revision:** After next batch of completed tasks (reviews)

---
### Overview
* Use this file to specify tasks for Claude Code. Follow the template below for each new task.
* At the top of the page, the "Task & Backlog List" section is a list of active and backlog tasks.
* The "Examples" section contains some example tasks.
---

## How to use this file

1. **You write:** A task using the template below
2. **Claude reads:** Understands requirements, context, criteria
3. **Claude suggests:** "Here's my plan: [...]"
4. **You approve:** "Yes, I can run" or "Change it"
5. **Claude executes:** Creates files, you run `dbt run` etc
6. **You mark:** Status as ✅ Completed
7. **Statuses are:** 🆕 New, 🔄 In Progress, ✅ Done

---

## Tips

- **Be specific:** "Create model X" is vague. "Create model X with FULL OUTER JOIN to find Y" is better.
- **Context is gold:** Link to existing models, references, assumptions.
- **Clear criterion:** How do you validate readiness?
- **One task per section:** Don't mix "create model" with "refactor old SQL".

---

# Task & Backlog List

<details>
<summary>Task List</summary>

| ID | Task | Priority | Status | Claude Approves? | Date Completed | Feedback 
|---|---|---|---|---|---|---|
| [1] | Create project folder structure | High | ✅ | No | 2026-05-24 | Done correctly, but I had to specify that it was only to create folders |
| [2] | Generate/update the README.md | High | ✅ | Yes | 2026-05-24 | Done, minor changes made before creating the final file | 
| [3] | Create mock data with Polars | High | ✅ | Yes | 2026-05-24 | Done, data generated successfully / Found a bug in the datetime generation in 2026-05-30 (created Task 5 to fix it) |
| [4] | Redesign GL structure | High | ✅ | No | 2026-05-30 | Done, needed to update the structure of the schema.yml file (include '"' in the descriptions) and tell Claude to not create the _sources.yml file |
| [5] | Fix date generation bug | High | ✅ | No | 2026-05-30 | Done |
| [6] | Update project README | Low | ✅ | No | 2026-05-30 | Done, minimal changes made (standard dbt badge description) |
| [7] | Update project README (03/07/2026) | Low | 🆕 | No |  |  |
</details>

<details> 
<summary>Backlog</summary>

- [X] Create mock data with Polars
- [X] Redesing GL structure
- [X] Fix date generation bug (same date being generated for every record)
- [X] Create duckdb structure
- [X] Update project README
- [ ] Update project README (03/07/2026)
- [ ] Start analysis
</details>

## Tasks

<details>
<summary>Ongoing Tasks</summary>
## Task 7: Update project README (03/07/2026)

**Priority:** Low  
**Category:** Docs  
**Status:** 🆕 New 

### Description
Update project README.md to reflect current status of project.

### Requirements
- [ ] Review the project status
- [ ] Compare it to the current README.md
- [ ] Update the README.md to reflect the current status of the project

### Context
The update should compare what is in the README.md at this moment and update it with the current status of the project.

### Acceptance Criteria
- [ ] README.md updated and reflects current status of project
- [ ] Information updated correctly reflects current status of project

### Notes
Don't add anything that did not change.
Keep the strucutre of the README.md the same.

</details>

<details>
<summary>Completed Tasks</summary>

## Task 6: Update project README

**Priority:** Low  
**Category:** Docs  
**Status:** ✅ Completed

### Description
Update project README.md to reflect current status of project.

### Requirements
- [X] eview the project status
- [X] Compare it to the current README.md
- [X] Update the README.md to reflect the current status of the project

### Context
The update should compare what is in the README.md at this moment and update it with the current status of the project.

### Acceptance Criteria
- [X] README.md updated
- [X] Information updated correctly reflects current status of project

### Notes
Don't add anything that did not change.
Keep the strucutre of the README.md the same.

---

## Task 5: Fix date generation bug

**Prioridade:** High  
**Categoria:** Bug Fix  
**Status:** ✅ Completed

### Descrição
Fix bug on date generation. It was generating the same date for every record. If there's no difference in the dates, we can't do a variance analysis between months or days.

### Requisitos
- [X] Make it so that the dates are different for every record on the AP and AR tables
- [X] Dates must be created in a range of 90 days from the last 3 months

### Contexto / Referências
Without different dates, we can't do a variance analysis between months, days, etc.

### Critério de Aceitação
- [X] Dates are different for every record on the AP and AR tables
- [X] Dates are created in a range of 90 days from the last 3 months

### Notas
- AP and AR tables can have the same dates, but it should be in different hours
- The date range should be 90 days from the last 3 months
- It shoud be possible to compare different months, days, times, etc

---

## Task 4: Redesing GL structure

**Priority:** High  
**Category:** Dados  
**Status:** ✅ Completed

### Description
Rebuild GL table as a double-entry journal (two lines per transaction, same journal_id, same entry_description, same entry_date)

### Requirements
- [X] Rebuild GL table as a double-entry journal (two lines per transaction, same journal_id, same entry_description, same entry_date)
- [X] New structure: gl_id, journal_id,document_ref, account_code, account_name, department, amount, entry_type, entry_description, source_system, posting_date, status
- [X] GL must be derived from the AP and AR tables
- [X] Must have controlled noise (~5% AP unposted, ~8% AR unposted, ~3% manual/orphan GL entries)
- [X] entry_description as a single formatted string that have transaction data
- [X] Drop matched_to_gl from AP/AR tables - the reconciliation status will be added in the dbt models

### Context
- The idea of the redesing is to have a simulation of a real GL system, where it have the standard information an ERP would have.
- The GL must be derived from the AP and AR tables, so we can use the same data for both.
- It must have controlled noise, so we can implement the reconciliation logic. Without this, the GL would be a perfect copy of the AP and AR tables.
-The entry_description must be a single formatted string that have transaction data, so we can use it for reporting and validation.
- entry_description must have a standard format per transaction type (AP, AR, manual entries, adjustments, etc).

### Acceptance Criteria
 - [X] GL table created and follow the new structure defined
 - [X] GL must be derived from the AP and AR tables
 - [X] GL must have double entry journaling following accounting principles (both entries must be balanced)
 - [X] Must have controlled noise (~5% AP unposted, ~8% AR unposted, ~3% manual/orphan GL entries)
 - [X] entry_description as a single formatted string that have transaction data and clearly explains the transaction
 - [X] The column matched_to_gl must have been dropped

### Notes
- New structure definitions:
  - gl_id: PK
  - journal_id: groups the two entries together
  - document_ref: Links back to AP/AR invoice
  - account_code: AP Liability, AR Asset, Expense, etc
  - account_name: Name of the account in the balance sheet or P&L
  - department: Name of the department/cost center
  - amount: Value of the transaction from the AP/AR tables
  - entry_type: debit / credit
  - entry_description: Formatted string that has transaction data and clearly explains the transaction
  - source_system: Which subledger generated the transaction (AP, AR, etc)
  - posting_date: Date of the transaction, may differ from invoice date (posting delay)
  - status: posted / pending / reversed
- entry_description format examples: 
  - AP Invoice INV770487 | Vendor VENDOR00006 | 2026-04-26
  - AR Invoice INV216739 | Customer CUST00042 | 2026-04-28
  - Manual Entry GL00094821 | Dept: Finance | Period: 2026-04

## Task 3 : Create mock data with Polars

**Priority:** High
**Category:** Data Creation  
**Status:** ✅ Completed

### Description
Create 100k records with realistic variance using Polars.

### Requirements
- [X] Data must be generated with Polars
- [X] After creating the mock data, it must be saved as CSV in the `data/raw/` folder
- [X] The scripts must be saved in the `scripts/` folder
- [X] One script per table (Accounts Payable, Accounts Receivable, General Ledger)
- [X] The data must follow the objectives of the project
- [X] It should contain mismatched records (intentional) for reconciliation testing
- [X] It should be seeded with a random number for reproducibility
- [X] Keep the structure of the script modular, so it can be easily extended and reused
- [X] If needed, create a new folder for helper functions inside the `scripts/` folder
- [X] Include raw data in .gitignore
- [X] Create documentation explaining how the data was generated

### Context
- Based on CLAUDE.md project structure and guidelines
- Data will be saved in the `data/raw/` folder
- If needed, create a schema file to be used to generate the data

### Acceptance Criteria
- [X] 100k records are generated with realistic variance
- [X] Records are saved as CSV in the `data/raw/` folder
- [X] One file per table (Accounts Payable, Accounts Receivable, General Ledger)
- [X] Polars was used to generate the data
- [X] Scripts are saved in the `scripts/` folder
- [X] Scripts are modular and can be easily extended and reused
- [X] Scripts are documented with Google style docstrings
- [X] Scripts are seeded with a random number for reproducibility
- [X] Scripts are modular and can be easily extended and reused
- [X] .gitignore includes the raw data folder (big files for github)
- [X] Documentation explains how the data was generated

### Notes
- Information must be in English
- Must have a documentation of how the data was generated
- Must follow the CLAUDE.md project structure and guidelines
- Three tables: one script, one file and one schema per table
- Mismatched definition: a mismatch in this context would mean 
different values, different amounts, different dates, records not in general ledger
- Schemas:
  Accounts Payable - ap_id, vendor_id, invoice_num, amount, invoice_date, status
  Accounts Receivable - ar_id, vendor_id, invoice_num, amount, invoice_date, status
  General Ledger - gl_id, department, amount, date
- Helper functions definition: Functions that can be used more than once in the project,
such as generating random dates, generating random amounts, etc.
- Documentation about the data generation process: it should inform the reader about
the data generation process, including the assumptions, the data structure, the steps
taken to generate the data, the stack used, the schemas defined, the outputs generated,
and any other relevant information. The documentation should be clear, concise, and
easy to understand. Opt for simplicity (be direct and to the point, separate itens 
clearly in the markdown file).
- Seeding: it must have the seed used in the code and in the documentation to be
reproducible and also have the ability to change the seed so it can be used to generate
different data sets and different results for new reconciliations.

---

## Task 2 : Generate/update the README.md

**Priority:** High  
**Category:** Docs  
**Status:** ✅ Completed

### Description
Create a README.md file documenting the project status, tech stack, completed tasks, and next steps. Include tech stack badges and explain that mock data is generated with Polars simulating real-world scenarios.

### Requirements
- [X] Add tech stack badges (Python, DuckDB, dbt, Streamlit, Status)
- [X] Explain in Overview section that mock data is generated with Polars simulating real-world data
- [X] Create "What's Done" section showing current progress (Tasks 1 and 2 completed)
- [X] Create "Next Steps" section with upcoming tasks
- [X] Add Tech Stack table explaining each component
- [X] Include basic setup instructions
- [X] Add project structure overview
- [X] Link to documentation (CLAUDE.md, TASKS.md, skills.md)
- [X] Note that project is work in progress

### Context
- README will be updated constantly as project progresses
- Will be pushed to GitHub (portfolio project)
- Reflects current project status
- Based on CLAUDE.md project structure and guidelines

### Acceptance Criteria
- [X] README.md created and readable
- [X] Badges display correctly
- [X] Clear explanation about mock data using Polars
- [X] Current status reflects completed Tasks 1 and 2
- [X] All sections properly formatted

### Notes
- Living document, will be updated frequently
- Must match project tone (portfolio/showcase quality)

---

## Task 1 : Create project folder structure

**Prioridade:** High  
**Categoria:** Project Setup  
**Status:** ✅ Completed

### Descrição
Criar estrutura de pastas e arquivos para o projeto.

### Requisitos
- [X] Folders that contain sensitive information, such as auths, passwords, tokens, etc, should be included in .gitignore.
- [X] Pastas que são referente aos models do dbt devem ser criadas em models/, e conter as etapas staging, intermediate e marts.
- [X] Folders that are related to dbt, such as tests, and documentation should be created in the finreconciler_dbt/ folder.
- [X] Folders that are related to dbt models (models/) and tests (tests/) should be created in the finreconciler_dbt/models/ (staging, intermediate, marts)
- [X] The folder structure should be organized in a way that makes it easy to read and understand.

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
</details>

<details>
<summary>Template</summary>

## Template


```markdown
## Task: [Descriptive Name]

**Priority:** High / Medium / Low  
**Category:** Models | Tests | Data | Docs | Debug  
**Status:** 🆕 New / 🔄 In Progress / ✅ Done

### Description
[What needs to be done? Why?]

### Requirements
- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Requirement 3

### Context / References
[Links, examples, or context needed]

### Acceptance Criteria
[How will you validate readiness?]

### Notes
[Restrictions, decisions already made, etc]
```
</details>

<details>
<summary>Examples</summary>

## Example 1: Create a dbt Model

```markdown
## Task: Create mart_ap_gl_match Model

**Priority:** High  
**Category:** Models  
**Status:** 🆕 New

### Description
Create model Mart that reconciles AP (Accounts Payable) with GL (General Ledger).
This is the core of the reconciliation project — shows advanced SQL patterns.

### Requirements
- [ ] Model must use FULL OUTER JOIN to find matched/unmatched
- [ ] Must aggregate by vendor + period (year/month)
- [ ] Must calculate variance = ap_amount - gl_amount
- [ ] Must mark status as 'matched' (variance < 0.01) or 'unmatched'
- [ ] Totally documented in schema.yml
- [ ] Tests dbt (not_null, unique key, data quality)
- [ ] SQL comments explaining

### Context
- Staging models already exist: `stg_accounts_payable`, `stg_general_ledger`
- AP amounts must be summed by vendor_id + period
- GL amounts must be summed by department + period (filtering accounts 2010, 2020)
- Use `coalesce()` in FULL JOIN to avoid nulls in key
- See `docs/financial_logic.md` for accounting logic
```

### Acceptance Criteria
```bash
dbt run -s mart_ap_gl_match      # Runs without error
dbt test -s mart_ap_gl_match     # All tests pass
```

Expected result:
- ~50K rows (100K AP × GL aggregated by period)
- ~85% matched, ~15% unmatched (reflects proposed losses in the data)
- Variance range: -50K to +50K USD

### Notes
- Materialized as `table` (not view) — used for BI
- Use macros `safe_divide()` if needed to calculate ratios
- Don't put variance logic here — it's in `mart_variance_monthly`

---

## Example 2: Generate Test Data

```markdown
## Task: Generate 100K AP Records with Realistic Variance

**Priority:** High  
**Category:** Data  
**Status:** 🆕 New

### Description
Extend `scripts/generate_source_data.py` to create AP (Accounts Payable) 
with realistic financial patterns. Used for all pipeline testing.

### Requirements
- [ ] Generate 100,000 records of AP
- [ ] Fields: ap_id, vendor_id, invoice_num, amount, invoice_date, gl_date, status
- [ ] Vendor IDs: 20 vendors (V001-V020)
- [ ] Amounts: realistic distribution (100-50,000 USD)
- [ ] Dates: 90 days of history (last 3 months)
- [ ] Status: 70% paid, 20% pending, 10% disputed
- [ ] **Important:** 5% of records will NOT have match in GL (intentionally)
- [ ] Full docstring (Google style) + type hints
- [ ] Logging informative
- [ ] Seed parameter to reproducibility

### Context
- Code enters `scripts/generate_source_data.py`
- Function must return `pl.DataFrame`
- Data will be saved as CSV in `data/raw/accounts_payable.csv`
- Called by `scripts/init_duckdb.py`
```

### Acceptance Criteria
```bash
python scripts/generate_source_data.py
# Output: "Generated 100,000 AP records in data/raw/"

# Local validation
df = pl.read_csv("data/raw/accounts_payable.csv")
df.shape  # (100000, 7)
df["status"].value_counts()  # ~70K paid, ~20K pending, ~10K disputed
df.filter(pl.col("amount") <= 0).height  # 0 (sem negatives)
```

### Notes
- Mismatched records: do not include in GL (logic is in `generate_general_ledger()`)
- Use `random.seed()` or `pl.Series.shuffle(seed=)` for reproducibility
- Amounts must have realistic variance (not normal distribution — use choices with weights)

---

## Example 3: Create dbt Tests

```markdown
## Task: Add Data Quality Tests for mart_reconciliation_summary

**Priority:** Medium  
**Category:** Tests  
**Status:** 🆕 New

### Description
Add 5+ dbt tests to validate data integrity of reconciliation.
Focus on edge cases: totals match, status is valid, no duplicates, etc.

### Requirements
- [ ] Test 1: `not_null` on critical columns (entity, ap_amount, gl_amount, status)
- [ ] Test 2: `unique` on composite key (entity + year + month)
- [ ] Test 3: Custom SQL assert — totals match between AP and GL (for matched items)
- [ ] Test 4: Custom SQL assert — status must be 'matched' or 'unmatched' (mid-term)
- [ ] All tests documented in schema.yml
- [ ] Tests must use `{{ fail_calc() }}` or `where` to indicate failure

### Context
- Target model: `marts.mart_reconciliation_summary`
- Schema.yml already exists in `models/marts/reconciliation/schema.yml`
- Custom tests in `tests/sql/`
```

### Acceptance Criteria
```bash
dbt test -s mart_reconciliation_summary  # All tests pass

# If proposed failure (to validate test):
dbt test -s mart_reconciliation_summary --select tag:assert  # Expected failure
```

### Notes
- Do not use `singular` tests (deprecated) — use models with `-- config(severity: warn)`
- Tests must be descriptive: `assert_variance_pct_within_tolerance`
- If test fails, it must be clear why (use comments in SQL)

---

## Example 4: Documentation

```markdown
## Task: Write Comprehensive schema.yml for mart_variance_monthly

**Priority:** Medium  
**Category:** Docs  
**Status:** 🆕 New

### Description
Document the `mart_variance_monthly` model fully following CLAUDE.md.
It must include detailed description, primary_key, all tests, and examples.

### Requirements
- [ ] Model description (multi-line, explaining purpose, use, assumptions)
- [ ] Primary key declared (entity + year + month)
- [ ] **Each column documented:**
  - name, description (a concise phrase), data_type (if relevant), tests
- [ ] Tests included:
  - not_null for critical columns
  - unique on composite key
  - accepted_values for variance_bucket
  - relationships if there is FK
- [ ] Example of use / query expected
- [ ] Annotations for financial logic (variance is YTD? MoM? Rolling?)

### Context
- Template: `models/marts/reconciliation/schema.yml` (exists)
- Add new section for `mart_variance_monthly`
```
### Acceptance Criteria
- Schema.yml validates without error (`dbt parse`)
- Each column has description > 5 words
- Each column has ≥1 test
- Documentation is clear without unnecessary technical jargon

### Notes
- Description must explain the **intent**, not just what it is
- Example: Bad: "Month and year of transaction"
- Example: Good: "Fiscal year and month when variance was calculated. Used to join with calendar for reporting."

---

## Example 5: Debug

```markdown
## Task: Debug Test Failure in test_variance_logic

**Priority:** High  
**Category:** Debug  
**Status:** 🔄 In Progress

### Description
Test `assert_variance_pct_within_tolerance` is failing.
Investigate and suggest correction.

### Context of Error
Failure in tests/sql/assert_variance_pct_within_tolerance.sql:
Got 153 rows where variance_pct > 0.05 (5%)
Expected 0 rows.
```

Data has ~100K records, 5% proposed losses → realistic variances.

### Requirements
- [ ] Analyze if it's a bug in SQL or in the test logic
- [ ] If it's a very restrictive test, suggest adjustment
- [ ] If it's a bug, suggest correction in the variance calculation SQL
- [ ] Validate that the correction does not break other tests

### Acceptance Criteria
```bash
dbt test -s test_variance_logic  # Passes
```
### Notes
- Test can be correct — maybe accuracy expectation needs adjustment
- Investigate if 5% of variance is acceptable or not (question: is it a bug or feature?)

---


## Example 6: Feature Streamlit

```markdown
## Task: Add Variance Anomaly Detection to Streamlit

**Priority:** Low  
**Category:** Models + Docs  
**Status:** 🆕 New

### Description
Create Streamlit page (`pages/3_anomalies.py`) that shows variance anomalies
(outliers). Use data from `mart_variance_monthly` for flagging.

### Requirements
- [ ] Sidebar filter: variance_pct range (slider)
- [ ] Sidebar filter: variance_bucket (multiselect)
- [ ] Sidebar filter: entity (multiselect de vendors)
- [ ] Main: Table with anomalies (sorted by variance_pct desc)
- [ ] Visual: Scatter plot (amount vs variance_pct)
- [ ] Metric top: Number of anomalies details, avg variance %

### Context
- Page enters `app/pages/3_anomalies.py`
- Data: `select * from marts.mart_variance_monthly where variance_pct > 0.05`
- Use Altair for visualizations (consistent with project)
```

### Acceptance Criteria
```bash
streamlit run app/app.py
# Navigate to "Anomalies" → Deve mostrar dados + filters + charts
```

### Notes
- Do not create new dependencies (Altair is already in lock)
- Use cache `@st.cache_data` for queries
- Responsive on mobile
</details>