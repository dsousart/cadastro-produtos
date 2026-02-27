from __future__ import annotations

import time
from uuid import uuid4


def test_health_endpoints(client_no_db):
    for path, expected_status in [("/healthz", "ok"), ("/health", "ok")]:
        resp = client_no_db.get(path)
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == expected_status

    ready = client_no_db.get("/readyz")
    assert ready.status_code == 200
    body = ready.json()
    assert body["check"] == "readiness"
    assert body["checks"]["config_loaded"] == "ok"
    assert body["checks"]["database"] == "not_configured"


def test_create_product_stateless(client_no_db, example_input):
    payload = dict(example_input)
    payload["sku"] = f"{payload['sku']}-STAT-{uuid4().hex[:6]}"
    resp = client_no_db.post("/api/v1/products", json=payload)
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["auditoria"]["resultado"] in {"aprovado", "reprovado"}
    assert body["metadata"]["db_persisted"] is False
    assert "titulo" in body and "descricao" in body


def test_list_and_jobs_require_db_when_not_configured(client_no_db):
    assert client_no_db.get("/api/v1/products").status_code == 503
    assert client_no_db.post("/api/v1/generation-jobs", json={"items": []}).status_code == 422


def test_db_flow_products_and_generation_jobs(client_db, example_input):
    payload = dict(example_input)
    payload["sku"] = f"{payload['sku']}-DB-{uuid4().hex[:8]}"

    create_resp = client_db.post("/api/v1/products", json=payload)
    assert create_resp.status_code == 201, create_resp.text
    created = create_resp.json()
    assert created["metadata"]["db_persisted"] is True
    product_id = created["metadata"]["product_id"]
    assert product_id

    list_resp = client_db.get("/api/v1/products", params={"status": "generated"})
    assert list_resp.status_code == 200, list_resp.text
    list_body = list_resp.json()
    assert list_body["pagination"]["total"] >= 1
    assert any(item["id"] == product_id for item in list_body["items"])

    search_resp = client_db.get("/api/v1/products", params={"q": payload["sku"]})
    assert search_resp.status_code == 200, search_resp.text
    search_body = search_resp.json()
    assert any(item["id"] == product_id for item in search_body["items"])

    sort_resp = client_db.get(
        "/api/v1/products",
        params={"sort_by": "sku", "sort_dir": "asc", "limit": 5, "offset": 0},
    )
    assert sort_resp.status_code == 200, sort_resp.text
    sort_body = sort_resp.json()
    assert "items" in sort_body and "pagination" in sort_body

    detail_resp = client_db.get(f"/api/v1/products/{product_id}")
    assert detail_resp.status_code == 200, detail_resp.text
    detail = detail_resp.json()
    assert detail["sku"] == payload["sku"]

    job_payload = dict(example_input)
    job_payload["sku"] = f"{example_input['sku']}-JOB-{uuid4().hex[:8]}"
    job_create = client_db.post("/api/v1/generation-jobs", json={"items": [job_payload]})
    assert job_create.status_code == 202, job_create.text
    job_id = job_create.json()["job_id"]

    final_body = None
    for _ in range(15):
        status_resp = client_db.get(f"/api/v1/generation-jobs/{job_id}")
        assert status_resp.status_code == 200, status_resp.text
        final_body = status_resp.json()
        if final_body["status"] in {"completed", "failed"}:
            break
        time.sleep(0.2)

    assert final_body is not None
    assert final_body["status"] == "completed"
    assert final_body["completed_items"] == 1
    assert final_body["failed_items"] == 0
    assert len(final_body["results"]) == 1
    assert final_body["results"][0]["status"] == "completed"
