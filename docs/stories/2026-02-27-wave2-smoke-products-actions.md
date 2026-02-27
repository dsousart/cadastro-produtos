# Story - Wave 2 Smoke (Produtos Actions)

**Data:** 2026-02-27  
**Status:** Done

## Escopo

- Cobrir acoes operacionais de `/produtos` na suite smoke E2E
- Validar `Resetar visao` e `Copiar link da visao`

## Checklist

- [x] Teste smoke para `Resetar visao` adicionado
- [x] Teste smoke para `Copiar link da visao` adicionado
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

- [x] Acoes principais da tela de produtos cobertas em smoke
- [x] Deep-linking e reset operacional validados automaticamente
- [x] Story documentada com checklist e file list
