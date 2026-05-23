# .claude/ — Claude Code Documentation Index

**FinReconciler Project | Paulo Santana**

---

## 📚 Documentos Disponíveis

### 1. **CLAUDE.md** — Manual Principal
**Tamanho:** ~2.5KB | **Tempo leitura:** 10-15min

Guia completo para trabalhar com Claude Code neste projeto.

**Contém:**
- Visão geral & propósito de Claude
- Estrutura do projeto
- Padrões & convenções (SQL, Python, dbt)
- Fluxo de trabalho esperado
- Dados & ambiente
- Documentação esperada
- Comunicação & contato

**Quando ler:** Antes de usar Claude Code pela primeira vez

---

### 2. **skills.md** — Capacidades & Checklist
**Tamanho:** ~2.2KB | **Tempo leitura:** 10-15min

Define exatamente o que Claude FAZ e o que NÃO FAZ.

**Contém:**
- ✅ Capacidades (testes, dados, docs, debug, código)
- ❌ Limitações (não executa, não decide arquitetura)
- 🚨 Armadilhas conhecidas (window functions, joins, etc)
- ✓ Checklist pré-submissão (obrigatório)
- 📋 Padrões obrigatórios
- 📊 Performance expectations
- 🔑 Quick reference

**Quando ler:** Antes de cada nova task (review checklist)

---

### 3. **TASKS.md** — Task Template & Exemplos
**Tamanho:** ~2.8KB | **Tempo leitura:** 10min

Como especificar tarefas para Claude Code.

**Contém:**
- Template genérico (copy-paste)
- 6 exemplos detalhados:
  - Criar modelo dbt
  - Gerar dados
  - Criar testes
  - Documentar
  - Debug
  - Feature Streamlit
- Task list ativa
- Tips & melhores práticas

**Quando usar:** SEMPRE que tiver uma nova task

---

## 🚀 Quick Start

### Para você (especificador de tarefas):

1. **Primeira vez:**
   - Leia CLAUDE.md (entenda padrões + fluxo)
   - Leia skills.md (entenda limites)

2. **Cada nova task:**
   - Copie template de TASKS.md
   - Preencha requisitos + contexto + critério
   - Mande para Claude

3. **Antes de aceitar código:**
   - Revise checklist em skills.md
   - Valide localmente (dbt run, testes)

### Para Claude Code (lendo este repo):

1. **Setup inicial:** Leia CLAUDE.md (seções 1-5)
2. **Cada task:** Revise skills.md checklist (seção 4)
3. **Antes de responder:** Use template de TASKS.md

---

## 📖 Leitura Recomendada por Cenário

### "Vou usar Claude Code pela primeira vez"
→ CLAUDE.md (seções 1-5) + skills.md (seções 1-2)

### "Vou especificar uma task"
→ TASKS.md (template + exemplo relevante)

### "Claude sugeriu algo estranho"
→ skills.md (seção 2: O que Claude NÃO FAZ)

### "Preciso validar qualidade do código"
→ skills.md (seção 4: Checklist Pré-Submissão)

### "Qual é o padrão de docstring/SQL?"
→ CLAUDE.md (seção 3: Padrões & Convenções)

### "Como rodar o projeto?"
→ CLAUDE.md (seção 5: Ambiente)

### "Claude disse que não pode fazer X"
→ skills.md (seção 2: O que Claude NÃO FAZ)

---

## 🔄 Workflow Resumido

```
Você escreve task em TASKS.md
         ↓
Claude lê CLAUDE.md + skills.md + sua task
         ↓
Claude usa checklist de skills.md seção 4
         ↓
Claude propõe solução (mostra plano)
         ↓
Você aprova em TASKS.md status
         ↓
Claude cria arquivos
         ↓
Você roda dbt/streamlit localmente
         ↓
Você marca ✅ em TASKS.md
```

---

## 📋 Checklist: Você Está Pronto?

- [ ] Leu CLAUDE.md pelo menos uma vez
- [ ] Entende padrões (SQL lowercase, Python type hints, dbt YAML)
- [ ] Tem template de TASKS.md salvo/bookmarkado
- [ ] Sabe onde verificar capacidades de Claude (skills.md seção 1-2)
- [ ] Sabe como validar qualidade (skills.md seção 4)
- [ ] Ambiente pronto (Python 3.13+, uv, DuckDB)

---

## 🤔 FAQ Rápido

**P: Posso adicionar features extras?**  
R: Veja skills.md seção 2 (O que NÃO FAZ) → Sem features extras.

**P: E se Claude errar em algo?**  
R: Está documentado em skills.md seção 3 (armadilhas).

**P: Como estruturo uma boa task?**  
R: Veja TASKS.md → Template + 6 exemplos.

**P: Qual padrão de código devo usar?**  
R: CLAUDE.md seção 3 → Python, SQL, dbt.

**P: Claude pode refatorar código?**  
R: Só se você pedir (não por iniciativa própria).

---

## 📞 Suporte

- **Dúvida sobre padrões?** → CLAUDE.md seção 3
- **Dúvida sobre capacidades?** → skills.md seção 1-2
- **Como especificar task?** → TASKS.md
- **Erro/bug em código?** → skills.md seção 3 (armadilhas)

---

**Última atualização:** 2026-05-23  
**Versão:** 1.0  
**Status:** Pronto para produção

---

## 📊 Estatísticas dos Documentos

| Doc | Tamanho | Seções | Exemplos | Checklists |
|---|---|---|---|---|
| CLAUDE.md | ~2.5KB | 10 | 3+ | 1 |
| skills.md | ~2.2KB | 10 | 5+ | 5 |
| TASKS.md | ~2.8KB | 8 | 6 | 3 |
| **Total** | **~7.5KB** | **28** | **14+** | **9** |

Tempo total de leitura: ~30-40 minutos para entender tudo.

---

**Próximo passo:** Crie primeira task em TASKS.md e vamos começar! 🚀
