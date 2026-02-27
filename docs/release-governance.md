# Release Governance Policy

Politica operacional para versionamento e protecao de branch no repositorio.

## Versionamento

- Padrao: SemVer `MAJOR.MINOR.PATCH`
- Exemplos:
  - `v0.3.0` (release final)
  - `v0.3.1` (hotfix)
  - `v0.4.0` (nova feature em lote)

## Convention de RC

- Padrao de tag RC: `vMAJOR.MINOR.PATCH-rc.N`
- Exemplos:
  - `v0.3.0-rc.1`
  - `v0.3.0-rc.2`
- RC deve ser criada somente via workflow `Release Candidate`.
- Release final deve ser promovida somente via workflow `Release`.

## Fluxo oficial

1. Merge em `main` com CI verde (`api-ci` e `web-ci`).
2. Rodar workflow `Release Candidate` com `tag` RC.
3. Validar RC (gates API + Web).
4. Rodar workflow `Release` com:
   - `rc_tag` (RC existente)
   - `release_tag` (tag final SemVer)
5. Publicar release final automatica no GitHub Releases.

## Branch Protection (main)

Configurar em `Settings > Branches > Add branch protection rule`:

- Branch name pattern: `main`
- Require a pull request before merging: `ON`
- Require approvals: minimo `1`
- Dismiss stale approvals when new commits are pushed: `ON`
- Require conversation resolution before merging: `ON`
- Require status checks to pass before merging: `ON`
- Required checks:
  - `api-ci`
  - `web-ci`
- Require branches to be up to date before merging: `ON`
- Include administrators: `ON`
- Restrict who can push to matching branches: `ON` (somente mantenedores)

## Guardrails adicionais

- Bloquear force-push em `main`.
- Bloquear delete de branch `main`.
- Nao criar tags de release manualmente fora dos workflows.
- Toda mudanca de release process deve atualizar:
  - `docs/release-candidate-runbook.md`
  - `docs/release-final-runbook.md`
  - `docs/release-governance.md`
