# Story - Wave 2 E2E (Gerar -> Jobs -> Produtos)

**Data:** 2026-02-27  
**Status:** Done

## Escopo

- Cobrir fluxo ponta a ponta principal da operacao:
  - `Gerar` cria produto e redireciona com `focus`
  - `Jobs` cria job e conclui polling
  - retorno para `Produtos` com `focus` atualizado

## Checklist

- [x] Teste E2E completo adicionado na suite smoke
- [x] Assertivas de URL com `focus` do produto criado e do produto do job
- [x] Assertiva de detalhe carregado no `Produtos` apos fluxo
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

- [x] Jornada critica ponta a ponta validada automaticamente
- [x] Redirecionamentos e foco de produto validados em sequencia
- [x] Story documentada com checklist e file list
