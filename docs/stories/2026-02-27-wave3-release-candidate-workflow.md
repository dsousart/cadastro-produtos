# Story - Wave 3 Release Candidate Workflow

**Data:** 2026-02-27  
**Status:** Done

## Escopo

- Criar fluxo de release candidate com gate obrigatoria de API + Web
- Publicar RC apenas quando quality gates estiverem verdes
- Gerar release draft automaticamente apos sucesso

## Checklist

- [x] Workflow `release-candidate.yml` criada
- [x] Input de `tag` e `target` adicionados no `workflow_dispatch`
- [x] Gate API e Web incorporadas antes de publicar RC
- [x] Fail-fast para tag existente no remoto
- [x] Criacao de tag automatizada no fim do fluxo
- [x] Criacao de draft release automatica no fim do fluxo
- [x] Runbook de operacao documentado

## File List

- `.github/workflows/release-candidate.yml`
- `docs/release-candidate-runbook.md`

## DoD

- [x] RC depende de gate unificada antes de publicacao
- [x] Processo manual de RC esta documentado
- [x] Story documentada com checklist e file list
