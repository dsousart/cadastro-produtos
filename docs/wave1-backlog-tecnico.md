# Wave 1 - Backlog Tecnico (API + Core Integration)

**Data:** 2026-02-26
**Base:** `docs/prd.md` (Stories 1.1-1.6) + `docs/architecture.md` + `docs/adrs/ADR-000-prd-arquitetura-alinhamento-wave1.md`
**Status:** Fechado tecnicamente (stories formalizadas + evidencias consolidadas)

---

## Status de Execucao (2026-02-26)

**Implementacao (codigo)**
- [x] `1.1` Estrutura API (FastAPI + health/readiness + alias `/health`)
- [x] `1.2` Schemas Pydantic (`ProductInput` / `ProductOutput`)
- [x] `1.3` `POST /api/v1/products` com integracao ao pipeline
- [x] `1.4` `generation-jobs` + status + aliases temporarios (`batch/batches`)
- [x] `1.5` SQLAlchemy + Alembic + migration inicial
- [x] `1.6` Persistencia + listagem paginada + detalhe

**Smoke local (com PostgreSQL real)**
- [x] PostgreSQL 18 rodando local (`postgresql-x64-18`)
- [x] Banco `cadastro_produtos` criado
- [x] `alembic upgrade head` executado
- [x] `POST /api/v1/products` retorna `201` e persiste (`db_persisted=true`)
- [x] `GET /api/v1/products` retorna lista paginada
- [x] `GET /api/v1/products/{id}` retorna detalhe
- [x] `POST /api/v1/generation-jobs` retorna `202`
- [x] `GET /api/v1/generation-jobs/{id}` retorna `completed`
- [x] `results` do job persistido e retornado (bug corrigido em JSON payload)

**Testes automatizados (API integration)**
- [x] `pytest` configurado em `api/requirements-dev.txt`
- [x] Suite minima em `api/tests/test_api_integration.py`
- [x] Fluxo sem DB (health + create stateless + erros `503`) validado
- [x] Fluxo com DB real (create/list/detail + `generation-jobs`) validado

**Evidencias registradas**
- [x] `python -m alembic -c alembic.ini upgrade head` (DB local)
- [x] `python -m pytest -q api\\tests\\test_api_integration.py` -> `4 passed`
- [x] Smoke com `TestClient` cobrindo persistencia e `generation-jobs`

**Pendencias para fechamento formal**
- [x] Atualizar stories/checklists oficiais (story de fechamento criada em `docs/stories/2026-02-26-wave1-api-foundation-closure.md`)
- [x] Preparar pacote de evidencias para PR (`docs/sprint-1-execution-report.md`)
- [x] Adicionar CI minima da API (pytest) no GitHub Actions (`.github/workflows/api-ci.yml`)

---

## Objetivo da Wave 1

Entregar a base da API (FastAPI + integracao com core Python + persistencia inicial) mantendo compatibilidade com:

- `CR1` CLI intacto
- `CR2` paridade de formato JSON CLI/API
- `CR3` BK markdown compativel
- `CR4` Python 3.14+

---

## Escopo (Stories 1.1 -> 1.6)

- `1.1` Estrutura do Projeto API
- `1.2` Schemas Pydantic
- `1.3` `POST /api/v1/products`
- `1.4` `POST /api/v1/generation-jobs` + status (`BackgroundTasks`)
- `1.5` PostgreSQL + Alembic + models
- `1.6` Persistencia + listagem paginada + detalhe

---

## Decisoes de Alinhamento (ADR-000)

- Health endpoints canônicos: `GET /healthz` + `GET /readyz`
- `/health` pode existir como alias temporario
- Naming canonico de jobs: `generation-jobs`
- Aliases `batch/batches` opcionais e temporarios
- Auth/RBAC **fora da Wave 1** (Wave 4); no maximo protecao minima por ambiente interno

---

## Sequencia Recomendada (Execucao)

1. Fase 0 tecnica minima (testes/smoke do core)
2. Story `1.1` (estrutura API)
3. Story `1.2` (schemas)
4. Story `1.5` (DB + Alembic + models)
5. Story `1.3` (create product)
6. Story `1.4` (generation-jobs batch/background)
7. Story `1.6` (persistencia + listagem + detalhe)
8. Contract tests CLI/API + smoke de release local

---

## Backlog por Story

### Story 1.1 - Estrutura do Projeto API

**Entregaveis tecnicos**
- criar pasta `api/`
- criar app FastAPI inicial (`app/main.py`)
- rotas base de health (`/healthz`, `/readyz`)
- alias opcional `/health`
- `api/requirements.txt`
- `api/.env.example`
- `api/README.md` (setup rapido)

**Tarefas**
- definir layout base (`app/api`, `app/core`, `app/schemas`, `app/services`, `app/models`)
- criar `create_app()` + bootstrap de config
- implementar `GET /healthz`
- implementar `GET /readyz` com checks minimos (config carregada; DB pode retornar degraded se nao configurado)
- adicionar `uvicorn` entrypoint

**Critico validar**
- `uvicorn ... --reload` sobe local
- core Python ainda roda (`python pipeline/run.py ...`)

### Story 1.2 - Schemas Pydantic

**Entregaveis tecnicos**
- `ProductInput`
- `ProductOutput`
- schemas auxiliares (`Audit`, `Scores`, `BKContext`, metadata)

**Tarefas**
- mapear formato atual de `pipeline/run.py` / JSON de saida
- modelar tipos com foco em paridade de contrato (`CR2`)
- criar validacoes minimas (campos obrigatorios)
- adicionar exemplos no OpenAPI

**Critico validar**
- payload invalido retorna 422
- schemas aceitam `examples-*.json`

### Story 1.5 - Database Setup (adiantada antes de 1.3/1.6)

**Entregaveis tecnicos**
- SQLAlchemy base/session
- Alembic configurado
- migration inicial
- models: `tenants`, `users`, `products`, `generation_jobs`

**Tarefas**
- definir `DATABASE_URL`
- bootstrap de session/pool
- criar models e enums de status basicos
- gerar migration inicial
- aplicar migration local

**Critico validar**
- API sobe com DB vazio
- core nao depende de DB

### Story 1.3 - `POST /api/v1/products`

**Entregaveis tecnicos**
- endpoint `POST /api/v1/products`
- service de integracao com core adapter
- mapeamento de erros (422/500)

**Tarefas**
- criar adapter/wrapper para chamar pipeline
- normalizar resposta para `ProductOutput`
- incluir `audit_id` e `timestamp`
- opcao de persistencia desacoplada (reutilizavel pela story 1.6)

**Critico validar**
- resultado API compatível com CLI (amostra controlada)
- erro do pipeline nao derruba app

### Story 1.4 - `generation-jobs` (batch/background)

**Entregaveis tecnicos**
- `POST /api/v1/generation-jobs`
- `GET /api/v1/generation-jobs/{id}`
- processamento via `BackgroundTasks`

**Tarefas**
- definir payload batch (array + limite 20)
- criar model/status de job (`pending`, `running`, `completed`, `failed`)
- persistir progresso/resultado agregado
- implementar leitura de status e resultados
- aliases temporarios opcionais:
- `POST /api/v1/products/batch`
- `GET /api/v1/batches/{id}`

**Critico validar**
- >20 retorna 400
- falha parcial nao impede demais itens
- endpoint responde rapido (202)

### Story 1.6 - Persistencia de Resultados

**Entregaveis tecnicos**
- persistencia do create product
- `GET /api/v1/products` paginado
- `GET /api/v1/products/{id}`
- filtros iniciais (`status`, `min_score`)

**Tarefas**
- mapear campos persistidos (input, output, score, status, timestamps)
- paginacao com metadata (`page/limit/total` ou `offset/limit/total`)
- filtros indexaveis
- serializacao listagem vs detalhe

**Critico validar**
- listar com banco vazio
- mesmo input pode gerar multiplos registros sem conflito indevido

---

## Fase 0 Tecnica Minima (antes de codar API)

**Objetivo**
- reduzir risco de regressao do core antes da integracao via API

**Tarefas minimas**
- instalar/adicionar `pytest` no fluxo Python
- smoke test automatizado de `pipeline/run.py`
- 2-3 testes unitarios de regressao:
- `core/extract_raw.py` (parser por dominio / filtro OCR)
- `core/normalize_to_markdown.py` (decimais `17.5`)
- `core/bk_validator.py` (errors vs warnings)

**Saida esperada**
- baseline testavel para proteger `CR1/CR2`

---

## Dependencias e Ordem de Bloqueio

- `1.1` bloqueia `1.2`, `1.3`, `1.4`, `1.5`, `1.6`
- `1.2` bloqueia `1.3` e influencia `1.6`
- `1.5` bloqueia persistencia real de `1.4` e `1.6`
- `1.3` desbloqueia contract tests CLI/API
- `1.4` depende de `1.3` (reuso de service core)
- `1.6` depende de `1.5` e integra com `1.3`

---

## Definicao de Pronto (Kickoff Wave 1)

- `docs/architecture.md` consolidado e aprovado
- `docs/prd.md` alinhado com ADR-000
- ADR-000 marcado como aceito
- naming canonico `generation-jobs` acordado
- health endpoint padrao (`/healthz`, `/readyz`) acordado
- escopo Wave 1 congelado em stories `1.1`-`1.6`

---

## Definicao de Concluido (Wave 1 tecnico)

- stories `1.1`-`1.6` implementadas e validadas
- smoke CLI continua OK (`CR1`)
- teste comparativo CLI/API (contrato) executado (`CR2`)
- BK markdown inalterado/compatível (`CR3`)
- ambiente Python 3.14+ suportado (`CR4`)
- docs de setup API atualizados

---

## Checklist de Kickoff (1a sprint)

1. Criar branch `feature/wave1-api-foundation`
2. Implementar `1.1` + `1.2`
3. Subir Postgres local + Alembic (`1.5`)
4. Implementar `POST /api/v1/products` (`1.3`)
5. Validar paridade CLI/API (smoke)
6. Implementar `generation-jobs` (`1.4`)
7. Implementar listagem/detalhe/persistencia (`1.6`)
8. Rodar smoke final + revisar PR contra `ADR-000`
