# Final Release Runbook

Fluxo recomendado para promover uma RC validada para release final.

## Pre-requisito

- Tag de RC existente (exemplo: `v0.3.0-rc.1`)
- Workflow `Release` habilitada no repositorio
- Gate de API e Web verde para a RC informada

## Como executar

1. Abra `Actions` no GitHub.
2. Selecione workflow `Release`.
3. Clique em `Run workflow`.
4. Preencha:
   - `rc_tag`: exemplo `v0.3.0-rc.1`
   - `release_tag`: exemplo `v0.3.0`
5. Execute.

## O que o workflow faz

1. Faz checkout da `rc_tag` e roda `api-gate`:
   - migra DB
   - `pytest` de integracao API
   - `compileall`
2. Faz checkout da `rc_tag` e roda `web-gate`:
   - `npm run release:check` (lint + typecheck + unit + smoke E2E)
3. Faz validacoes antes de publicar:
   - falha se `rc_tag` nao existe no remoto
   - falha se `release_tag` ja existe no remoto
4. Se tudo passar:
   - cria a `release_tag` apontando para o mesmo commit da RC
   - publica release final automaticamente (nao draft, nao prerelease)

## Regras de seguranca

- Nunca criar `release_tag` manualmente fora do workflow.
- Nunca reaproveitar uma `release_tag` existente.
- Release final deve sempre partir de uma RC validada.

## Politica

- RC aprovada e release final devem apontar para o mesmo SHA.
- Qualquer falha no gate bloqueia publicacao.
