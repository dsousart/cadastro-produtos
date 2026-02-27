# Release Gate Checklist

Checklist unica para validar publicacao com qualidade minima no estado atual do projeto.

## Escopo do gate

- API: migrations, testes de integracao e compilacao
- Web: lint, typecheck, unit tests e smoke E2E

## Execucao manual local

### API

```bash
python -m alembic -c api/alembic.ini upgrade head
python -m pytest -q api/tests/test_api_integration.py
python -m compileall api
```

### Web

```bash
cd web
npm run release:check
```

## Execucao no GitHub Actions

- Workflow manual: `.github/workflows/release-gate.yml`
- Trigger: `workflow_dispatch`

## Criterio de aprovacao

1. Todas as etapas da API verdes
2. Todas as etapas da Web verdes
3. Sem regressao em CI (`api-ci.yml`, `web-ci.yml`)

## Evidencias para PR de release

- link da execucao de `Release Gate`
- logs finais de `npm run release:check`
- hash do commit release-candidate
