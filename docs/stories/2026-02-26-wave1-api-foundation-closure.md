# Story - Wave 1 API Foundation Closure

**Data:** 2026-02-26  
**Status:** Done

## Escopo

- Story 1.1 Estrutura API
- Story 1.2 Schemas Pydantic
- Story 1.3 `POST /api/v1/products`
- Story 1.4 `generation-jobs`
- Story 1.5 DB + Alembic + models
- Story 1.6 Persistencia + listagem + detalhe

## Checklist

- [x] Endpoints de health/readiness ativos (`/healthz`, `/readyz`, alias `/health`)
- [x] Schemas de input/output alinhados ao pipeline
- [x] Endpoint de create de produto integrado ao core
- [x] Jobs batch assíncronos com status e resultados
- [x] Migration inicial aplicada e tabelas base criadas
- [x] Persistencia de produtos e listagem/detalhe paginados
- [x] Testes de integração API (DB e stateless) verdes
- [x] CI mínima de API criada (`.github/workflows/api-ci.yml`)

## Evidencias

- `python -m alembic -c alembic.ini upgrade head`
- `python -m pytest -q api/tests/test_api_integration.py`
- `python -m compileall api`

## File List (principal)

- `api/app/main.py`
- `api/app/api/routes/health.py`
- `api/app/api/routes/products.py`
- `api/app/api/routes/generation_jobs.py`
- `api/app/schemas/product.py`
- `api/app/schemas/generation_job.py`
- `api/app/services/pipeline_service.py`
- `api/app/services/product_persistence_service.py`
- `api/app/services/generation_job_service.py`
- `api/alembic/versions/0001_wave1_initial.py`
- `api/tests/test_api_integration.py`
- `.github/workflows/api-ci.yml`

## DoD

- [x] Implementacao completa das stories 1.1-1.6
- [x] Validacao local com PostgreSQL real
- [x] Testes automatizados de integração passando
- [x] Contrato canônico `generation-jobs` aplicado (aliases temporários mantidos)
- [x] Compatibilidade CR1-CR4 preservada
