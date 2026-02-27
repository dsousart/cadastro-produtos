# Story - Wave 2 Produtos (Query Parsing Fix)

**Data:** 2026-02-27  
**Status:** Done

## Escopo

- Ajustar parse de query params em `/produtos`
- Evitar defaults forzados no server para `limit`/`offset` quando ausentes
- Preservar comportamento de preferencia local no cliente quando nao ha query explicita

## Checklist

- [x] Parse numerico de `limit`/`offset` convertido para opcional
- [x] `initialProductQuery` deixa campos indefinidos quando query nao existe
- [x] `npm run lint` executado
- [x] `npm run typecheck` executado
- [x] `npm test` executado com sucesso

## Evidencias

- `cd web && npm run lint`
- `cd web && npm run typecheck`
- `cd web && npm test`

## File List

- `web/app/produtos/page.tsx`

## DoD

- [x] Rota `/produtos` nao impõe `limit`/`offset` na inicializacao sem query
- [x] Ajuste sem regressao de quality gates
- [x] Story documentada com checklist e file list
