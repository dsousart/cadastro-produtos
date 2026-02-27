# Cadastro de Produtos Premium - Brownfield Enhancement PRD

**Versão:** 2.0
**Data:** 2026-02-25
**Autor:** Morgan (Product Manager)
**Status:** Aprovado para Execução

---

## Change Log

| Data | Versão | Descrição | Autor |
|------|--------|-----------|-------|
| 2026-02-25 | 2.0 | PRD inicial - Evolução Híbrida do Sistema | Morgan (PM) |

---

## 1. Intro Project Analysis and Context

### 1.1 Existing Project Overview

**Analysis Source:** IDE-based fresh analysis + documentação existente (SPEC.md, CLAUDE.md, roadmap)

**Current Project State:**

O **Cadastro de Produtos Premium** é um sistema Python CLI para geração automatizada de conteúdo de e-commerce premium voltado para moda masculina 30+. O sistema transforma fichas técnicas em argumentos de venda com tom premium discreto, estrutura padronizada e foco em redução de devolução.

**Arquitetura Atual:**

```
core/
├── generator.py      # Geração de conteúdo premium (título, descrição, bullets)
├── auditor.py        # Validação e score de qualidade (0-100)
├── refiner.py        # Refinamento iterativo baseado em feedback
├── bk_reader.py      # Leitura de Base de Conhecimento
├── bk_validator.py   # Validação de BK
├── extract_raw.py    # Extração de HTML para texto
└── normalize_to_markdown.py  # Normalização para markdown

pipeline/
├── pipeline.py       # Orquestração principal do fluxo
├── run.py           # CLI runner
├── bk_ingest.py     # Ingestão de BK
├── bk_scraper.py    # Scraper de concorrentes
└── bk_validate.py   # Validação de qualidade da BK
```

**Tech Stack Atual:**
- **Linguagem:** Python 3.14.3
- **Dependências:** Stdlib Python (re, json, typing, datetime, uuid)
- **OCR:** Tesseract (opcional)
- **Formato de dados:** JSON (I/O), Markdown (BK)
- **Deployment:** CLI local (sem cloud deployment)

**O que funciona hoje:**
1. ✅ Pipeline completo: generator → auditor → refiner
2. ✅ Sistema de Base de Conhecimento com confidence score
3. ✅ Scraper de concorrentes com filtros masculinos
4. ✅ OCR opcional em imagens
5. ✅ Auditoria com score 0-100
6. ✅ Estrutura obrigatória de blocos (headline, abertura, benefícios, autoridade, uso, risco)

---

### 1.2 Available Documentation

**Documentação Disponível:**
- ✅ SPEC.md - Especificação completa do sistema
- ✅ CLAUDE.md - Guia para Claude Code
- ✅ docs/roadmap-proximos-passos.md - Plano de próximos passos
- ✅ docs/clone-review-and-plan.md - Análise e decisões
- ✅ docs/stories/ - Stories de desenvolvimento (brownfield)
- ✅ examples-*.json - Exemplos de entrada/saída
- ❌ PRD formal (este documento)
- ❌ Arquitetura técnica formal
- ❌ Diagramas de fluxo

---

### 1.3 Enhancement Scope

**Enhancement Type:**
- ✅ New Feature Addition - API REST e Interface Web
- ✅ Integration with New Systems - Plataformas de e-commerce
- ✅ Performance/Scalability Improvements - Multi-usuário

**Enhancement Description:**

Transformar o sistema CLI Python em uma **plataforma híbrida** que mantém a robustez do pipeline existente e adiciona:

1. **API REST** para integração com plataformas de e-commerce (Shopify, VTEX, WooCommerce)
2. **Dashboard Web** para visualização de resultados, gestão de BK e monitoramento
3. **Arquitetura modular** que permite uso via CLI (desenvolvedores) ou Web (usuários de negócio)

**Objetivo:** Democratizar o acesso ao sistema mantendo a qualidade técnica.

**Impact Assessment:** ✅ **Significant Impact**

- Core Python permanece **intacto** como engine
- Nova camada de API será **wrapper** sobre pipeline existente
- Frontend é **consumidor** da API (baixo acoplamento)
- Arquitetura: **CLI → Core Engine ← API → Frontend**

---

### 1.4 Goals and Background Context

**Goals:**

1. **Democratizar Acesso** - Permitir que usuários não-técnicos usem o sistema via interface web
2. **Habilitar Integrações** - API REST para conectar com plataformas de e-commerce
3. **Melhorar Observabilidade** - Dashboard para monitorar pipeline, BK e qualidade
4. **Escalar Operação** - Suportar múltiplos usuários e produtos simultâneos
5. **Manter Excelência Técnica** - Preservar qualidade do core Python existente
6. **Facilitar Colaboração** - Gestores podem revisar e aprovar cadastros via web

**Background Context:**

O sistema CLI atual é **tecnicamente excelente** para desenvolvedores, mas cria barreiras para:

- **Gestores de e-commerce** que querem revisar cadastros antes da publicação
- **Equipes de marketing** que precisam ajustar tom de voz e guidelines
- **Integrações automatizadas** com Shopify/VTEX que exigem API
- **Escalabilidade operacional** - processar centenas de produtos/dia requer orquestração

**Contexto do mercado:**
- Plataformas de e-commerce oferecem APIs robustas
- Usuários de negócio preferem dashboards visuais a CLI
- Competidores oferecem SaaS, não ferramentas CLI

**Alinhamento com roadmap:**
Este enhancement **complementa** os próximos passos já planejados (parser por domínio, OCR filtrado, validador BK) e **exponencializa** seu valor através da API/dashboard.

---

## 2. Requirements

### 2.1 Functional Requirements

**FR1:** O sistema deve expor uma **API REST** que execute o pipeline completo (generator → auditor → refiner) e retorne JSON estruturado

**FR2:** A API deve permitir **upload de produtos em batch** (até 20 produtos via background tasks; 20+ requer Celery em Fase 2)

**FR3:** O dashboard web deve exibir **histórico de cadastros** com filtros por data, marca, categoria e score de qualidade

**FR4:** O dashboard deve permitir **edição manual** de cadastros. Edições criam nova versão (original preservada para auditoria)

**FR5:** O sistema deve suportar **gestão de Base de Conhecimento via UI** (upload de markdowns, preview, validação)

**FR6:** A API deve oferecer **webhooks opcionais** para notificar quando cadastro está pronto para publicação

**FR7:** O **CLI atual** deve continuar funcionando sem dependência da API/web (compatibilidade total)

**FR8:** Sistema oferece **export one-way** para Shopify/VTEX/WooCommerce (Fase 1: JSON export, Fase 2: API direta)

**FR9:** O dashboard deve exibir **métricas de qualidade da BK** (confidence score, hits, missing terms)

**FR10:** O sistema deve suportar **múltiplos usuários** com autenticação JWT e roles (admin, editor, viewer)

**FR11:** Sistema implementa **workflow de 3 estados**: Draft → Approved → Published

**FR12:** Edições manuais acionam **re-auditoria opcional** (configurável por tenant)

**FR13:** Dashboard permite **upload/preview de BK markdowns** (filesystem backed)

**FR14:** Sistema **indexa BK** para busca rápida (in-memory cache + file scanning)

**FR15:** Sistema suporta **multi-tenancy** com BK compartilhada + overrides por tenant

**FR16:** **Autenticação via JWT** com roles: admin (full access), editor (create/edit), viewer (read-only)

**FR17:** Sistema oferece **export em formato JSON** compatível com Shopify, VTEX, WooCommerce

---

### 2.2 Non-Functional Requirements

**NFR1:** Fase 1 suporta **20 produtos simultâneos**, Fase 2 até **100 produtos** (< 5s por produto)

**NFR2:** O sistema deve manter **compatibilidade com Python 3.14+** e todas as dependências atuais

**NFR3:** Tempo de resposta da API deve ser **< 500ms** para endpoints de consulta (não-processamento)

**NFR4:** Dashboard funciona em **navegadores modernos** (Chrome, Firefox, Safari, Edge - últimas 2 versões)

**NFR5:** Sistema deve ter **99% uptime** em produção (monitoramento e alertas)

**NFR6:** API implementa **rate limiting** (100 req/min por usuário, 1000 req/hora por tenant)

**NFR7:** Dados sensíveis (guidelines de marca, restrições legais) devem ser **criptografados em repouso**

**NFR8:** Sistema suporta **deployment em múltiplos ambientes** (dev, staging, production)

**NFR9:** Logs e auditoria rastreiam **todas as operações** (quem, quando, o quê)

**NFR10:** Core Python mantém **zero dependências externas pesadas** (manter simplicidade atual)

**NFR11:** BK filesystem suporta até **500 markdowns** com performance aceitável (<2s busca)

**NFR12:** Guidelines de marca e restrições legais são **isoladas por tenant** (criptografadas em DB)

**NFR13:** Deploy em **Railway ou Render** com PostgreSQL incluído

**NFR14:** BK armazenada em **volume persistente** (filesystem)

**NFR15:** Monitoramento via **Railway Dashboard** (Fase 1) ou **Sentry** (Fase 2)

---

### 2.3 Compatibility Requirements

**CR1: CLI Compatibility** - O CLI existente (`python pipeline/run.py`) funciona **exatamente como antes**, sem mudanças breaking

**CR2: Output Format Compatibility** - A API retorna JSON no **mesmo formato** que o CLI atual

**CR3: BK Format Compatibility** - A Base de Conhecimento em **markdown** permanece compatível

**CR4: Python Version Compatibility** - Manter compatibilidade com **Python 3.14+**

---

## 3. User Interface Enhancement Goals

### 3.1 Integration with Existing UI

**Contexto:** Este é um projeto **greenfield** para interface web (não há UI atual).

**Princípios de Design:**

1. **Clean & Minimal** - Interface focada em produtividade
2. **Dashboard-First** - Overview de cadastros (não formulários)
3. **Progressive Disclosure** - Detalhes sob demanda
4. **Responsive** - Desktop (primário) e tablet (secundário)

**Design System:**
- **Componentes:** shadcn/ui (Tailwind CSS + Radix UI)
- **Cores:** Brand-agnostic (configurável por tenant)
- **Tipografia:** Inter
- **Icons:** Lucide Icons

---

### 3.2 Modified/New Screens and Views

**1. Dashboard (Home)**
- Overview de cadastros recentes e métricas
- Cards: total cadastros, score médio, pending approval
- Tabela de cadastros com filtros
- Gráfico de qualidade da BK

**2. Cadastro Detail View**
- Tabs: Preview | Editar | Auditoria | Histórico
- Preview renderizado como e-commerce
- Formulário de edição
- Score breakdown
- Diff view de versões

**3. Base de Conhecimento Manager**
- File tree (estilo VSCode)
- Preview pane (markdown renderizado)
- Upload de novos markdowns
- Validação em tempo real

**4. Batch Upload**
- Drag & drop JSON file
- Progress bar
- Resultados com links

**5. Settings**
- Guidelines de marca
- Restrições legais
- Integração com e-commerce
- Usuários e permissões

---

### 3.3 UI Consistency Requirements

**UC1:** Layout consistente (sidebar + header + content)

**UC2:** Feedback visual para operações assíncronas

**UC3:** Estados vazios com ilustrações e CTAs

**UC4:** Mensagens de erro actionable

**UC5:** Validação client-side em formulários

---

## 4. Technical Constraints and Integration Requirements

### 4.1 Existing Technology Stack

| Categoria | Tecnologia | Versão | Constraints |
|-----------|-----------|--------|-------------|
| **Language** | Python | 3.14.3 | Core engine não pode mudar versão |
| **Core Modules** | `core/`, `pipeline/` | - | Devem permanecer funcionais standalone |
| **Data Format** | JSON (I/O), Markdown (BK) | - | Formatos não podem mudar |
| **OCR** | Tesseract | - | Path configurável via env var |
| **Dependencies** | Stdlib Python | - | Manter zero deps pesadas |

---

### 4.2 Integration Approach

**Database Integration:**
- PostgreSQL para metadados (cadastros, usuários, auditoria)
- **Não armazena:** BK (permanece em filesystem)
- **Armazena:** Resultados, histórico de versões, configurações

**Schema:**
```sql
- tenants (id, name, settings)
- users (id, tenant_id, email, role, jwt_hash)
- products (id, tenant_id, sku, input_json, output_json, status, score, created_at)
- product_versions (id, product_id, output_json, edited_by, created_at)
- bk_files (id, tenant_id, path, hash, indexed_at)
```

**API Integration:**
- FastAPI como framework
- Endpoints: `/api/v1/products`, `/api/v1/bk`, `/api/v1/export`
- Core Python importado como biblioteca

**Frontend Integration:**
- Next.js 14 (App Router)
- SSG para landing, SSR para dashboard
- API calls via fetch/SWR

**Testing:**
- Core: pytest
- API: pytest + httpx
- Frontend: Vitest + Testing Library
- E2E: Playwright

---

### 4.3 Code Organization

```
cadastro-premium/
├── core/                    # ✅ EXISTENTE
├── pipeline/                # ✅ EXISTENTE
├── api/                     # 🆕 NOVO
│   ├── main.py
│   ├── routers/
│   ├── models/
│   ├── services/
│   └── utils/
├── web/                     # 🆕 NOVO
│   ├── app/
│   ├── components/
│   └── lib/
├── base_conhecimento/       # ✅ EXISTENTE
├── docs/
│   └── prd.md              # 🆕 Este documento
└── README.md
```

**Naming Conventions:**
- Python: snake_case
- TypeScript: camelCase (vars), PascalCase (components)
- Database: snake_case
- API: kebab-case

---

### 4.4 Deployment and Operations

**Build Process:**
- Core: sem build (interpretado)
- API: `pip install -r requirements.txt && uvicorn api.main:app`
- Web: `cd web && npm install && npm run build`

**Deployment:**
- Plataforma: Railway ou Render
- Services: API (FastAPI), Web (Next.js), PostgreSQL
- Volume: BK filesystem

**Monitoring:**
- Fase 1: Railway Dashboard
- Fase 2: Sentry + Grafana

**Configuration:**
- `.env` files (local)
- Railway env vars (prod)
- Secrets encrypted

---

### 4.5 Risk Assessment

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| BK filesystem lento (500+ markdowns) | Média | Alto | Fase 2: PostgreSQL FTS |
| Background tasks sem retry | Alta | Médio | Celery em Fase 2 |
| Core Python sem testes | Alta | Alto | Adicionar pytest antes de API |
| OCR path hardcoded | Média | Baixo | Env var configurável |
| Sem versionamento de API | Baixa | Médio | `/api/v1/` desde início |
| Multi-tenant sem isolamento | Média | Alto | Criptografia + RLS |

---

## 5. Epic and Story Structure

### Epic Approach

**Decisão:** Single Epic com Waves Sequenciais

**Rationale:**
- Enhancement coeso (transformação CLI → Híbrido)
- Waves permitem entrega incremental

**Epic Structure:**
```
Epic 1: Evolução Híbrida do Sistema de Cadastro Premium
├── Wave 1: Foundation (API + Core Integration)
├── Wave 2: Frontend MVP (Dashboard básico)
├── Wave 3: BK Management (UI para BK)
├── Wave 4: Multi-Tenancy & Auth
└── Wave 5: E-commerce Integration
```

---

## 6. Epic 1: Evolução Híbrida - Stories Detalhadas

**Epic Goal:** Transformar CLI Python em plataforma híbrida com API REST e Dashboard Web, mantendo 100% compatibilidade.

---

### Wave 1: Foundation (API + Core Integration)

#### Story 1.1: Estrutura do Projeto API

**As a** desenvolvedor,
**I want** estrutura de projeto FastAPI,
**so that** a API seja manutenível e escalável.

**Acceptance Criteria:**
1. ✅ Estrutura de diretórios criada
2. ✅ FastAPI app inicializado com `/healthz` endpoint (e `/readyz` recomendado)
3. ✅ `requirements.txt` com fastapi, uvicorn, pydantic
4. ✅ `.env.example` atualizado
5. ✅ README com instruções de setup
6. ✅ API roda: `uvicorn api.main:app --reload`

**Integration Verification:**
- IV1: CLI existente continua funcionando
- IV2: Core Python importável na API
- IV3: Estrutura não quebra AIOS framework

---

#### Story 1.2: Schemas Pydantic

**As a** desenvolvedor da API,
**I want** schemas Pydantic para validação,
**so that** API tenha validação automática.

**Acceptance Criteria:**
1. ✅ `ProductInput` schema criado
2. ✅ Valida campos obrigatórios (SPEC.md)
3. ✅ `ProductOutput` schema criado
4. ✅ Tipos Python corretos
5. ✅ OpenAPI docs (`/docs`) funcional

**Integration Verification:**
- IV1: Schemas compatíveis com `examples-*.json`
- IV2: Validação rejeita JSONs inválidos
- IV3: Não altera core Python

---

#### Story 1.3: Endpoint POST /api/v1/products

**As a** usuário da API,
**I want** enviar produto via POST,
**so that** receba cadastro premium.

**Acceptance Criteria:**
1. ✅ Endpoint `POST /api/v1/products` criado
2. ✅ Aceita `ProductInput`, retorna `ProductOutput`
3. ✅ Chama `pipeline.run_pipeline()`
4. ✅ Status 201 (Created) com resultado
5. ✅ Status 422 para input inválido
6. ✅ Status 500 se pipeline falhar
7. ✅ Response inclui `audit_id`, `timestamp`

**Integration Verification:**
- IV1: Pipeline via API = mesmo resultado que CLI
- IV2: Teste comparativo CLI vs API
- IV3: Core Python não modificado

---

#### Story 1.4: Endpoint POST /api/v1/generation-jobs (batch)

**As a** usuário da API,
**I want** enviar múltiplos produtos em background,
**so that** não espere 5s × N sincronamente.

**Acceptance Criteria:**
1. ✅ Endpoint `POST /api/v1/generation-jobs` criado
2. ✅ Aceita array (limite: 20 produtos)
3. ✅ Retorna 202 com `job_id`
4. ✅ Usa `BackgroundTasks`
5. ✅ Endpoint `GET /api/v1/generation-jobs/{id}` retorna status
6. ✅ Retorna array de resultados quando completo
7. ✅ >20 produtos retorna erro 400

**Integration Verification:**
- IV1: Cada produto processado pelo pipeline Python
- IV2: Falha em 1 não impede outros
- IV3: Background tasks não bloqueiam API
- IV4: Aliases temporários (`/products/batch`, `/batches/{id}`) são opcionais durante transição, se necessário

---

#### Story 1.5: Database Setup (PostgreSQL)

**As a** desenvolvedor,
**I want** PostgreSQL com schema inicial,
**so that** API armazene metadados.

**Acceptance Criteria:**
1. ✅ PostgreSQL rodando (Docker/Railway)
2. ✅ Alembic configurado
3. ✅ Migration inicial: tenants, users, products, generation_jobs
4. ✅ SQLAlchemy models criados
5. ✅ `DATABASE_URL` configurável
6. ✅ Migration aplicada: `alembic upgrade head`

**Integration Verification:**
- IV1: BK permanece em filesystem
- IV2: Core Python não depende de DB
- IV3: API funciona com DB vazio

---

#### Story 1.6: Persistência de Resultados

**As a** usuário da API,
**I want** resultados salvos no DB,
**so that** possa consultá-los depois.

**Acceptance Criteria:**
1. ✅ `POST /api/v1/products` salva no DB
2. ✅ Tabela `products` populada
3. ✅ `GET /api/v1/products` retorna lista paginada
4. ✅ `GET /api/v1/products/{id}` retorna específico
5. ✅ Filtros: `?status=`, `?min_score=`
6. ✅ Response com metadata de paginação

**Integration Verification:**
- IV1: CLI não salva em DB (inalterado)
- IV2: API processa mesmo produto múltiplas vezes
- IV3: DB é opcional (modo stateless para testes)

---

### Wave 2: Frontend MVP

#### Story 1.7: Setup Next.js com Shadcn/UI

**As a** desenvolvedor frontend,
**I want** Next.js configurado,
**so that** crie UI consistente.

**Acceptance Criteria:**
1. ✅ Next.js 14 criado em `web/`
2. ✅ Shadcn/UI inicializado
3. ✅ Componentes instalados
4. ✅ Tailwind configurado
5. ✅ Layout base criado
6. ✅ Página inicial placeholder
7. ✅ `npm run dev` funciona

**Integration Verification:**
- IV1: Frontend isolado
- IV2: Componentes renderizam sem backend
- IV3: Build estático funciona

---

#### Story 1.8: Dashboard Home - Lista de Cadastros

**As a** gestor,
**I want** ver lista de cadastros,
**so that** monitore pipeline.

**Acceptance Criteria:**
1. ✅ Página `/dashboard` com tabela
2. ✅ Colunas: SKU, Nome, Marca, Score, Status, Data
3. ✅ Fetch via API com SWR
4. ✅ Filtros: Busca, Status, Score
5. ✅ Paginação: 50/página
6. ✅ Badges coloridos
7. ✅ Click abre detail view

**Integration Verification:**
- IV1: Dashboard funciona com array vazio
- IV2: Erros de API não quebram UI
- IV3: Atualiza automaticamente

---

#### Story 1.9: Product Detail View

**As a** gestor,
**I want** ver detalhes e editar,
**so that** ajuste antes de publicar.

**Acceptance Criteria:**
1. ✅ Página `/dashboard/products/[id]`
2. ✅ Tabs: Preview | Editar | Auditoria | Histórico
3. ✅ Preview renderizado
4. ✅ Formulário de edição
5. ✅ Score breakdown
6. ✅ Diff view de versões
7. ✅ Botão "Salvar Edição"
8. ✅ Preserva original

**Integration Verification:**
- IV1: Edições não afetam core Python
- IV2: Re-audit opcional
- IV3: Original sempre acessível

---

#### Story 1.10: Workflow de Status

**As a** gestor,
**I want** aprovar cadastros,
**so that** só conteúdo de qualidade vá para e-commerce.

**Acceptance Criteria:**
1. ✅ Endpoint `PATCH /api/v1/products/{id}/status`
2. ✅ Aceita `{"status": "approved|published"}`
3. ✅ Validação: Draft → Approved → Published
4. ✅ Botões condicionais na UI
5. ✅ Badge atualiza em tempo real
6. ✅ Filtro por status funcional

**Integration Verification:**
- IV1: Status é metadata
- IV2: CLI não tem status
- IV3: Mudança registrada em logs

---

### Wave 3: BK Management

#### Story 1.11: Endpoint GET /api/v1/bk

**As a** usuário da API,
**I want** listar markdowns da BK,
**so that** navegue via web.

**Acceptance Criteria:**
1. ✅ Endpoint `GET /api/v1/bk`
2. ✅ Lista `base_conhecimento/` recursively
3. ✅ Response: path, size, modified_at
4. ✅ Filtro: `?domain=`, `?search=`
5. ✅ Performance: <2s para 500 markdowns

**Integration Verification:**
- IV1: BK em filesystem
- IV2: Core Python lê filesystem
- IV3: Funciona se BK vazio

---

#### Story 1.12: Endpoint GET /api/v1/bk/{path}

**As a** usuário da API,
**I want** ler markdown específico,
**so that** exiba preview.

**Acceptance Criteria:**
1. ✅ Endpoint `GET /api/v1/bk/{path}`
2. ✅ Retorna content + metadata
3. ✅ Response: path, content, size, modified_at
4. ✅ Validação: path dentro de `base_conhecimento/`
5. ✅ Retorna 404 se não existir

**Integration Verification:**
- IV1: Read-only
- IV2: Não interfere com core Python
- IV3: Suporta frontmatter YAML

---

#### Story 1.13: BK Manager UI

**As a** gestor de conteúdo,
**I want** navegar BK,
**so that** revise conhecimento.

**Acceptance Criteria:**
1. ✅ Página `/dashboard/bk`
2. ✅ Layout: File tree + Preview
3. ✅ Tree hierárquica
4. ✅ Preview renderizado
5. ✅ Busca por nome
6. ✅ Ícones por tipo

**Integration Verification:**
- IV1: Read-only
- IV2: Preview não altera arquivo
- IV3: Tree atualiza com novos markdowns

---

#### Story 1.14: Upload de Markdowns

**As a** gestor de conteúdo,
**I want** upload via drag & drop,
**so that** adicione conhecimento sem terminal.

**Acceptance Criteria:**
1. ✅ Endpoint `POST /api/v1/bk`
2. ✅ Aceita `.md` files
3. ✅ Valida: markdown válido, UTF-8
4. ✅ Salva em `base_conhecimento/{tenant_id}/`
5. ✅ Retorna 201 com path
6. ✅ UI: Drag & drop + upload button
7. ✅ Progress bar
8. ✅ Mensagem sucesso/erro

**Integration Verification:**
- IV1: Markdowns upados lidos pelo core Python
- IV2: Respeita estrutura de diretórios
- IV3: Validação de encoding

---

#### Story 1.15: Validação de Qualidade da BK

**As a** gestor de conteúdo,
**I want** validar markdowns,
**so that** BK mantenha padrão.

**Acceptance Criteria:**
1. ✅ Endpoint `POST /api/v1/bk/validate`
2. ✅ Retorna score de qualidade
3. ✅ Validações: tamanho, densidade técnica, estrutura, encoding
4. ✅ Response: valid, score, issues
5. ✅ UI: validação em tempo real
6. ✅ Upload bloqueado se score < 60

**Integration Verification:**
- IV1: Usa critério de `pipeline/bk_validate.py`
- IV2: Não re-valida existentes
- IV3: Threshold configurável

---

### Wave 4: Multi-Tenancy & Auth

#### Story 1.16: JWT Authentication

**As a** usuário,
**I want** login com email/senha,
**so that** acesse API com segurança.

**Acceptance Criteria:**
1. ✅ Endpoint `POST /api/v1/auth/login`
2. ✅ Retorna JWT
3. ✅ JWT: user_id, tenant_id, role, exp (24h)
4. ✅ Password hashing com bcrypt
5. ✅ Middleware valida JWT
6. ✅ Endpoints protegidos retornam 401
7. ✅ Endpoint `POST /api/v1/auth/register`

**Integration Verification:**
- IV1: CLI sem auth
- IV2: Endpoints públicos: `/healthz`, `/readyz`, `/docs` (`/health` pode ser alias temporário)
- IV3: JWT secret configurável

---

#### Story 1.17: RBAC

**As a** admin,
**I want** definir roles,
**so that** controle acesso.

**Acceptance Criteria:**
1. ✅ Roles: admin, editor, viewer
2. ✅ Decorator `@require_role("admin")`
3. ✅ Permissions definidas
4. ✅ Endpoint `GET /api/v1/users/me`
5. ✅ UI baseada em role

**Integration Verification:**
- IV1: RBAC apenas na API
- IV2: Acesso não-autorizado retorna 403
- IV3: Roles editadas apenas por admin

---

#### Story 1.18: Multi-Tenancy

**As a** tenant,
**I want** dados isolados,
**so that** concorrentes não vejam minha BK.

**Acceptance Criteria:**
1. ✅ Middleware extrai `tenant_id` do JWT
2. ✅ Queries filtram por `tenant_id`
3. ✅ BK: `base_conhecimento/{tenant_id}/`
4. ✅ Guidelines criptografadas
5. ✅ `GET /api/v1/products` filtra por tenant
6. ✅ Outro tenant retorna 404

**Integration Verification:**
- IV1: BK `_global/` acessível por todos
- IV2: Tenant overrides têm prioridade
- IV3: Core Python sem conceito de tenant

---

### Wave 5: E-commerce Integration

#### Story 1.19: Export para JSON

**As a** gestor,
**I want** exportar para minha plataforma,
**so that** importe sem reescrever.

**Acceptance Criteria:**
1. ✅ Endpoint `GET /api/v1/products/{id}/export?platform=shopify`
2. ✅ Plataformas: shopify, vtex, woocommerce
3. ✅ Mapeamento de campos
4. ✅ Response: JSON da plataforma
5. ✅ UI: Botão "Exportar" com dropdown
6. ✅ Download de JSON

**Integration Verification:**
- IV1: Export usa output do core Python
- IV2: Funciona para qualquer status
- IV3: JSON validado com schemas oficiais

---

#### Story 1.20: Webhooks

**As a** desenvolvedor de integração,
**I want** webhook quando pronto,
**so that** automatize publicação.

**Acceptance Criteria:**
1. ✅ Endpoint `POST /api/v1/webhooks`
2. ✅ Aceita url, events
3. ✅ Dispara POST quando status muda
4. ✅ Payload: event, product_id, timestamp
5. ✅ Retry: 3 tentativas com backoff
6. ✅ Logs de deliveries

**Integration Verification:**
- IV1: Webhooks opcionais
- IV2: Falha não bloqueia status
- IV3: Delivery async

---

## 7. Success Metrics & Roadmap

### Success Criteria (Programa completo - Waves 1-5)

**Nota:** O kickoff da **Wave 1** deve usar como crit?rio principal o escopo das stories `1.1`-`1.6` + requisitos de compatibilidade (CR1-CR4), e n?o o pacote completo de 20 stories.

**Técnicos:**
1. ✅ CLI 100% funcional
2. ✅ API com 20 stories implementadas
3. ✅ Dashboard usável
4. ✅ Performance: <500ms consulta, <5s processamento
5. ✅ Deploy em Railway/Render

**Negócio:**
1. ✅ 10 produtos cadastrados via dashboard por 2+ usuários
2. ✅ Export bem-sucedido para Shopify/VTEX
3. ✅ 5 markdowns upados via UI
4. ✅ 3 produtos Draft → Approved → Published

### Roadmap Fase 2

| Feature | Prioridade |
|---------|------------|
| Celery + Redis (100+ produtos) | Alta |
| PostgreSQL FTS (BK database) | Média |
| Sentry Monitoring | Alta |
| API Direta E-commerce | Média |
| Scheduled Publishing | Baixa |
| Colaboração Real-time | Baixa |

---

## 8. Next Steps

1. **Arquitetura Técnica** - Ativar @architect para criar fullstack architecture
2. **Epic Execution** - Usar `@pm *execute-epic` para começar desenvolvimento
3. **Wave 1** - Começar com Foundation (API + Core Integration)

---

**Aprovado por:** Morgan (Product Manager)
**Data de Aprovação:** 2026-02-25

— Morgan, planejando o futuro 📊
