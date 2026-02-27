# Story - Wave 2 Smoke (Network Failures)

**Data:** 2026-02-27  
**Status:** Done

## Escopo

- Cobrir indisponibilidade de backend (falha de rede) na suite smoke E2E
- Validar feedback de erro operacional em `Produtos` e `Gerar`

## Checklist

- [x] Teste de falha de rede em listagem de produtos adicionado
- [x] Teste de falha de rede em criacao de produto adicionado
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

- [x] Caminhos de indisponibilidade de backend cobertos em smoke
- [x] Mensagens de erro esperadas validadas automaticamente
- [x] Story documentada com checklist e file list
