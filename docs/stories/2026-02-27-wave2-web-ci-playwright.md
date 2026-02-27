# Story - Wave 2 Web CI (Playwright)

**Data:** 2026-02-27  
**Status:** Done

## Escopo

- Adicionar pipeline CI dedicada para frontend
- Executar gates `lint`, `typecheck` e `npm test` (Playwright smoke)
- Acionar workflow apenas quando houver mudanca no `web/`

## Checklist

- [x] Workflow `web-ci.yml` criada
- [x] Trigger por `push` e `pull_request` com filtro de paths
- [x] `npm ci` configurado com cache de lockfile
- [x] Instalacao de browser Playwright no runner
- [x] Etapas `lint`, `typecheck` e `npm test` adicionadas

## File List

- `.github/workflows/web-ci.yml`

## DoD

- [x] Frontend passa a ter quality gates automatizados em CI
- [x] Smoke E2E inicial executado automaticamente no PR
- [x] Story documentada com checklist e file list
