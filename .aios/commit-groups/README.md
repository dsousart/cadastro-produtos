# Commit Grouping Plan (2026-03-05)

Branch ativa: `chore/aios-sync-stabilization`

Ordem recomendada (especialistas):
1. `feat-core-runtime` (Dev)
2. `chore-tooling-infra` (DevOps)
3. `chore-aios-assets` (AIOS Master/PM-Process)
4. `data-kb-registry` (Data/Knowledge)
5. `docs-templates-guides` (Docs)
6. `chore-agent-sync` (AgentOps)

Arquivos de grupo:
- `feat-core-runtime.txt`
- `chore-tooling-infra.txt`
- `chore-aios-assets.txt`
- `data-kb-registry.txt`
- `docs-templates-guides.txt`
- `chore-agent-sync.txt`
- `other.txt` (review manual)

Staging por grupo (PowerShell):
`Get-Content .aios/commit-groups/feat-core-runtime.txt | % { git add -- $_ }`

Commit por grupo (exemplo):
`git commit -m "feat(core): ..."`

Observacao:
- `other.txt` contem `.env.backup...` e deve ficar fora de commit.
