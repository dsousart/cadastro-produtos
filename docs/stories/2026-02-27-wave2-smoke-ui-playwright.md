# Story - Wave 2 Smoke UI (Playwright)

**Data:** 2026-02-27  
**Status:** Done

## Escopo

- Fechar gap de quality gate `npm test` no frontend
- Adicionar suite smoke E2E inicial com Playwright
- Validar fluxos basicos de `Produtos`, `Gerar` e `Jobs`

## Checklist

- [x] Dependencia `@playwright/test` instalada no `web`
- [x] Script `npm test` configurado
- [x] Config Playwright criada (`webServer` + `baseURL`)
- [x] Smoke tests iniciais criados para abas principais
- [x] Browser Chromium instalado para execucao local
- [x] `npm run lint` executado
- [x] `npm run typecheck` executado
- [x] `npm test` executado com sucesso

## Evidencias

- `cd web && npm run lint`
- `cd web && npm run typecheck`
- `cd web && npm test`

## File List

- `web/package.json`
- `web/package-lock.json`
- `web/playwright.config.ts`
- `web/tests/e2e/smoke.spec.ts`

## DoD

- [x] Quality gate `npm test` habilitado e operacional
- [x] Cobertura smoke para fluxos criticos iniciais da Wave 2
- [x] Story documentada com checklist e arquivos alterados
