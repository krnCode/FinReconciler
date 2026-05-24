# FinReconciler

A portfolio project demonstrating financial reconciliation and variance analysis using SQL, dbt, and Python.

<!-- Tech Badges -->
![Python](https://img.shields.io/badge/Python-3.13+-blue)
![DuckDB](https://img.shields.io/badge/DuckDB-Latest-teal)
![dbt](https://img.shields.io/badge/dbt-Coming%20Soon-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-1.57+-red)
![Status](https://img.shields.io/badge/Status-Work%20in%20Progress-yellow)

---

## 📋 Overview

FinReconciler is a **work-in-progress** financial reconciliation pipeline that reconciles Accounts Payable (AP) invoices against General Ledger (GL) postings, identifies variance, and surfaces unmatched items for investigation.

**Goal:** Showcase SQL proficiency, scalable data architecture, and test automation for a portfolio.

**Data:** Uses realistic mock data generated with Polars that simulates real-world financial scenarios, including intentional mismatches and variance patterns to test reconciliation logic.

---

## ✅ What's Done

- [x] Project folder structure
- [x] Dependencies configured (DuckDB, Polars, Streamlit, Altair)
- [x] Project documentation (CLAUDE.md, TASKS.md, skills.md)
- [ ] dbt setup
- [ ] Test data generation
- [ ] SQL models (staging → intermediate → marts)
- [ ] dbt tests
- [ ] Streamlit dashboard

---

## 🚀 Next Steps

1. **dbt Setup** — Add dbt to dependencies, configure profiles.yml
2. **Data Generation** — Create 100K realistic records (AP, AR, GL) with intentional mismatches
3. **SQL Models** — Build staging, intermediate, and mart models
4. **Tests** — Add dbt tests for data quality
5. **Streamlit Dashboard** — Visualize reconciliation findings

---

## 🛠️ Tech Stack

| Component | Tech | Purpose |
|---|---|---|
| **Database** | DuckDB | Columnar OLAP for fast aggregations |
| **Data Generation** | Polars | Create realistic test data |
| **Transformation** | dbt + SQL | Data pipeline (staging → marts) |
| **Frontend** | Streamlit | Interactive dashboard |
| **Visualization** | Altair | Charts and graphs |

---

## 📦 Setup (Local Development)

### Prerequisites
- Python 3.13+
- uv (dependency manager)

### Installation

```bash
# Clone and navigate
git clone <repo>
cd finreconciler

# Install dependencies
uv sync
```

### Project Structure

```
finreconciler/
├── finreconciler_dbt/      → dbt project (models, tests, macros)
├── scripts/                → Python scripts (data generation, init)
├── streamlit_app/          → Streamlit dashboard
├── data/                   → Raw data and seeds
└── docs/                   → Documentation
```

---

## 📚 Documentation

- **[CLAUDE.md](./.claude/CLAUDE.md)** — Project manual and guidelines
- **[TASKS.md](./.claude/TASKS.md)** — Task backlog and templates
- **[skills.md](./.claude/skills.md)** — Claude Code capabilities

---

## 📝 Notes

This is a **learning project** for portfolio purposes. It will be updated regularly as features are added.
