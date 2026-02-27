# Story - Wave 3 Release Gate (Checklist + Workflow)

**Data:** 2026-02-27  
**Status:** Done

## Escopo

- Definir gate unico de release para API + Web
- Criar comando padrao de verificacao completa da Web
- Criar workflow manual de release gate no GitHub Actions

## Checklist

- [x] Script `npm run release:check` criado no frontend
- [x] Workflow `.github/workflows/release-gate.yml` criada (API + Web)
- [x] Checklist de release documentada em `docs/release-gate-checklist.md`
- [x] `npm run lint` executado
- [x] `npm run typecheck` executado
- [x] `npm run test:unit` executado
- [x] `npm test` executado com sucesso

## Evidencias

- `cd web && npm run lint`
- `cd web && npm run typecheck`
- `cd web && npm run test:unit`
- `cd web && npm test`

## File List

- `.github/workflows/release-gate.yml`
- `web/package.json`
- `web/package-lock.json`
- `web/scripts/release-gate.mjs`
- `web/README.md`
- `docs/release-gate-checklist.md`

## DoD

- [x] Processo de release possui gate unificada e reproduzivel
- [x] Workflow manual pronta para execucao antes de publicar release
- [x] Story documentada com checklist e file list
