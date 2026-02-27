# Fullstack Architecture - Work in Progress

**Status:** Secoes 1-15 Completas (100%)
**Data:** 2026-02-26
**Arquiteto:** Aria (@architect)

---

## ℹ️ Informações Importantes

**Este documento contém o progresso PARCIAL da arquitetura fullstack.**

- **Completo:** Secoes 1-15 (Introduction -> Appendices)
- **Pendente:** Nenhuma (arquitetura completa)
- **Proximo passo:** Consolidar em `docs/architecture.md` e revisar aprovacao

**Para retomar:** Ver `docs/next-steps-architecture.md`

---

## 1. Introduction

### 1.1 Project Overview

Este documento define a arquitetura fullstack para evolução do **Sistema de Cadastro Premium de Produtos** de CLI Python para plataforma híbrida (CLI + API REST + Dashboard Web).

**Contexto:**
- **Tipo de projeto**: Brownfield evolution (core existente será preservado)
- **Objetivo**: Democratizar acesso mantendo compatibilidade 100% com CLI
- **Usuários atuais**: Desenvolvedores via terminal
- **Usuários futuros**: Desenvolvedores + Gestores + Integrações E-commerce

**Requisitos de compatibilidade críticos (CR1-CR4):**
- CR1: CLI Python funciona exatamente como antes
- CR2: API retorna mesmo formato JSON que CLI
- CR3: Base de conhecimento markdown permanece compatível
- CR4: Pipeline de 7 etapas inalterado

### 1.2 Starter Template Assessment

**Para Camada API/Web (Greenfield):**
- ✅ Pode usar starter template Next.js + FastAPI
- ✅ Database schema design do zero
- ✅ Auth system from scratch

**Para Core Engine (Brownfield):**
- ❌ NÃO usar template (código existente)
- ✅ Core vira biblioteca compartilhada
- ✅ Adapter pattern para integração

**Decisão arquitetural**: Hybrid approach
- Frontend/API: Modern stack (Next.js 14 + FastAPI)
- Core: Existing Python 3.14 wrapped as library

---

## 2. High Level Architecture

### 2.1 Technical Summary

**Arquitetura de 3 camadas:**

```
┌─────────────────────────────────────────────┐
│         CAMADA DE ACESSO                    │
├──────────────┬──────────────┬───────────────┤
│ CLI (Python) │  API (REST)  │ Dashboard Web │
│   Devs       │  Integrações │ Gestores      │
└──────┬───────┴──────┬───────┴──────┬────────┘
       │              │              │
       └──────────────┼──────────────┘
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

### 2.2 Platform and Infrastructure Choice

**Escolha: Railway**

| Critério | Railway | Render | Vercel | Rationale |
|----------|---------|--------|--------|-----------|
| **PostgreSQL** | ✅ Incluído ($0 extra) | ✅ $25/mês | ❌ Externo (~$20 Supabase) | Railway mais econômico |
| **Custo Total** | ~$30/mês | ~$50/mês | ~$70/mês | Railway vence |
| **Preview Deploys** | ✅ Por PR | ✅ Por PR | ✅ Por PR | Empate |
| **Build Time** | Fast (Nixpacks) | Medium | Fast (Vercel) | Railway/Vercel empatados |
| **Monorepo Support** | ✅ Nativo | 🟡 Manual | ✅ Nativo | Railway/Vercel empatados |

**Decisão:** Railway (PostgreSQL incluído, menor custo, monorepo nativo)

### 2.3 Repository Structure

**Monorepo com npm workspaces:**

```
.
├── api/                      # FastAPI backend
│   ├── app/
│   │   ├── routers/
│   │   ├── services/
│   │   ├── models/
│   │   └── main.py
│   └── requirements.txt
│
├── web/                      # Next.js 14 frontend
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── package.json
│
├── core/                     # Existing Python engine (biblioteca)
│   ├── generator.py
│   ├── auditor.py
│   ├── refiner.py
│   └── bk_reader.py
│
├── pipeline/                 # CLI (mantido como está)
│   └── run.py
│
├── base_conhecimento/        # Markdown BK (Fase 1)
│
├── package.json             # Root workspace
└── railway.json             # Deploy config
```

### 2.4 High Level Architecture Diagram

```mermaid
flowchart TB
    subgraph "Camada de Acesso"
        CLI[CLI Python<br/>pipeline/run.py]
        API[API REST<br/>FastAPI]
        Web[Dashboard Web<br/>Next.js 14]
    end

    subgraph "Camada de Negócio"
        Core[Core Engine<br/>generator + auditor + refiner]
        BKReader[BK Reader]
    end

    subgraph "Camada de Dados"
        PG[(PostgreSQL<br/>Products, Users, Tenants)]
        FS[/Filesystem<br/>base_conhecimento/]
        Ecom[E-commerce<br/>Shopify API]
    end

    CLI -->|import core| Core
    API -->|Core Adapter| Core
    Web -->|HTTP calls| API

    Core -->|read BK| BKReader
    BKReader -->|Fase 1| FS
    BKReader -.->|Fase 2| PG

    API -->|SQL| PG
    API -.->|Fase 5| Ecom

    style Core fill:#4CAF50
    style CLI fill:#2196F3
    style API fill:#FF9800
    style Web fill:#9C27B0
```

### 2.5 Architectural Patterns

**1. Layered Architecture**
- **Presentation** (CLI, API, Web) → **Business** (Core Engine) → **Data** (PostgreSQL, Filesystem)
- Separação clara de responsabilidades
- Core isolado de mudanças na apresentação

**2. Adapter Pattern**
- Core Engine inalterado (brownfield)
- `CoreAdapter` wraps existing modules
- Mantém compatibilidade (CR1-CR4)

**3. Multi-Tenant SaaS**
- Shared database com `tenant_id`
- Row Level Security (RLS) no PostgreSQL
- BK global (`_global/`) + overrides por tenant

**4. Backend for Frontend (BFF)**
- Next.js chama API (não core diretamente)
- API agrega dados de múltiplas fontes
- Otimizações específicas por cliente (mobile futuro)

**5. Repository Pattern**
- Abstração de acesso a dados (ProductRepository, UserRepository)
- Facilita testes (mock repositories)
- Migração futura (PostgreSQL → NoSQL se necessário)

---

## 3. Tech Stack

### 3.1 Complete Technology Matrix

| Category | Technology | Version | Rationale |
|----------|-----------|---------|-----------|
| **Frontend Language** | TypeScript | 5.3+ | Type safety, IntelliSense, reduz bugs em runtime |
| **Frontend Framework** | Next.js | 14.x (App Router) | SSR/SSG, API routes, otimização automática |
| **UI Component Library** | Shadcn/UI | Latest | Headless (Radix UI), customizável, sem vendor lock-in |
| **State Management** | React Query (TanStack Query) | 5.x | Server state sync, cache automático, devtools |
| **Backend Language** | Python | 3.14 | Compatibilidade total com core existente |
| **Backend Framework** | FastAPI | 0.110+ | Performance (async), OpenAPI auto, validação Pydantic |
| **API Style** | REST | - | Simplicidade, compatibilidade com CLI JSON |
| **Primary Database** | PostgreSQL | 16+ | ACID, FTS (Fase 2), JSON support, RLS multi-tenant |
| **Cache** | Redis | 7.x (Fase 2) | Background tasks (Celery), sessions, rate limiting |
| **File Storage** | Filesystem | - (Fase 1) | Compatibilidade BK markdown |
| **Authentication** | JWT + bcrypt | PyJWT 2.8+, bcrypt 4.1+ | Stateless, escalável, secure hashing (cost 12) |
| **Backend Testing** | Pytest | 8.x | Padrão Python, fixtures, coverage integrado |
| **Frontend Testing** | Vitest + Testing Library | Vitest 1.x | Compatível Vite (Next.js), rápido |
| **Build Tool** | Turbo (Next.js built-in) | - | Bundling otimizado, tree-shaking |
| **Package Manager** | npm | 10+ | Workspaces para monorepo, lock file confiável |
| **CI/CD** | GitHub Actions | - | Grátis, integração nativa GitHub |
| **Deployment** | Railway | - | PostgreSQL incluído, ~$30/mês, zero config |
| **Monitoring** | Railway Metrics | - (Fase 1) | Built-in (CPU, RAM), upgrade Sentry Fase 3+ |
| **Logging** | Python logging + Railway | - | Structured logs (JSON), Railway log aggregation |
| **CSS Framework** | Tailwind CSS | 3.4+ | Utility-first, tree-shaking, design system |
| **ORM** | SQLAlchemy | 2.0+ (async) | Python padrão, migrations (Alembic), type hints |
| **Migrations** | Alembic | 1.13+ | SQLAlchemy integrado, versionamento, rollback |
| **Background Tasks** | FastAPI BackgroundTasks | - (Fase 1) | Simples MVP, migra Celery quando >100 produtos/dia |

### 3.2 Migration Path (Fase 1 → Fase 2+)

| Component | Fase 1 (MVP) | Fase 2 (Escala) | Trigger |
|-----------|--------------|-----------------|---------|
| **Background Tasks** | FastAPI BackgroundTasks | Celery + Redis | >100 produtos/dia |
| **BK Storage** | Filesystem markdown | PostgreSQL FTS | >500 markdowns OU busca >2s |
| **Monitoring** | Railway Metrics | Sentry + DataDog | Deploy produção clientes pagantes |
| **Cache** | None | Redis | API latency >500ms P95 |

---

## 4. Data Models

### 4.1 Entity Relationship Diagram

```mermaid
erDiagram
    tenants ||--o{ users : "has"
    tenants ||--o{ products : "owns"
    tenants ||--o{ brand_guidelines : "configures"
    users ||--o{ products : "creates"
    products ||--o{ product_versions : "has_history"
    products ||--o{ product_images : "has"
    products }o--o{ categories : "belongs_to"

    tenants {
        uuid id PK
        string name UK
        string slug UK
        jsonb settings
        timestamp created_at
    }

    users {
        uuid id PK
        uuid tenant_id FK
        string email UK
        string password_hash
        enum role
        timestamp last_login
    }

    products {
        uuid id PK
        uuid tenant_id FK
        string sku UK
        string status
        jsonb input_data
        jsonb normalized_attributes
        jsonb generated_content
        int quality_score
        timestamp deleted_at
    }
```

### 4.2 Key PostgreSQL Tables

**products** (Core Entity):
```sql
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    created_by UUID NOT NULL REFERENCES users(id),
    sku VARCHAR(100) NOT NULL,
    status VARCHAR(20) CHECK (status IN ('draft', 'approved', 'published')),
    input_data JSONB NOT NULL,
    normalized_attributes JSONB,
    generated_content JSONB,
    quality_score INTEGER CHECK (quality_score BETWEEN 0 AND 100),
    created_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP,
    UNIQUE(tenant_id, sku)
);

-- RLS Policy
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation_products ON products
    USING (tenant_id = current_setting('app.current_tenant_id')::uuid);
```

### 4.3 Filesystem Structure (BK - Fase 1)

```
base_conhecimento/
├── _global/                    # Shared BK
│   ├── categoria/
│   │   └── camisas.md
│   └── tecidos/
│       └── algodao.md
│
└── {tenant_slug}/              # Tenant overrides
    └── marca/
        └── guidelines.md
```

---

## 5. API Specification

### 5.1 Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/login` | Authenticate & get tokens | ❌ |
| POST | `/auth/refresh` | Refresh access token | ❌ (refresh token) |
| GET | `/auth/me` | Get current user | ✅ |

**Login Example:**
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecureP@ss123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "expires_in": 3600,
  "user": {
    "id": "...",
    "email": "user@example.com",
    "role": "editor",
    "tenant_id": "..."
  }
}
```

### 5.2 Product Endpoints

| Method | Endpoint | Description | Role |
|--------|----------|-------------|------|
| GET | `/products` | List products (paginated) | viewer+ |
| POST | `/products` | Create product (runs pipeline) | editor+ |
| PATCH | `/products/{id}/status` | Change status workflow | editor+ |
| DELETE | `/products/{id}` | Soft delete | admin |

**Create Product Example:**
```http
POST /api/v1/products
Authorization: Bearer {token}

{
  "sku": "CAM-001",
  "nome_produto": "Camisa Social Slim Fit",
  "marca": "Premium Brand",
  "categoria": "camisas-sociais",
  "tamanhos": ["P", "M", "G"],
  "cores": ["branco", "azul-claro"],
  "preco": 189.90,
  "imagens": ["https://cdn.example.com/img1.jpg"]
}
```

### 5.3 Error Handling

**Standard Error Response:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid product data",
    "details": [
      {
        "field": "preco",
        "issue": "must be greater than 0"
      }
    ]
  }
}
```

**HTTP Status Codes:**
- 200: OK
- 201: Created
- 400: Bad Request (validation)
- 401: Unauthorized
- 403: Forbidden (insufficient role)
- 409: Conflict (SKU duplicate)
- 422: Unprocessable (pipeline failed)
- 429: Rate limit exceeded

---

## 6. Components

### 6.1 Frontend Components (Next.js)

**Directory Structure:**
```
web/
├── app/
│   ├── (auth)/login/page.tsx
│   ├── (dashboard)/
│   │   ├── products/page.tsx
│   │   └── bk/page.tsx
│   └── layout.tsx
│
├── components/
│   ├── ui/           # Shadcn/UI
│   ├── products/     # Product-specific
│   └── layout/       # Header, Sidebar
│
├── hooks/
│   ├── use-products.ts
│   └── use-auth.ts
│
└── lib/
    └── api-client.ts
```

### 6.2 Backend Components (FastAPI)

**Directory Structure:**
```
api/
├── app/
│   ├── routers/         # API routes
│   │   ├── auth.py
│   │   └── products.py
│   │
│   ├── services/        # Business logic
│   │   └── product_service.py
│   │
│   ├── adapters/        # Core integration
│   │   └── core_adapter.py
│   │
│   ├── models/          # SQLAlchemy
│   │   └── product.py
│   │
│   └── middleware/
│       └── tenant.py
│
└── requirements.txt
```

**Core Adapter (mantém compatibilidade):**
```python
class CoreAdapter:
    def process_product(self, input_data: Dict) -> Dict:
        """Runs pipeline: generate → audit → refine"""
        # Import existing core modules
        from core.generator import generate_premium_content
        from core.auditor import audit_product

        # Same logic as CLI
        product = input_data.copy()
        generated = generate_premium_content(product)
        audit = audit_product(generated)

        return {
            **generated,
            'auditoria': audit,
            'quality_score': audit['score_total']
        }
```

---

## 7. Security

### 7.1 Authentication (JWT)

**Token Strategy:**
- **Access Token**: 1 hour (short-lived, stateless)
- **Refresh Token**: 30 days (stored in DB, revokable)

**JWT Payload:**
```json
{
  "sub": "user_id",
  "tenant_id": "...",
  "role": "editor",
  "exp": 1645808400
}
```

### 7.2 Authorization (RBAC)

**3 Roles:**

| Role | Permissions |
|------|-------------|
| **viewer** | List/view products, view BK |
| **editor** | Create/update products, upload BK, change status |
| **admin** | Delete products, create users, manage tenant |

**Implementation:**
```python
# app/dependencies/auth.py
def require_role(*allowed_roles: str):
    async def role_checker(current_user: User):
        if current_user.role not in allowed_roles:
            raise HTTPException(403, "Insufficient permissions")
        return current_user
    return role_checker

# Usage
@router.post("/products", dependencies=[Depends(require_role("editor", "admin"))])
```

### 7.3 Data Protection

**Encryption at Rest (Guidelines):**
```python
# Fernet symmetric encryption
from cryptography.fernet import Fernet

class EncryptionService:
    def encrypt(self, plaintext: str) -> str:
        return self.cipher.encrypt(plaintext.encode()).decode()
```

**Encryption in Transit:**
- HTTPS enforced (Railway auto-SSL)
- TLS 1.3
- HTTPS redirect middleware

### 7.4 Multi-Tenant Security (RLS)

**Row Level Security:**
```sql
-- PostgreSQL RLS
CREATE POLICY tenant_isolation_products ON products
    USING (tenant_id = current_setting('app.current_tenant_id')::uuid);
```

**Middleware:**
```python
class TenantMiddleware:
    async def dispatch(self, request, call_next):
        payload = verify_token(request.headers["Authorization"])
        tenant_id = payload["tenant_id"]

        # Set PostgreSQL session variable for RLS
        db.execute(f"SET app.current_tenant_id = '{tenant_id}'")
```

### 7.5 OWASP Top 10 Compliance

| Vulnerability | Mitigation |
|---------------|------------|
| Broken Access Control | RBAC + RLS policies |
| Cryptographic Failures | Bcrypt (cost 12) + Fernet + HTTPS |
| Injection | SQLAlchemy ORM + Pydantic validation |
| Authentication Failures | JWT short-lived + Password strength |

---

## 8. Deployment & Infrastructure

### 8.1 Deployment Topology (Railway)

**Servi?os planejados (Fase 1 MVP):**
- `api` (FastAPI) -> servi?o web Python
- `web` (Next.js 14) -> servi?o web Node
- `postgres` (Railway managed PostgreSQL)

**Opcional Fase 2+:**
- `redis` (cache + fila)
- `worker` (Celery/jobs ass?ncronos)

**Princ?pio de deploy:**
- CLI Python local continua independente (CR1)
- API/Web usam o mesmo core Python via adapter
- BK markdown permanece em filesystem (Fase 1)

### 8.2 Railway Project Structure

**Estrat?gia de servi?os no monorepo:**
- 1 projeto Railway com m?ltiplos servi?os
- cada servi?o aponta para subdiret?rio (`api/`, `web`)
- vari?veis compartilhadas no n?vel do projeto e sens?veis por servi?o quando necess?rio

**Arquivos de infraestrutura (target):**
- `railway.json` (config comum / build hints)
- `api/Dockerfile` (fallback se Nixpacks n?o atender)
- `web/Dockerfile` (fallback se necess?rio)

### 8.3 Environment Variables

**Project-level (Railway Variables):**
- `NODE_ENV=production`
- `APP_ENV=production`
- `DATABASE_URL`
- `JWT_SECRET_KEY`
- `FERNET_KEY`
- `CORS_ALLOWED_ORIGINS`
- `LOG_LEVEL=INFO`

**API service:**
- `PYTHONPATH=/app`
- `BK_BASE_PATH=/data/base_conhecimento`
- `ACCESS_TOKEN_EXPIRES_MINUTES=60`
- `REFRESH_TOKEN_EXPIRES_DAYS=30`

**Web service:**
- `NEXT_PUBLIC_API_BASE_URL`
- `NEXT_PUBLIC_APP_ENV`

**Regras:**
- segredos de produ??o nunca v?m de `.env` local
- separar vari?veis de preview e produ??o
- rotacionar `JWT_SECRET_KEY` e `FERNET_KEY` com procedimento controlado

### 8.4 Build and Start Commands

**API (FastAPI)**
- Build: `pip install -r requirements.txt`
- Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Web (Next.js 14)**
- Build: `npm ci && npm run build`
- Start: `npm run start -- --port $PORT`

**Monorepo simplificado:**
- Preferir `rootDirectory` por servi?o no Railway (`api`, `web`) para reduzir complexidade de build

### 8.5 Database Migrations (Alembic Workflow)

**Fluxo recomendado:**
1. Criar migration local (`alembic revision --autogenerate -m "..."`)
2. Revisar SQL gerado (RLS, ?ndices, constraints)
3. Aplicar local (`alembic upgrade head`)
4. Deploy API
5. Executar migration em Railway (release step/job)

**Regras operacionais:**
- Preferir migrations forward-only em produ??o
- Mudan?as destrutivas devem ser decompostas em m?ltiplas releases
- Backfills grandes migram para worker ass?ncrono (Fase 2+)

### 8.6 Domains, SSL and Networking

**Dom?nios (target):**
- `api.seudominio.com` -> API FastAPI
- `app.seudominio.com` -> Dashboard Next.js

**SSL/TLS:**
- TLS gerenciado pelo Railway
- HTTPS obrigat?rio
- redirect HTTP -> HTTPS no edge/app

**CORS:**
- permitir apenas dom?nios do dashboard (prod + preview)
- proibir `*` em produ??o

### 8.7 Health Checks and Readiness

**API**
- `GET /healthz` (liveness)
- `GET /readyz` (readiness: DB + BK path acess?vel)

**Web**
- rota leve (`/api/health` ou `/_health`)
- readiness ap?s boot completo do app

**Checklist de release (m?nimo):**
- API responde `200`
- conex?o Postgres OK
- smoke de cria??o de produto (payload m?nimo) em ambiente de teste

### 8.8 Preview Environments (PR)

**Estrat?gia:**
- preview deploy autom?tico por branch/PR
- banco de preview separado (ou schema isolado, se custo exigir)
- dataset seed reduzido + BK sample

**Seguran?a:**
- sem segredos de produ??o em preview
- webhooks externos desabilitados/mocados

### 8.9 Rollback Strategy

**Aplica??o:**
- rollback para deploy anterior no Railway
- validar `healthz/readyz` ap?s rollback

**Dados:**
- preferir migration corretiva a downgrade imediato
- snapshot/backup antes de migrations de risco

**Compatibilidade:**
- quebra de CR2 (contrato JSON da API) exige rollback imediato da API
- CLI permanece conting?ncia operacional (CR1)

### 8.10 BK Storage (Fase 1)

**Decis?o:**
- BK em markdown local/volume persistente
- path de BK configur?vel por env (`BK_BASE_PATH`)

**Opera??o:**
- manter BK ativa separada de quarentena (`_pendente`)
- registrar saneamentos em `base_conhecimento/_reports/`
- migrar para PostgreSQL FTS na Fase 2 quando volume/consulta exigir

---

## 9. Development Workflow

### 9.1 Git Branching Strategy

**Branch principal:**
- `main` (sempre deployavel)

**Branches de trabalho:**
- `feature/<story-id>-<slug>` para novas features (ex.: `feature/1.9-bk-domain-parser`)
- `fix/<slug>` para correcao de bug em producao/dev
- `chore/<slug>` para refactor, docs, tooling

**Regras:**
- branch curta e com escopo unico
- merge via Pull Request (sem push direto em `main`)
- preferir squash merge para manter historico legivel por story
- commits pequenos e reversiveis

**Mapeamento com stories:**
- 1 branch por story de `docs/stories/`
- PR referencia a story e atualiza checklist/file list antes do merge

### 9.2 Local Development Setup

**Objetivo:**
- rodar API + Web + Postgres localmente sem afetar o core CLI atual

**Modo A (recomendado - manual, Fase 1):**
- Terminal 1: backend FastAPI (`uvicorn ... --reload`)
- Terminal 2: frontend Next.js (`npm run dev`)
- Terminal 3: tarefas auxiliares (migrations, seeds, scripts)
- Postgres via Docker apenas para banco local

**Modo B (opcional):**
- `docker compose up` para subir Postgres (e Redis na Fase 2)

**Estrutura alvo (novo app fullstack):**
- `api/` -> FastAPI + SQLAlchemy + Alembic
- `web/` -> Next.js 14
- `packages/` -> libs compartilhadas (tipos, SDK)
- `tests/` -> suites cross-layer (quando aplicavel)

**Core legado:**
- pipeline Python atual continua executavel por `pipeline/run.py`
- adapter da API importa funcoes do core sem alterar contrato CLI (CR1/CR2)

### 9.3 Local Environment Configuration

**Arquivos `.env` locais (nao commitar):**
- `api/.env`
- `web/.env.local`

**Variaveis minimas (dev):**
- `DATABASE_URL=postgresql://postgres:postgres@localhost:5432/cadastro_produtos`
- `JWT_SECRET_KEY=<dev-only>`
- `FERNET_KEY=<dev-only>`
- `BK_BASE_PATH=../base_conhecimento`
- `CORS_ALLOWED_ORIGINS=http://localhost:3000`
- `NEXT_PUBLIC_API_BASE_URL=http://localhost:8000`

**Convencoes:**
- manter `.env.example` sem segredos reais
- valores locais devem simular producao (nomes iguais de env)
- separar config de `dev`, `test` e `production`

### 9.4 Run Commands (Dev Loop)

**Backend API (FastAPI):**
```bash
cd api
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend Web (Next.js):**
```bash
cd web
npm run dev
```

**CLI/Core (continuidade operacional):**
```bash
python pipeline/run.py --input examples-input.json --out out.json
```

**Hot reload esperado:**
- Next.js: HMR para UI
- FastAPI: `--reload` para API
- core Python: sem watcher obrigatorio; executar script/smoke conforme mudancas

### 9.5 Database Migrations and Seeding (Dev)

**Migrations (Alembic):**
1. Alterar models SQLAlchemy
2. Gerar migration: `alembic revision --autogenerate -m "..."`
3. Revisar migration (constraints, indices, defaults)
4. Aplicar: `alembic upgrade head`

**Seeding local (dados de teste):**
- comando alvo: `python -m app.seed.dev_seed`
- cria:
- tenant demo
- usuario admin/editor/viewer
- poucos produtos e jobs
- apontadores para BK sample

**Regras:**
- seed idempotente (pode rodar mais de uma vez)
- sem dados sensiveis reais
- dataset pequeno para boot rapido

### 9.6 Code Quality and Pre-Commit Hooks

**Padrao minimo por camada:**
- API Python: `ruff`, `black` (ou formatter equivalente), `pytest`
- Web/TS: `eslint`, `tsc --noEmit`, `vitest` (quando existir)

**Pre-commit (recomendado):**
- format/lint rapido em staged files
- bloquear commit com erro sintatico evidente
- checks pesados (test suite completa) ficam no CI

**Politica pragmatica:**
- hooks devem ser rapidos (<30s ideal)
- se hook virar gargalo, mover parte para CI e manter apenas checks essenciais

### 9.7 Pull Request Process and Review Rules

**Template de PR (obrigatorio):**
- contexto/problema
- escopo da mudanca
- story/issue vinculada
- evidencia de teste (comandos + resultado)
- risco/rollback
- screenshots (quando UI)

**Checklist de review:**
- contrato API/CLI preservado (CR1-CR4)
- mudanca cobre casos de erro e observabilidade minima
- migrations revisadas
- sem segredos ou arquivos temporarios commitados
- docs/story atualizados quando aplicavel

**Aprovacao recomendada:**
- 1 reviewer tecnico para mudancas pequenas
- 2 reviewers para auth, migrations destrutivas, contrato publico

### 9.8 CI/CD Pipeline (GitHub Actions)

**Triggers:**
- `pull_request` em `main`
- `push` em `main`

**Pipeline de PR (minimo):**
1. `lint` (web/api)
2. `typecheck` (web)
3. `tests` (api + core smoke)
4. `build` (web e api import check)

**Pipeline de merge em `main`:**
1. repetir checks
2. build artifacts/images
3. deploy para Railway (api/web)
4. smoke pos-deploy (`/healthz`, `/readyz`)

**Observacao de transicao (estado atual do repo):**
- o repo ainda e Python-first e nao possui `package.json` raiz para gates `npm run lint/typecheck/test`
- na Fase 1, CI deve rodar por subprojeto (`web/`, `api/`) sem quebrar o fluxo atual do core

### 9.9 Example GitHub Actions Workflow (Target)

```yaml
name: CI

on:
  pull_request:
  push:
    branches: [main]

jobs:
  api:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.14"
      - run: pip install -r api/requirements.txt
      - run: pytest -q

  web:
    runs-on: ubuntu-latest
    if: ${{ hashFiles('web/package.json') != '' }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"
          cache-dependency-path: web/package-lock.json
      - run: npm ci
        working-directory: web
      - run: npm run lint && npm run typecheck && npm test
        working-directory: web
```

### 9.10 Definition of Done (Workflow Layer)

**Para considerar a camada de workflow pronta (Fase 1):**
- existe padrao de branch/PR documentado
- API e Web sobem localmente com comando reproduzivel
- migrations e seed local documentados
- CI de PR roda checks minimos automaticamente
- processo de review inclui validacao de CR1-CR4

---

## 10. Testing Strategy

### 10.1 Testing Principles

**Objetivos da estrategia de testes:**
- proteger compatibilidade CLI/API (CR1-CR4)
- detectar regressao cedo no core e adapters
- manter feedback rapido em PR (piramide de testes)
- evitar dependencias externas em testes por padrao

**Principios operacionais:**
- testar comportamento/contrato antes de detalhes internos
- separar testes rapidos (PR) de suites lentas (nightly/release)
- fixtures deterministicas e dados pequenos
- cada bug relevante deve gerar teste de regressao

### 10.2 Test Pyramid by Layer

**Distribuicao alvo (Fase 1 -> Fase 2):**
- Unit tests (60-70%): funcoes puras, services, validators, serializers
- Integration tests (20-30%): API + DB + adapter/core mockado ou sample real
- Contract/smoke tests (5-10%): CLI/API JSON parity, health endpoints
- E2E UI (0-10% inicial; cresce na Wave 3+): fluxos criticos no dashboard

**Racional:**
- core atual e pipeline Python pedem alta cobertura unit/integration
- E2E entra depois para nao atrasar entrega da base API

### 10.3 Backend Unit Tests (Python / Pytest)

**Escopo principal (API + core adapter):**
- services de dominio (produto, jobs, auth)
- validacao Pydantic
- normalizadores/serializadores de resposta
- wrappers do core (tratamento de erro, timeout, contrato)
- utilitarios (slug, parsing, auditoria quando aplicavel)

**Ferramentas recomendadas:**
- `pytest`
- `pytest-cov`
- `pytest-mock`
- `freezegun` (se houver logica temporal relevante)

**Padroes:**
- nomear por comportamento (`test_create_product_rejects_missing_title`)
- evitar I/O real quando nao agrega valor
- usar factories/fixtures para entidades recorrentes

### 10.4 Frontend Unit and Component Tests (Vitest)

**Escopo inicial (Wave 2):**
- hooks customizados (fetch, filtros, polling)
- funcoes utilitarias (formatacao, mapeamento de status)
- componentes de apresentacao com regras criticas
- formularios (validacoes e estados de erro)

**Ferramentas recomendadas:**
- `vitest`
- `@testing-library/react`
- `@testing-library/user-event`
- `msw` (mock de API no frontend)

**Regras:**
- testar interacao e output visivel (nao detalhes de implementacao)
- snapshots apenas para componentes estaveis e pequenos

### 10.5 API Integration Tests (FastAPI)

**Objetivo:**
- validar endpoints reais com routing, validacao, auth e persistencia

**Cobertura minima por recurso (Fase 1):**
- `POST /products` (sucesso + validacao + authz)
- `GET /products/:id`
- `POST /generation-jobs`
- `GET /generation-jobs/:id`
- `GET /healthz` / `GET /readyz`

**Ferramentas:**
- `fastapi.testclient` ou `httpx.AsyncClient`
- banco de teste dedicado (Postgres local ou container)
- transacao rollback por teste quando possivel

**Testes de erro obrigatorios:**
- 401/403 (auth/rbac)
- 404 (recurso inexistente)
- 422 (payload invalido)
- 409 (conflito, quando aplicavel)
- 500 mapeado (falha controlada do core adapter)

### 10.6 Contract Tests (CLI x API Parity)

**Objetivo critico (CR2):**
- garantir que API retorne mesmo formato JSON da CLI para o pipeline de geracao

**Estrategia:**
- definir fixtures de input (`examples-input.json` e variantes)
- executar CLI e capturar output esperado
- chamar endpoint da API equivalente
- comparar:
- chaves obrigatorias
- tipos de campos
- semantica minima (ex.: `texto_final`, `scores`, `bk_context`)

**Observacao pragmatica:**
- campos volateis (timestamps, ids) devem ser normalizados antes da comparacao

### 10.7 Core/Pipeline Regression Tests

**Como proteger o core legado sem travar evolucao:**
- smoke tests de pipeline (`pipeline/run.py`) com sample fixture
- testes unitarios para modulos com bugs recentes:
- `core/extract_raw.py`
- `core/normalize_to_markdown.py`
- `core/bk_validator.py`
- validacao BK ativa em CI (modo sem `_pendente`, quando flag existir)

**Prioridade imediata (antes da Wave 1):**
- capturar regressao de OCR/filter parser por dominio
- capturar regressao de normalizacao (decimais `17.5`, tokens tecnicos)
- capturar regressao de validator (errors vs warnings)

### 10.8 Test Data, Fixtures and Factories

**Fixtures compartilhadas (target):**
- `tests/fixtures/products/*.json`
- `tests/fixtures/bk/*.md`
- `tests/fixtures/core/examples-input.json`

**Factories:**
- tenant, user, product, generation_job
- defaults validos + overrides simples

**Boas praticas:**
- fixtures pequenas e semanticamente nomeadas
- versionar samples reais anonimizados quando ajudarem cobertura
- evitar fixtures gigantes que mascaram causa de falha

### 10.9 Mocking Strategy

**O que mockar (unit tests):**
- chamadas externas (OpenAI / APIs terceiras)
- filesystem de BK quando teste nao e de I/O
- clock/uuid aleatorio
- adapters pesados do core

**O que preferir nao mockar (integration):**
- roteamento FastAPI
- validacao Pydantic
- queries SQLAlchemy (com banco de teste)

**Regra de ouro:**
- mockar na fronteira do sistema, nao no meio da regra de negocio

### 10.10 Coverage Targets and Quality Gates

**Metas iniciais (Fase 1 realistas):**
- core/pipeline tocado recentemente: >= 80%
- API services e endpoints criticos: >= 75%
- frontend (quando existir): >= 60% em unit/component tests

**Metas evolutivas (Fase 2+):**
- backend global >= 80%
- frontend global >= 75%

**Gates de PR (minimo):**
- testes unit/integration essenciais passando
- sem regressao em contract/smoke CLI/API
- cobertura nao cai em modulos alterados (delta coverage)

### 10.11 E2E Strategy (Playwright - Wave 3+)

**Quando entra:**
- apos dashboard ter fluxos estaveis (Wave 2/3)

**Fluxos E2E prioritarios:**
1. login -> criar produto -> iniciar geracao -> visualizar resultado
2. erro de validacao em formulario -> mensagem exibida
3. listagem com filtros basicos -> detalhe do produto

**Ambiente:**
- preview environment com DB seed
- mocks para integracoes externas custosas

### 10.12 Test Execution in CI (Parallelization)

**Pipeline recomendado (PR):**
1. lint/typecheck
2. unit tests Python
3. integration API tests
4. core smoke/contract tests
5. web tests (quando `web/` existir)

**Paralelizacao:**
- jobs separados por camada (`core`, `api`, `web`)
- fail-fast para economizar tempo em PR
- artifacts de relatorio/cobertura publicados para review

**Nightly (opcional Fase 2):**
- suite expandida
- testes mais lentos / cenarios extras

### 10.13 Definition of Done (Testing Layer)

**Para considerar a estrategia de testes pronta (Fase 1):**
- matriz de testes por camada documentada
- suite minima de backend + core executa em CI
- testes de contrato CLI/API definidos e automatizados
- fixtures/factories base disponiveis
- coverage targets e gates de PR definidos

---

## 11. Monitoring & Observability

### 11.1 Observability Goals

**Objetivos da camada de observabilidade:**
- detectar falhas rapidamente (MTTD baixo)
- facilitar diagnostico de erros no core/API/web
- acompanhar saude operacional e throughput de geracoes
- criar base para tuning de performance e capacidade (Secoes 12-13)

**Principio pratico:**
- logs primeiro, metricas depois, tracing/APM por fase

### 11.2 Structured Logging Standard

**Padrao de log (JSON):**
- formato estruturado em producao (JSON Lines)
- texto legivel em dev local (opcional)
- `request_id`/`correlation_id` em toda requisicao HTTP
- `job_id`, `product_id`, `tenant_id` quando aplicavel

**Campos minimos recomendados:**
- `timestamp`
- `level`
- `service` (`api`, `web`, `worker`)
- `env`
- `message`
- `request_id`
- `route` / `method` / `status_code` (API)
- `duration_ms`

**Niveis de log (guideline):**
- `DEBUG`: somente dev/troubleshooting local
- `INFO`: eventos operacionais normais
- `WARNING`: degradacao recuperavel / input suspeito
- `ERROR`: falha de operacao
- `CRITICAL`: indisponibilidade ou risco de dados

### 11.3 API Logging and Request Correlation

**Middleware de request logging (FastAPI):**
- gerar ou propagar `X-Request-Id`
- medir latencia por request
- logar inicio/fim com status e duracao
- anexar contexto de tenant/user (sem dados sensiveis)

**Eventos importantes para logar:**
- login/logout e falhas de auth (sem vazar segredo)
- criacao/atualizacao de produto
- inicio/fim de generation job
- falhas de integracao com core adapter
- falhas de acesso a BK (path, leitura, parse)

### 11.4 Core/Pipeline Observability (Python Legacy)

**Objetivo:**
- manter visibilidade do pipeline de 7 etapas sem reescrever o core

**Abordagem:**
- adicionar logs estruturados nos adapters e wrappers primeiro
- preservar logs simples do core quando ja existentes
- capturar tempos por etapa no adapter/API quando possivel

**Metricas de pipeline (minimo):**
- duracao total da geracao
- duracao por etapa (extract/normalize/validate/generate)
- score de auditoria final
- tamanho de BK consultada (itens/blocos)
- taxa de falha por etapa

### 11.5 Metrics (Application + Platform)

**Metricas de plataforma (Railway):**
- CPU
- RAM
- restart count
- request volume
- status de deploy

**Metricas de aplicacao (Fase 1 minimas):**
- requests por rota
- taxa de erro (4xx/5xx)
- latencia p50/p95/p99 por endpoint
- jobs de geracao: sucesso/falha/tempo medio
- tempo de `readyz`

**Implementacao sugerida:**
- logs estruturados + agregacao inicial
- metricas dedicadas/Prometheus na Fase 2+ se necessario

### 11.6 Error Tracking and Exception Handling

**Fase 1 (obrigatorio):**
- handler global de excecoes na API
- resposta padronizada de erro
- log estruturado com stack trace em `ERROR`
- mascaramento de segredos/PII em mensagens

**Fase 2+ (recomendado):**
- integrar Sentry (API e Web)
- tags: `env`, `service`, `tenant_id`, `release`
- release tracking para correlacionar regressao apos deploy

**Regras de seguranca:**
- nunca logar tokens JWT completos
- nunca logar payloads sensiveis integralmente
- truncar campos grandes e blobs

### 11.7 Health Checks, Readiness and Synthetic Checks

**Endpoints (ja definidos na Secao 8):**
- `GET /healthz` -> liveness
- `GET /readyz` -> readiness (DB + BK path)

**Expansao de readiness (Fase 1):**
- verificar conexao DB
- verificar acesso ao `BK_BASE_PATH`
- validar dependencias criticas minimas (ex.: config carregada)

**Checks sinteticos (recomendado):**
- ping externo periodico em `/healthz`
- smoke autenticado simples em ambiente de staging/preview

### 11.8 Alerting Rules (Initial)

**Alertas prioritarios (Fase 1):**
- API indisponivel (health check falhando)
- aumento de 5xx acima de limiar por janela (ex.: >5% em 5 min)
- latencia p95 elevada em endpoints criticos
- falha repetida em generation jobs
- falha de `readyz` por DB/BK inacessivel

**Canais:**
- email (minimo)
- Slack/Teams webhook (recomendado)

**Pratica operacional:**
- alertas acionaveis; evitar ruido de baixa severidade
- revisar limiares apos 2-4 semanas de dados reais

### 11.9 Dashboards and Operational Views

**Dashboard minimo (Fase 1):**
- requests/min e taxa de erro
- latencia por endpoint
- jobs de geracao (sucesso/falha/tempo)
- deploys recentes + correlacao com incidentes

**Fase 2+:**
- Grafana/observability stack dedicada
- dashboards por tenant (quando multi-tenancy estiver em uso real)

### 11.10 Auditability and Business Events

**Eventos de negocio para auditoria:**
- criacao/edicao de produto
- disparo de geracao
- aprovacao/edicao manual de conteudo
- movimentacao de BK ativa -> `_pendente` (quando feita via UI/ferramenta)

**Requisitos de trilha:**
- `who` (usuario/servico)
- `what` (acao)
- `when` (timestamp)
- `target` (resource id)
- `result` (success/failure)

**Observacao:**
- auditoria de negocio complementa logs tecnicos; nao substitui

### 11.11 Log Retention and Privacy

**Retencao inicial (guideline):**
- logs de aplicacao: 15-30 dias (ajustar por custo)
- eventos de auditoria: maior retencao (ex.: 90+ dias), conforme necessidade operacional
- backups/exports sob controle de acesso

**Privacidade:**
- minimizar PII em logs
- anonimizar quando possivel
- documentar politica de acesso aos logs por role (admin/devops)

### 11.12 Definition of Done (Observability Layer)

**Para considerar observabilidade pronta (Fase 1):**
- API com logs estruturados e `request_id`
- health/readiness operacionais e monitorados
- metricas minimas de erro/latencia acompanhadas
- alertas basicos configurados
- erros nao tratados viram logs acionaveis (e Sentry planejado para Fase 2)

---

## 12. Performance Optimization

### 12.1 Performance Goals and SLO Mindset

**Objetivos (Fase 1):**
- manter API responsiva para operacoes CRUD e disparo de geracao
- reduzir latencia percebida no dashboard
- evitar gargalos obvios em BK/filesystem e consultas SQL
- instrumentar antes de otimizar (medir -> ajustar -> validar)

**Metas iniciais (guideline, revisar com dados reais):**
- endpoints CRUD p95 < 500ms
- endpoint de criacao de job p95 < 800ms
- `healthz` p95 < 100ms
- `readyz` p95 < 300ms (sem checks pesados)

**Principio:**
- otimizar caminhos criticos de usuario primeiro, nao microbenchmarks isolados

### 12.2 Frontend Performance (Next.js 14)

**Prioridades (Wave 2):**
- Server Components por padrao quando possivel
- Client Components apenas onde houver interatividade real
- code splitting automatico + dynamic imports para modulos pesados
- lazy loading de tabelas/grids/editores secundarios

**Boas praticas:**
- evitar waterfalls de requests no carregamento inicial
- usar skeletons/spinners curtos com estados de empty/error
- memoizacao apenas onde profiling mostrar beneficio
- limitar re-renders em listas grandes (paginated/virtualized se necessario)

**Imagens e assets:**
- usar `next/image` para assets do dashboard
- comprimir imagens e usar tamanhos responsivos
- evitar carregar previews pesados sem necessidade

### 12.3 API Performance (FastAPI)

**Otimiza??es de baixo risco (Fase 1):**
- endpoints paginados por padrao em listagens
- selecionar apenas campos necessarios nas queries
- timeouts explicitos para chamadas ao core/externas
- reutilizacao de conexoes (pool do SQLAlchemy/driver)
- validacoes eficientes (evitar retrabalho em camadas duplicadas)

**Resposta e serializacao:**
- response models enxutos para listagem vs detalhe
- evitar payloads muito grandes (ex.: logs brutos, blobs)
- compressao HTTP (gzip/brotli) quando custo-beneficio for positivo

**Processamento de geracao:**
- endpoint de disparo deve ser rapido (cria job + retorna)
- processamento pesado migra para background tasks/worker (Fase 2)

### 12.4 Database Query Optimization

**Base (referencia Secao 4):**
- indices corretos em colunas de filtro/ordenacao
- constraints e tipos adequados para reduzir scans desnecessarios

**Praticas operacionais:**
- medir queries lentas (tempo + frequencia)
- revisar planos com `EXPLAIN ANALYZE` em casos criticos
- evitar N+1 em relacionamentos (eager loading seletivo)
- paginacao por cursor quando volume crescer e ordenacao for estavel

**Hot paths previstos:**
- listagem de produtos por tenant/status
- listagem de generation jobs por produto/status
- auditoria/eventos recentes no dashboard

### 12.5 Caching Strategy (Phased)

**Fase 1 (sem Redis obrigatorio):**
- cache de curta duracao em memoria para config/metadata estaticos
- ETags/headers HTTP para respostas idempotentes (quando aplicavel)
- cache no frontend (SWR/React Query) para leituras frequentes

**Fase 2 (Redis):**
- cache de queries frequentes
- rate limiting distribuido
- fila de jobs/background tasks

**Regra de consistencia:**
- preferir invalidacao simples por evento (create/update) a TTLs longos opacos

### 12.6 BK Access and Filesystem Optimization (Fase 1)

**Contexto atual:**
- BK permanece em markdown no filesystem (CR3)

**Otimiza??es praticas:**
- evitar varredura completa da BK por request se nao necessario
- carregar e indexar metadados em memoria no startup (ou cache com refresh)
- separar BK ativa de `_pendente` no caminho de leitura operacional
- normalizar leitura de arquivos com encoding/fallback consistente

**Evolucao planejada (Fase 2):**
- migrar busca textual pesada para PostgreSQL FTS
- manter markdown como fonte/artefato compat?vel enquanto necessario

### 12.7 Background Processing and Async Workloads

**Fase 1 (simples):**
- FastAPI `BackgroundTasks` para tarefas curtas e nao criticas
- jobs longos persistidos com polling de status

**Fase 2 (robusto):**
- Celery + Redis para processamento de geracao/exports/backfills
- retries com backoff
- dead-letter strategy (ou equivalente)

**Objetivo de performance:**
- desacoplar latencia HTTP do processamento pesado do pipeline

### 12.8 Pagination, Filtering and Payload Control

**Listagens (API):**
- pagina??o obrigatoria (`limit`, `offset` ou cursor)
- limite maximo por pagina (ex.: 100)
- ordenacao explicita e filtros indexados

**Dashboard (Web):**
- busca/filtro com debounce
- nao baixar colecoes completas para filtrar no cliente
- carregar detalhe sob demanda

**Payload budget (guideline):**
- respostas de listagem devem ser pequenas e previsiveis
- endpoints de detalhe podem expandir campos sob parametro (`include=`) se necessario

### 12.9 Performance Testing and Profiling Workflow

**Processo recomendado:**
1. medir baseline (logs/metricas)
2. identificar gargalo real (endpoint/query/render)
3. aplicar mudanca pequena
4. medir novamente
5. registrar impacto (PR/nota tecnica)

**Ferramentas por camada (exemplos):**
- API: logs de latencia, profiling Python pontual
- DB: `EXPLAIN ANALYZE`
- Web: Lighthouse, React Profiler, Web Vitals (Wave 2+)

**Anti-pattern:**
- otimizar sem baseline e sem reproduzir carga minima

### 12.10 CDN and Static Asset Delivery

**Fase 1:**
- usar CDN/edge padrao do host da camada web (Railway + provider de dominio)
- cache de assets estaticos com headers adequados

**Fase 2+:**
- CDN dedicada se houver volume de assets/usuarios maior
- estrategia de versionamento/hash para invalida??o segura

### 12.11 Definition of Done (Performance Layer)

**Para considerar performance planejada adequadamente (Fase 1):**
- metas iniciais de latencia documentadas
- paginacao e controle de payload definidos para listagens
- hot paths de DB e BK identificados com estrategia de mitigacao
- caminho para background processing definido (Fase 1 -> Fase 2)
- processo de profiling/medicao documentado

---

## 13. Scalability Plan

### 13.1 Scalability Principles

**Objetivo:**
- escalar por fases sem quebrar CR1-CR4 e sem overengineering precoce

**Principios:**
- escalar apenas gargalos medidos (CPU, latencia, fila, DB)
- separar escalabilidade de throughput (jobs) da escalabilidade de UX (API/web)
- priorizar simplicidade operacional na Fase 1
- preparar interfaces para evolucao (cache, fila, FTS) antes da necessidade plena

### 13.2 Capacity Assumptions (Initial)

**Cenarios de referencia (ajustar com dados reais):**
- Fase 1: ~100 produtos/dia, baixa concorrencia, uso interno/equipe pequena
- Fase 2: ~300-500 produtos/dia, multiplos usuarios simultaneos
- Fase 3: ~1000+ produtos/dia, picos por campanhas/importacoes

**Dimensoes que mais crescem:**
- volume de jobs de geracao
- tamanho da BK e custo de busca
- leituras de dashboard/listagens
- eventos de auditoria/logs

### 13.3 Horizontal Scaling (API/Web)

**API (FastAPI):**
- escalar replicas horizontalmente no Railway quando CPU/latencia justificar
- manter instancias stateless (sessao via JWT; sem estado em memoria critica)
- garantir idempotencia em endpoints sensiveis quando houver retry de cliente/proxy

**Web (Next.js):**
- escalar horizontalmente conforme trafego de dashboard
- aproveitar cache/CDN para assets e paginas adequadas

**Pre-requisitos para escalar API:**
- logs com `request_id`
- health/readiness confiaveis
- pool de conexoes configurado

### 13.4 Database Scaling Plan (PostgreSQL)

**Fase 1 (single instance managed):**
- tuning basico de indices e queries
- connection pooling adequado
- manutencao de schema/indexes por migrations

**Fase 2+:**
- read replicas para leituras pesadas (se workload justificar)
- separar workloads (ex.: analytics/auditoria) de queries operacionais criticas
- revisar particionamento para tabelas de eventos/jobs grandes (quando volume pedir)

**Riscos de escala de DB:**
- crescimento de logs/eventos sem politica de retencao
- queries de listagem sem pagina??o/filtros indexados
- locks por migrations destrutivas em horarios de pico

### 13.5 Caching Layer Evolution (Redis)

**Quando introduzir Redis (gatilhos):**
- latencia recorrente em leituras repetidas
- necessidade de rate limiting distribuido
- filas/background jobs confiaveis
- invalida??o cross-instance (multiplas replicas)

**Usos previstos:**
- cache de consultas frequentes
- cache de sessoes efemeras (se algum dia necessario)
- rate limiting counters
- broker/backend para Celery

**Cuidado:**
- cache nao corrige query ruim ou payload excessivo

### 13.6 Queue System and Workers (Celery + Redis)

**Motivacao:**
- desacoplar geracao pesada e tarefas longas do ciclo HTTP
- absorver picos sem degradar API de forma imediata

**Roadmap:**
- Fase 1: polling + execucao simples
- Fase 2: worker dedicado (Celery)
- Fase 3: filas separadas por prioridade (geracao, import, backfill)

**Controles de escala:**
- concorrencia por worker configuravel
- retries com backoff e limites
- monitoramento de backlog (queue depth)
- dead-letter / quarantine para jobs problematicos

### 13.7 BK Scalability (Filesystem -> Searchable Store)

**Estado atual (Fase 1):**
- BK markdown em filesystem, com BK ativa e `_pendente`

**Limites esperados:**
- busca em filesystem escala mal com aumento de arquivos/consultas
- concorrencia de leitura/escrita pode aumentar latencia
- observabilidade e auditoria ficam mais manuais

**Plano Fase 2:**
- indexar BK em PostgreSQL com FTS
- manter origem markdown para compatibilidade/operacao gradual
- criar rotina de sincronizacao/indexacao (idempotente)

**Plano Fase 3 (se necessario):**
- servi?o dedicado de busca/indexacao ou engine especifica

### 13.8 Multi-Tenancy Scalability

**Com crescimento de tenants:**
- reforcar isolamento via RLS + `tenant_id` em todas as queries
- indices compostos por `tenant_id` + campos de filtro comuns
- quotas/limites por tenant (jobs concorrentes, requests/min)

**Operacao:**
- dashboards/metricas por tenant
- alertas de abuso ou uso anomalo

### 13.9 Load Testing Strategy

**Objetivo:**
- validar capacidade antes de picos reais e antes de cada salto de fase

**Cenarios minimos (progressivos):**
1. CRUD e listagens com concorrencia baixa (baseline)
2. disparo de jobs simultaneos (pico moderado)
3. leitura de dashboard + polling de jobs + uso de BK
4. pico misto simulando 10x uso normal

**Metricas de saida:**
- throughput (req/s, jobs/min)
- latencia p50/p95/p99
- taxa de erro
- saturacao de CPU/RAM/DB

**Ferramentas (exemplos):**
- k6 ou Locust
- scripts de carga versionados em `tests/perf/` (target)

### 13.10 Scale Triggers and Decision Matrix

**Gatilhos para escalar API/Web:**
- p95 acima da meta por periodo sustentado
- CPU/RAM elevadas em horario normal
- fila/backlog crescente sem drenagem

**Gatilhos para escalar DB:**
- queries lentas recorrentes apos tuning
- saturacao de conexoes
- necessidade clara de separar leitura/escrita

**Gatilhos para migrar BK para FTS:**
- busca BK impactando latencia de geracao/API
- volume de arquivos/consultas impedindo SLA
- manutencao operacional ficando manual demais

### 13.11 Cost-Aware Scalability

**Principio:**
- escalar mantendo visibilidade de custo por ganho de capacidade

**Praticas:**
- revisar custo de replicas vs ganho de latencia
- priorizar otimizacoes de query/payload antes de subir infra
- classificar features de escala por ROI tecnico (cache, fila, FTS)

### 13.12 Definition of Done (Scalability Layer)

**Para considerar plano de escalabilidade pronto:**
- fases e gatilhos de escala documentados
- roadmap Redis/worker/FTS definido
- estrategia de load testing definida
- riscos de DB/BK/multi-tenancy mapeados
- criterios de decisao com foco em custo + performance

---

## 14. Migration Strategy

### 14.1 Migration Goals and Constraints

**Objetivo principal:**
- evoluir de CLI-only para arquitetura hibrida (CLI + API + Web) sem interromper a operacao atual

**Restricoes criticas (CR1-CR4):**
- CLI continua funcionando exatamente como antes
- API preserva contrato JSON equivalente a CLI
- BK markdown permanece compat?vel
- pipeline de 7 etapas permanece funcional

**Principio de migracao:**
- strangler pattern por camadas, com rollout incremental e rollback simples

### 14.2 Migration Phases Overview

**Sequencia recomendada:**
1. Fase 0 - Preparacao tecnica do core e qualidade minima
2. Wave 1 - API backend em producao (uso interno)
3. Wave 2 - Dashboard web (gestores)
4. Wave 3 - Operacao de BK via UI
5. Wave 4 - Multi-tenancy real
6. Wave 5 - Integracoes e-commerce/export

**Regra:**
- cada fase precisa criterio de entrada/saida e rollback documentado

### 14.3 Fase 0: Preparation (Before API)

**Objetivo:**
- reduzir risco antes de expor o core como servico

**Trabalho minimo recomendado:**
- adicionar `pytest` ao fluxo Python (core/pipeline)
- criar smoke tests automatizados de `pipeline/run.py`
- consolidar validacao BK no processo operacional (BK ativa limpa)
- estabilizar bugs conhecidos de extracao/normalizacao (ja atacados)
- isolar adapter boundaries para API chamar o core

**Entregaveis:**
- baseline de testes minima
- contrato de entrada/saida do pipeline documentado
- checklist de regressao manual (fallback CLI)

### 14.4 Wave 1: API Deployment (CLI Continues as Primary Fallback)

**Objetivo:**
- disponibilizar FastAPI para uso interno/integracao mantendo CLI como contingencia

**Escopo:**
- endpoints principais de produto/job
- endpoint de geracao chamando core adapter
- auth basica + RBAC
- PostgreSQL para entidades operacionais
- logs/health/readiness

**Rollout:**
- liberar inicialmente para equipe interna
- comparar outputs API vs CLI (contract tests)
- monitorar erros/latencia antes de ampliar uso

**Crit?rio de saida:**
- API estavel em uso interno com rollback validado
- zero regressao em CR1/CR2 observada nas suites/smokes

### 14.5 Wave 2: Frontend Dashboard Deployment

**Objetivo:**
- permitir operacao por gestores sem terminal

**Escopo:**
- login
- listagem/edicao de produtos
- disparo e acompanhamento de jobs
- visualizacao de resultados

**Estrategia de adocao:**
- rollout progressivo por perfil/equipe
- manter CLI e API acessiveis para suporte e troubleshooting

**Riscos:**
- UX gerar carga extra em endpoints nao otimizados
- gaps de permissao/RBAC na interface

### 14.6 Wave 3: BK UI and Content Operations

**Objetivo:**
- trazer operacoes de base de conhecimento para fluxo mais controlado

**Escopo incremental:**
- upload/registro de fontes BK
- visualizacao de itens BK ativos vs `_pendente`
- saneamento/quarentena via UI com trilha de auditoria
- relatorios de qualidade (errors/warnings do validator)

**Cuidados de migracao:**
- BK markdown continua como fonte de verdade no inicio
- UI nao deve quebrar compatibilidade com estrutura atual da BK (CR3)

### 14.7 Wave 4: Multi-Tenancy Rollout

**Objetivo:**
- suportar multiplos clientes/tenants com isolamento real

**Passos:**
- consolidar `tenant_id` em entidades e fluxos
- ativar/validar RLS em producao
- quotas e observabilidade por tenant
- onboarding controlado de tenants piloto

**Risco principal:**
- vazamento cross-tenant por query sem filtro/RLS mal aplicado

**Mitigacao:**
- testes de seguranca + contract/integration por tenant
- rollout com poucos tenants antes de escala comercial

### 14.8 Wave 5: E-commerce Integrations and Export

**Objetivo:**
- integrar outputs ao fluxo comercial (ex.: Shopify export)

**Escopo:**
- export estruturado de produtos/conteudos
- mapeamentos de campo por plataforma
- jobs de sincronizacao com retry
- auditoria de exportacoes

**Estrategia:**
- iniciar por export manual/semiautomatico
- evoluir para sincronizacao automatizada apos confiabilidade

### 14.9 Data Migration Plan (When Applicable)

**Cenario atual:**
- core CLI trabalha com arquivos e outputs locais
- nova camada API/Web introduz banco relacional para estado operacional

**Migracoes de dados previstas:**
- sem migracao massiva inicial obrigatoria (brownfield leve)
- seeds de dados operacionais (usuarios/roles/tenant demo)
- importacao gradual de produtos historicos se houver necessidade de consulta UI

**BK migration (futura):**
- indexacao em PostgreSQL FTS (sem abandonar markdown de imediato)
- sincronizacao incremental e reversivel

### 14.10 Rollback Strategy by Wave

**Regra geral:**
- rollback de app antes de rollback de dados sempre que possivel
- manter CLI como plano de contingencia operacional ate maturidade da plataforma

**Por wave (resumo):**
- Wave 1: rollback API para versao anterior; CLI assume operacao
- Wave 2: desabilitar dashboard/feature flags; API/CLI seguem ativos
- Wave 3: desabilitar acoes de BK UI; operar BK manualmente
- Wave 4: suspender onboarding de novos tenants; manter tenants piloto
- Wave 5: desligar integracao/export automatico e usar export manual

**Dados/migrations:**
- preferir migrations forward-only + corretivas
- snapshot/backup antes de mudancas de risco

### 14.11 Feature Flags and Progressive Delivery

**Uso recomendado:**
- esconder funcionalidades incompletas por role/env
- liberar waves para grupos piloto
- desligar rapidamente features problem?ticas sem redeploy completo (quando suportado)

**Flags candidatas:**
- `enable_dashboard`
- `enable_bk_ui`
- `enable_multi_tenancy`
- `enable_shopify_export`

### 14.12 Migration Governance and Communication

**Governanca tecnica:**
- PRD (produto) e arquitetura (tecnica) sincronizados por wave
- checklist de go/no-go por release importante
- post-mortem para incidentes de migracao relevantes

**Comunicacao operacional:**
- avisos de janela de deploy/migracao
- plano de suporte durante rollout
- registro de mudancas e rollback executado (se ocorrer)

### 14.13 Definition of Done (Migration Layer)

**Para considerar a estrategia de migracao pronta:**
- fases/waves documentadas com escopo e riscos
- criterios de entrada/saida por wave definidos
- rollback por wave definido com contingencia CLI
- plano de dados/BK descrito (incluindo migracao gradual)
- uso de feature flags/progressive rollout previsto

---

## 15. Appendices

### 15.1 Glossary

**Termos do projeto:**
- **BK (Base de Conhecimento):** conjunto de markdowns usados como referencia contextual para geracao
- **BK ativa:** subconjunto operacional da BK sem erros/warnings do validator
- **`_pendente`:** quarentena para arquivos BK com ruido/baixa qualidade ou duplicatas
- **Core Engine:** pipeline Python legado de 7 etapas (mantido por compatibilidade)
- **Core Adapter:** camada que expoe o core para API sem alterar contrato original
- **Generation Job:** execucao assincrona/supervisionada de geracao de conteudo
- **CR1-CR4:** requisitos de compatibilidade critica (CLI/API/BK/pipeline)
- **RLS:** Row Level Security no PostgreSQL para isolamento multi-tenant
- **Wave:** bloco de entrega incremental da migracao (produto + arquitetura)

### 15.2 Key Decisions Summary (Reference)

**Decisoes arquiteturais consolidadas:**
1. Arquitetura hibrida (`CLI + API + Web`) para preservar legado e ampliar acesso
2. Core Python permanece inalterado, encapsulado por adapter
3. FastAPI + Next.js 14 + PostgreSQL como stack da camada nova
4. Deploy inicial em Railway com evolucao gradual de infra
5. BK permanece em markdown (Fase 1), com migracao de busca para FTS depois
6. Seguranca com JWT + RBAC + RLS desde as primeiras waves

### 15.3 Reference Documents (Internal)

**Produto e planejamento:**
- `docs/prd.md`
- `docs/prd-executive-summary.md`
- `docs/roadmap-proximos-passos.md`
- `docs/stories/`

**Arquitetura e operacao:**
- `docs/architecture-progress.md` (documento de trabalho completo)
- `docs/next-steps-architecture.md` (retomada / historico de progresso)
- `docs/bk-operacao-quarentena.md` (operacao BK ativa vs `_pendente`)

**Core/pipeline relevantes:**
- `pipeline/run.py`
- `pipeline/bk_validate.py`
- `core/extract_raw.py`
- `core/normalize_to_markdown.py`
- `core/bk_validator.py`

### 15.4 External Documentation (Primary References)

**Frameworks e plataforma (consultar versoes adotadas na Secao 3):**
- FastAPI documentation
- Next.js documentation (App Router / Server Components)
- Railway documentation (deploy, env vars, health checks)
- PostgreSQL documentation (RLS, indexing, FTS)
- SQLAlchemy + Alembic documentation
- Playwright documentation (Wave 3+ E2E)
- Celery + Redis documentation (Fase 2 workers)

**Nota:**
- preferir documentacao oficial para decisoes de implementacao e tuning

### 15.5 Suggested ADR Backlog (Optional)

**ADRs recomendados para registrar (quando a implementacao iniciar):**
- ADR-001: Core Adapter boundary and CLI/API parity contract
- ADR-002: BK storage strategy (markdown-first with future FTS index)
- ADR-003: Job execution model (sync endpoint + async worker roadmap)
- ADR-004: Multi-tenancy isolation model (RLS + JWT tenant_id)
- ADR-005: Deployment strategy on Railway (services, migrations, rollback)

**Formato minimo de ADR:**
- Contexto
- Decisao
- Consequencias
- Alternativas consideradas
- Data / status

### 15.6 Additional Diagrams (Optional Backlog)

**Diagramas uteis para fase de implementacao:**
- C4 Context (usuarios/sistemas externos)
- C4 Container (web/api/db/core adapter)
- Sequence diagram: `POST /generation-jobs` -> core adapter -> persistencia -> polling
- Sequence diagram: fluxo BK UI -> validator -> quarentena `_pendente`
- Deployment diagram (Railway services + domains + DB)

### 15.7 Assumptions and Open Questions

**Assumptions (registradas nesta arquitetura):**
- uso inicial e predominantemente interno nas primeiras waves
- Railway atende custo/performance da Fase 1
- BK markdown continua suficiente ate volume justificar FTS
- CLI seguira como fallback operacional durante migracao

**Open questions para kickoff de implementacao:**
- qual escopo exato de endpoints da Wave 1 entra no MVP tecnico?
- jobs de geracao na Wave 1 serao sincronos, polling simples ou ja com background task?
- quais perfis de gestor precisam acesso na Wave 2 (viewer/editor/admin)?
- existe necessidade de importacao de historico de produtos logo na Wave 1/2?

### 15.8 Handoff Checklist (Architecture -> Delivery)

**Antes do kickoff da Wave 1:**
- aprovar arquitetura (PRD + arquitetura alinhados)
- confirmar escopo tecnico da Wave 1 (endpoints, auth, jobs)
- definir estrutura inicial de repos/subpastas (`api/`, `web/`, migrations)
- criar backlog tecnico inicial (stories/tasks por wave)
- configurar CI minima e ambiente dev base

### 15.9 Completion Note and Final Deliverable

**Status desta arquitetura:**
- 15/15 secoes documentadas no `docs/architecture-progress.md`
- pronta para consolidacao em `docs/architecture.md`

**Proximo passo recomendado (operacional):**
1. consolidar/copy-edit para `docs/architecture.md`
2. revisao final com @architect + @dev + @po
3. aprovar kickoff da Wave 1

### 15.10 Definition of Done (Appendices Layer)

**Para considerar apendices prontos:**
- glossario basico definido
- referencias internas/externas listadas
- backlog de ADRs sugerido
- checklist de handoff registrado
- nota de conclusao e proximo passo final documentados

---

## 📊 Status Final

**Secoes completadas:** 1-15 (100%)
**Proximo:** Consolidar em `docs/architecture.md`

**Proximo passo operacional:** Revisao final e consolidacao

---

**Ultima atualizacao:** 2026-02-26
**Arquiteto:** Aria (@architect)

— Arquitetura em progresso 🏗️
