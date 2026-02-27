# Release Candidate Runbook

Fluxo recomendado para gerar RC com gate de qualidade obrigatoria.

## Pre-requisito

- `main` atualizada e estavel
- workflow `Release Candidate` habilitada no repositorio

## Como executar

1. Abra `Actions` no GitHub.
2. Selecione workflow `Release Candidate`.
3. Clique em `Run workflow`.
4. Preencha:
   - `tag`: exemplo `v0.3.0-rc.1`
   - `target`: `main` (ou SHA especifico)
5. Execute.

## O que o workflow faz

1. Roda `api-gate`:
   - migra DB
   - `pytest` de integracao API
   - `compileall`
2. Roda `web-gate`:
   - `npm run release:check` (lint + typecheck + unit + smoke E2E)
3. Se tudo passar:
   - cria tag no repo
   - cria release draft com release notes automaticas

## Politica

- Nao criar tag manual de RC fora deste workflow.
- Qualquer falha no gate bloqueia publicacao da RC.
