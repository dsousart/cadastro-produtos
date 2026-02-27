# Story - Wave 3 Frontend Component Integration Tests

**Data:** 2026-02-27  
**Status:** Done

## Escopo

- Criar camada inicial de testes de componentes no frontend (Vitest + Testing Library)
- Cobrir componentes de base (`JsonViewer`, `ProductGeneratorForm`)
- Integrar execucao de unit tests no pipeline de CI frontend

## Checklist

- [x] Dependencias de unit tests instaladas (Vitest + Testing Library + jsdom)
- [x] Configuracao de testes criada (`vitest.config.ts`, `vitest.setup.ts`)
- [x] Script `npm run test:unit` adicionado
- [x] Testes de componentes adicionados
- [x] `web-ci.yml` atualizado para rodar `test:unit`
- [x] `npm run lint` executado
- [x] `npm run typecheck` executado
- [x] `npm run test:unit` executado com sucesso
- [x] `npm test` executado com sucesso

## Evidencias

- `cd web && npm run lint`
- `cd web && npm run typecheck`
- `cd web && npm run test:unit`
- `cd web && npm test`

## File List

- `web/package.json`
- `web/package-lock.json`
- `web/vitest.config.ts`
- `web/vitest.setup.ts`
- `web/tests/unit/json-viewer.test.tsx`
- `web/tests/unit/product-generator-form.test.tsx`
- `web/components/json-viewer.tsx`
- `web/components/product-generator-form.tsx`
- `.github/workflows/web-ci.yml`
- `web/README.md`

## DoD

- [x] Projeto possui camada de testes de componentes executavel localmente e no CI
- [x] Cobertura inicial dos componentes chave de visualizacao/submissao
- [x] Story documentada com checklist e file list
