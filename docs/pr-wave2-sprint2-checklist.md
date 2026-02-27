# PR Checklist - Wave 2 + Sprint 2

**Data:** 2026-02-27  
**Objetivo:** Encerrar Sprint 2 com UX operacional consolidada, smoke E2E ampliada e CI de frontend ativa.

## Titulo sugerido do PR

`feat: close sprint2 wave2 ux + smoke e2e + web ci`

## Escopo do PR

1. Refino de UX operacional em `Produtos` e `Jobs`
2. Preservacao de contexto de filtros em navegacao por tabs
3. Expansao de cobertura smoke E2E (happy path + falhas)
4. CI de frontend com Playwright (`lint`, `typecheck`, `test`)
5. Consolidacao de documentacao de Sprint 2

## Arquivos-chave (documentacao)

- `docs/sprint-2-execution-report.md`
- `docs/wave2-front-kickoff.md`
- `docs/README.md`
- `docs/stories/2026-02-27-wave2-*.md`

## Arquivos-chave (codigo/infra)

- `web/components/products-list-panel.tsx`
- `web/components/generation-jobs-panel.tsx`
- `web/components/wave2-dashboard.tsx`
- `web/tests/e2e/smoke.spec.ts`
- `web/playwright.config.ts`
- `.github/workflows/web-ci.yml`

## Evidencias para colar no PR

```bash
cd web
npm run lint
npm run typecheck
npm test
```

## Resultado esperado dos comandos

1. `npm run lint` sem warnings/erros
2. `npm run typecheck` sem erros
3. `npm test` com smoke E2E verde (`15 passed`)

## Criterios de aceite (PR)

- [x] UX operacional base da Wave 2 consolidada
- [x] Fluxos criticos com smoke E2E automatizada
- [x] Caminhos de erro de API/rede cobertos em smoke
- [x] CI frontend ativa com Playwright
- [x] Report de Sprint 2 e stories atualizados

## Riscos / observacoes

1. Suite frontend ainda centrada em E2E; falta camada intermediaria de testes de componentes.
2. Dependencias ainda demandam ciclo dedicado de upgrade (`npm audit`).

## Proximo passo (Sprint 3)

1. E2E de fluxo ponta a ponta completo (`Gerar -> Jobs -> Produtos`)
2. Testes de integracao de componentes
3. Artifacts Playwright no CI para diagnostico rapido de falhas
