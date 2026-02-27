# Story - Wave 2 Tabs (Context Preservation)

**Data:** 2026-02-27  
**Status:** Done

## Escopo

- Preservar contexto de filtros de `/produtos` ao navegar entre tabs
- Reutilizar ultima visao de produtos ao retornar de `Jobs`/`Gerar`/`Health`
- Validar comportamento em smoke E2E

## Checklist

- [x] `Wave2Dashboard` ajustado para lembrar `lastView` de `/produtos`
- [x] Tab `Produtos` passa a usar href da ultima visao conhecida
- [x] Teste smoke de navegacao com preservacao de query adicionado
- [x] `npm run lint` executado
- [x] `npm run typecheck` executado
- [x] `npm test` executado com sucesso

## Evidencias

- `cd web && npm run lint`
- `cd web && npm run typecheck`
- `cd web && npm test`

## File List

- `web/components/wave2-dashboard.tsx`
- `web/tests/e2e/smoke.spec.ts`

## DoD

- [x] Navegacao por tabs preserva contexto operacional de produtos
- [x] Cobertura smoke garante nao regressao do comportamento
- [x] Story documentada com checklist e file list
