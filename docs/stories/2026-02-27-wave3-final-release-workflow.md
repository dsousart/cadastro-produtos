# Story - Wave 3 Final Release Workflow

**Data:** 2026-02-27  
**Status:** Done

## Escopo

- Criar workflow para promover RC validada para release final
- Garantir gates obrigatorias de API e Web antes da publicacao final
- Documentar operacao de release final

## Checklist

- [x] Workflow `.github/workflows/release.yml` criada
- [x] Inputs `rc_tag` e `release_tag` adicionados em `workflow_dispatch`
- [x] Gate API e Web executadas usando `rc_tag`
- [x] Guard para falha quando `rc_tag` nao existir no remoto
- [x] Guard para falha quando `release_tag` ja existir no remoto
- [x] Criacao automatica da `release_tag` apontando para o SHA da RC
- [x] Publicacao automatica da release final (nao draft)
- [x] Runbook final documentado

## File List

- `.github/workflows/release.yml`
- `docs/release-final-runbook.md`
- `docs/release-candidate-runbook.md`
- `docs/README.md`

## DoD

- [x] Release final depende de gate unificada antes de publicar
- [x] Processo manual de release final esta documentado
- [x] Story documentada com checklist e file list
