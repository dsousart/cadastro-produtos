# Story - Wave 3 Web CI (Playwright Artifacts)

**Data:** 2026-02-27  
**Status:** Done

## Escopo

- Melhorar diagnostico de falhas no pipeline de frontend
- Publicar artifacts do Playwright quando `npm test` falhar no CI

## Checklist

- [x] `playwright-report` habilitado no config de testes
- [x] Workflow `web-ci.yml` atualizado com upload de artifacts em falha
- [x] Paths de artifacts configurados (`playwright-report/`, `test-results/`)
- [x] `npm run lint` executado
- [x] `npm run typecheck` executado
- [x] `npm test` executado com sucesso

## Evidencias

- `cd web && npm run lint`
- `cd web && npm run typecheck`
- `cd web && npm test`

## File List

- `web/playwright.config.ts`
- `.github/workflows/web-ci.yml`

## DoD

- [x] Falhas de smoke no CI passam a ter artifact para troubleshooting rapido
- [x] Configuracao documentada com checklist e file list
