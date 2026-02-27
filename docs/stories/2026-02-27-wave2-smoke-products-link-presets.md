# Story - Wave 2 Smoke (Produtos Link Presets)

**Data:** 2026-02-27  
**Status:** Done

## Escopo

- Cobrir presets operacionais de links em `/produtos`
- Validar aplicacao de filtros esperados para:
  - `Revisao editorial`
  - `Aprovados`
  - `Score alto`
- Corrigir comportamento do preset para atualizar estado local antes da sincronizacao de URL

## Checklist

- [x] Smoke test para presets de link adicionado
- [x] Preset atualizado para aplicar filtros via estado local
- [x] `npm run lint` executado
- [x] `npm run typecheck` executado
- [x] `npm test` executado com sucesso

## Evidencias

- `cd web && npm run lint`
- `cd web && npm run typecheck`
- `cd web && npm test`

## File List

- `web/components/products-list-panel.tsx`
- `web/tests/e2e/smoke.spec.ts`

## DoD

- [x] Presets operacionais cobertos por smoke automatizado
- [x] Comportamento de filtros consistente apos clique nos presets
- [x] Story documentada com checklist e file list
