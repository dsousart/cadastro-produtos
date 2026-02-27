from __future__ import annotations

from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from ..db.models.generation_job import GenerationJob


def create_generation_job(
    db: Session,
    *,
    items: list[dict[str, Any]],
    tenant_id: Optional[str] = None,
) -> GenerationJob:
    job = GenerationJob(
        tenant_id=tenant_id,
        status="pending",
        total_items=len(items),
        completed_items=0,
        failed_items=0,
        request_payload={"items": items},
        result_payload={"results": []},
    )
    db.add(job)
    db.flush()
    db.refresh(job)
    return job


def get_generation_job(db: Session, job_id: str) -> Optional[GenerationJob]:
    return db.get(GenerationJob, job_id)


def mark_generation_job_running(db: Session, job: GenerationJob) -> GenerationJob:
    job.status = "running"
    db.add(job)
    db.flush()
    db.refresh(job)
    return job


def append_generation_job_result(
    db: Session,
    job: GenerationJob,
    *,
    item_result: dict[str, Any],
) -> GenerationJob:
    # Rebuild JSON payload objects to ensure SQLAlchemy detects column changes.
    current_payload = dict(job.result_payload or {})
    results = list(current_payload.get("results") or [])
    results.append(item_result)
    current_payload["results"] = results
    job.result_payload = current_payload

    if item_result.get("status") == "completed":
        job.completed_items += 1
    elif item_result.get("status") == "failed":
        job.failed_items += 1

    db.add(job)
    db.flush()
    db.refresh(job)
    return job


def finalize_generation_job(
    db: Session,
    job: GenerationJob,
    *,
    error_message: str | None = None,
) -> GenerationJob:
    if error_message:
        job.status = "failed"
        job.error_message = error_message
    elif job.failed_items > 0 and job.completed_items == 0:
        job.status = "failed"
    else:
        job.status = "completed"
    db.add(job)
    db.flush()
    db.refresh(job)
    return job
