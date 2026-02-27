# Story - Wave 2 Smoke (Navigation + Query State)

**Data:** 2026-02-27  
**Status:** Done

## Escopo

- Expandir smoke E2E para cobrir rota `health`
- Validar hidratacao inicial de filtros via query params em `/produtos`

## Checklist

- [x] Teste smoke para `/health` adicionado
- [x] Teste smoke para estado inicial de query params em `/produtos` adicionado
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

- [x] Navegacao essencial da Wave 2 coberta em smoke
- [x] Deep-linking operacional de `/produtos` validado automaticamente
- [x] Story documentada com checklist e arquivos alterados
