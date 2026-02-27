# PR Checklist - Wave 1 + Sprint 1

**Data:** 2026-02-26  
**Objetivo:** Encerrar Wave 1 formalmente e consolidar hardening base da Wave 2.

## Titulo sugerido do PR

`feat: close wave1 api foundation + sprint1 hardening baseline`

## Escopo do PR

1. Fechamento formal das stories Wave 1 (`1.1` a `1.6`)
2. Evidencias e documentacao de execucao da Sprint 1
3. Hardening frontend com cliente HTTP compartilhado e erros padronizados
4. Ajustes de quality gates (`lint`, `typecheck`, `pytest`)

## Arquivos-chave (documentacao)

- `docs/stories/2026-02-26-wave1-api-foundation-closure.md`
- `docs/wave1-backlog-tecnico.md`
- `docs/sprint-1-execution-report.md`
- `docs/wave2-front-kickoff.md`

## Arquivos-chave (codigo)

- `web/lib/api-client.ts`
- `web/components/product-generator-form.tsx`
- `web/components/products-list-panel.tsx`
- `web/components/generation-jobs-panel.tsx`
- `web/.eslintrc.json`
- `pytest.ini`

## Evidencias para colar no PR

```bash
# Web
cd web
npm run lint
npm run typecheck

# API (na raiz do repo)
python -m pytest -q api/tests/test_api_integration.py
python -m compileall api
```

## Resultado esperado dos comandos

1. `npm run lint` sem warnings/erros
2. `npm run typecheck` sem erros
3. `pytest` com `4 passed`
4. `compileall` sem erro sintatico

## Criterios de aceite (PR)

- [x] Wave 1 formalmente encerrada em doc de story
- [x] Backlog Wave 1 atualizado para status fechado tecnicamente
- [x] Report da Sprint 1 criado
- [x] Cliente HTTP compartilhado adicionado no frontend
- [x] Componentes principais migrados para cliente compartilhado
- [x] Quality gates executados e registrados

## Riscos / observacoes

1. `npm run build` pode falhar em ambiente local por `spawn EPERM` (restricao do host), sem indicar erro funcional de codigo.
2. Dependencias reportam vulnerabilidades no `npm audit`; tratar em sprint dedicada de upgrade/deps.

## Proximo passo (amanha)

1. Iniciar Sprint 2 (Wave 2 UX final + smoke UI + E2E inicial)
2. Definir backlog detalhado de Sprint 2 antes do primeiro commit
