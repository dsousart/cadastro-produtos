from __future__ import annotations

import importlib
import json
import os
import sys
from pathlib import Path
from typing import Iterator

import pytest
from fastapi.testclient import TestClient


REPO_ROOT = Path(__file__).resolve().parents[2]


def _reload_api_app():
    # Rebuild app after env changes (settings/session are initialized at import time).
    for name in list(sys.modules):
        if name == "api.main" or name.startswith("api.app"):
            sys.modules.pop(name, None)
    import api.main as api_main

    importlib.reload(api_main)
    return api_main.app


@pytest.fixture
def example_input() -> dict:
    return json.loads((REPO_ROOT / "examples-input.json").read_text(encoding="utf-8"))


@pytest.fixture
def client_no_db(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.delenv("DATABASE_URL", raising=False)
    app = _reload_api_app()
    with TestClient(app) as client:
        yield client


@pytest.fixture
def client_db(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    db_url = os.getenv("TEST_DATABASE_URL")
    if not db_url:
        pytest.skip("TEST_DATABASE_URL not configured")
    monkeypatch.setenv("DATABASE_URL", db_url)
    app = _reload_api_app()
    with TestClient(app) as client:
        yield client

