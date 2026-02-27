# Story - Wave 2 Smoke (API Error Paths)

**Data:** 2026-02-27  
**Status:** Done

## Escopo

- Cobrir cenarios de erro de API na suite smoke E2E
- Validar feedback operacional de erro em `Produtos` e `Gerar`

## Checklist

- [x] Teste de erro `GET /api/products` adicionado
- [x] Teste de erro `POST /api/products` adicionado
- [x] `npm run lint` executado
- [x] `npm run typecheck` executado
- [x] `npm test` executado com sucesso

## Evidencias

- `cd web && npm run lint`
- `cd web && npm run typecheck`
- `cd web && npm test`

## File List

- `web/tests/e2e/smoke.spec.ts`

## DoD

- [x] Fluxos criticos possuem cobertura basica de erro de API
- [x] Mensagens de erro operacionais validadas automaticamente
- [x] Story documentada com checklist e file list
