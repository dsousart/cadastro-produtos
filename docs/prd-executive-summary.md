# PRD Executive Summary - Evolução Híbrida do Cadastro Premium

**Data:** 2026-02-25 | **Aprovado por:** Morgan (PM) | **Status:** Ready for Architecture

---

## 🎯 Visão Geral

Transformar o **sistema CLI Python** atual em **plataforma híbrida** com API REST e Dashboard Web, mantendo 100% de compatibilidade com CLI e habilitando integrações com e-commerce.

**Objetivo:** Democratizar acesso ao sistema (gestores + desenvolvedores) mantendo excelência técnica.

---

## 📊 Situação Atual vs. Futuro

| Aspecto | Hoje (CLI) | Futuro (Híbrido) |
|---------|------------|------------------|
| **Usuários** | Apenas desenvolvedores | Desenvolvedores + Gestores + Integrações |
| **Interface** | Terminal (Python CLI) | CLI + API REST + Dashboard Web |
| **Deployment** | Local | Cloud (Railway/Render) |
| **Colaboração** | Individual | Multi-usuário (auth + roles) |
| **Integração** | Manual (JSON files) | Automática (API + Webhooks) |
| **BK Management** | Filesystem manual | UI + Filesystem |

---

## 🏗️ Arquitetura Decidida

```
┌─────────────────────────────────────────────────────┐
│                  CAMADA DE ACESSO                   │
├──────────────┬──────────────┬──────────────────────┤
│ CLI (Python) │  API (REST)  │  Dashboard (Web)     │
│   Devs       │  Integrações │  Gestores/Marketing  │
└──────┬───────┴──────┬───────┴──────────┬───────────┘
       │              │                  │
       └──────────────┼──────────────────┘
                      │
              ┌───────▼────────┐
              │  CORE ENGINE   │
              │ (Python 3.14)  │
              │ ✅ Inalterado  │
              └───────┬────────┘
                      │
       ┌──────────────┼──────────────┐
       │              │              │
   ┌───▼───┐    ┌────▼────┐   ┌────▼─────┐
   │  BK   │    │Database │   │E-commerce│
   │(Files)│    │(Postgres)│  │(Shopify) │
   └───────┘    └─────────┘   └──────────┘
```

---

## 💻 Tech Stack Decisões

| Camada | Tecnologia | Rationale |
|--------|-----------|-----------|
| **Core Engine** | Python 3.14 | ✅ Mantido (zero mudanças) |
| **API** | FastAPI + PostgreSQL | Performance, OpenAPI auto, async |
| **Frontend** | Next.js 14 + Shadcn/UI | Modern, SSR/SSG, design system |
| **Auth** | JWT + bcrypt | Stateless, escalável |
| **Deploy** | Railway/Render | Simples, PostgreSQL incluído, ~$30/mês |
| **Processing** | BackgroundTasks (Fase 1) → Celery (Fase 2) | Incremental complexity |
| **BK Storage** | Filesystem (Fase 1) → PostgreSQL FTS (Fase 2) | Compatibilidade first |

---

## 📦 Entregas por Wave

### Wave 1: Foundation (2-3 semanas)
- ✅ API REST completa (`/api/v1/products`, `/batch`)
- ✅ PostgreSQL + migrations
- ✅ Core Python integrado como biblioteca
- **Entregável:** API funcional que processa produtos

### Wave 2: Frontend MVP (2 semanas)
- ✅ Dashboard com lista de cadastros
- ✅ Detail view (preview + editar)
- ✅ Workflow: Draft → Approved → Published
- **Entregável:** UI para gestores revisarem cadastros

### Wave 3: BK Management (1-2 semanas)
- ✅ File tree + preview de markdowns
- ✅ Upload via drag & drop
- ✅ Validação de qualidade
- **Entregável:** Gestão de BK via UI

### Wave 4: Multi-Tenancy & Auth (1 semana)
- ✅ JWT authentication
- ✅ RBAC (admin, editor, viewer)
- ✅ Isolamento de dados por tenant
- **Entregável:** Sistema pronto para múltiplos clientes

### Wave 5: E-commerce Integration (1 semana)
- ✅ Export JSON (Shopify, VTEX, WooCommerce)
- ✅ Webhooks para notificações
- **Entregável:** Integração completa

**Total:** 7-9 semanas para MVP completo

---

## 🎯 Requisitos Críticos (Must-Have)

### Compatibilidade (CR1-CR4)
- ✅ CLI existente funciona **exatamente** como antes
- ✅ API retorna mesmo formato JSON que CLI
- ✅ BK em markdown permanece compatível

### Performance (NFR1, NFR3)
- ✅ Fase 1: 20 produtos simultâneos
- ✅ API: <500ms para consultas
- ✅ Pipeline: <5s por produto

### Segurança (NFR7, NFR12)
- ✅ Guidelines de marca criptografadas
- ✅ JWT authentication
- ✅ RBAC (admin, editor, viewer)
- ✅ Isolamento multi-tenant

---

## 💰 ROI Esperado

### Problemas Resolvidos
1. **Bottleneck técnico:** Gestores dependem de devs para ver cadastros → **Resolvido com Dashboard**
2. **Integração manual:** Copy-paste JSON para Shopify → **Resolvido com Export/API**
3. **Zero observabilidade:** Não sabem qualidade da BK → **Resolvido com Métricas**
4. **Não escala:** 1 produto por vez via CLI → **Resolvido com Batch API**

### Benefícios Quantificáveis
- **Redução 70%** no tempo de publicação (revisão via dashboard vs. CLI)
- **100+ produtos/dia** processados (vs. ~20 manual)
- **Zero downtime** para gestores (API always-on vs. CLI local)
- **SaaS-ready:** Multi-tenant desde MVP (monetização futura)

---

## ⚠️ Riscos e Mitigações

| Risco | Probabilidade | Mitigação |
|-------|---------------|-----------|
| BK filesystem lento (500+ markdowns) | Média | Fase 2: PostgreSQL FTS |
| Core Python sem testes | Alta | ✅ Adicionar pytest antes de API |
| Background tasks sem retry | Alta | Fase 2: Celery + Redis |
| Multi-tenant sem isolamento forte | Média | ✅ Criptografia + RLS desde Fase 1 |

---

## ✅ Success Metrics (MVP)

**Técnicos:**
- CLI 100% funcional (zero regressões)
- API com 20 endpoints implementados
- Dashboard usável (3 telas principais)
- Deploy em produção (Railway/Render)

**Negócio:**
- 10 produtos cadastrados via dashboard por 2+ usuários
- 1 export bem-sucedido para Shopify/VTEX
- 5 markdowns upados via UI
- 3 produtos Draft → Approved → Published

---

## 🚀 Próximos Passos

1. **Arquitetura Técnica** → @architect cria fullstack architecture
2. **Wave 1 Kickoff** → @dev implementa API Foundation
3. **Wave 2-5** → Entrega incremental a cada 1-2 semanas

---

## 📞 Stakeholders

- **Product Manager:** Morgan (este documento)
- **Architect:** Aria (próximo)
- **Lead Developer:** TBD
- **Business Owner:** TBD (aprovação final)

---

**Documento completo:** `docs/prd.md` (22KB, 20 stories detalhadas)

— Morgan, planejando o futuro 📊
