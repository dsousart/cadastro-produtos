# Story - Wave 2 Smoke (Jobs Failure Paths)

**Data:** 2026-02-27  
**Status:** Done

## Escopo

- Cobrir falhas de polling de `generation-jobs` na suite smoke E2E
- Validar feedback operacional para erro HTTP e erro de rede

## Checklist

- [x] Teste de erro 500 no polling de job adicionado
- [x] Teste de falha de rede no polling de job adicionado
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

- [x] Fluxo de jobs cobre caminhos de falha essenciais
- [x] Mensagens de erro operacionais validadas automaticamente
- [x] Story documentada com checklist e file list
