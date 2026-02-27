# API (Wave 1 Foundation)

Minimal FastAPI skeleton for Wave 1 (`Stories 1.1-1.6`).

## Story 1.1 scope

- FastAPI app bootstrap
- `GET /healthz`
- `GET /readyz`
- optional alias `GET /health`
- local run command

## Quick start

```bash
cd api
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Alternative (from repo root, matching PRD intent):

```bash
uvicorn api.main:app --reload
```

## Endpoints

- `GET /healthz` -> liveness
- `GET /readyz` -> readiness (config + optional DB DSN presence)
- `GET /health` -> temporary alias to `/healthz` (ADR-000)

## Notes

- Auth/RBAC are out of scope for Wave 1 (ADR-000).
- Core pipeline integration starts on Story 1.3.

