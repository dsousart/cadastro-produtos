import os
from datetime import datetime, timezone

from fastapi import APIRouter, Request


router = APIRouter(tags=["health"])


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@router.get("/healthz")
def healthz() -> dict:
    return {
        "status": "ok",
        "service": "api",
        "check": "liveness",
        "timestamp": _utc_now(),
    }


@router.get("/health")
def health_alias() -> dict:
    # Temporary alias for older stories/clients during Wave 1 rollout.
    return healthz()


@router.get("/readyz")
def readyz(request: Request) -> dict:
    settings = getattr(request.app.state, "settings", None)
    database_url = getattr(settings, "database_url", "") if settings else ""
    bk_base_path = getattr(settings, "bk_base_path", "../base_conhecimento") if settings else "../base_conhecimento"

    checks = {
        "config_loaded": "ok",
        "database": "configured" if database_url else "not_configured",
        "bk_base_path": "ok" if os.path.exists(bk_base_path) else "missing",
    }
    status = "ready" if checks["bk_base_path"] == "ok" else "not_ready"

    return {
        "status": status,
        "service": "api",
        "check": "readiness",
        "checks": checks,
        "timestamp": _utc_now(),
    }

