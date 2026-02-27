from __future__ import annotations

from typing import Any

from fastapi import APIRouter, BackgroundTasks, HTTPException, status

from ...db.session import session_scope_optional
from ...schemas import (
    GenerationJobCreateRequest,
    GenerationJobCreateResponse,
    GenerationJobStatusResponse,
)
from ...services.generation_job_service import (
    append_generation_job_result,
    create_generation_job,
    finalize_generation_job,
    get_generation_job,
    mark_generation_job_running,
)
from ...services.pipeline_service import generate_product_content
from ...services.product_persistence_service import create_product_record


router = APIRouter(tags=["generation-jobs"])


def _run_generation_job_background(job_id: str, items: list[dict[str, Any]], bk_base_path: str) -> None:
    with session_scope_optional() as db:
        if db is None:
            return
        job = get_generation_job(db, job_id)
        if job is None:
            return

        mark_generation_job_running(db, job)
        db.commit()
        db.refresh(job)

        try:
            for index, product in enumerate(items):
                sku = product.get("sku")
                try:
                    core_output = generate_product_content(product, bk_base_path=bk_base_path)
                    product_record = create_product_record(
                        db,
                        product_input=product,
                        core_output=core_output,
                        generation_job_id=job.id,
                    )
                    append_generation_job_result(
                        db,
                        job,
                        item_result={
                            "index": index,
                            "sku": sku,
                            "status": "completed",
                            "product_id": product_record.id,
                        },
                    )
                    db.commit()
                    db.refresh(job)
                except Exception as item_exc:  # noqa: BLE001
                    db.rollback()
                    job = get_generation_job(db, job_id)
                    if job is None:
                        return
                    append_generation_job_result(
                        db,
                        job,
                        item_result={
                            "index": index,
                            "sku": sku,
                            "status": "failed",
                            "error": str(item_exc),
                        },
                    )
                    db.commit()
                    db.refresh(job)
            finalize_generation_job(db, job)
            db.commit()
        except Exception as exc:  # noqa: BLE001
            db.rollback()
            job = get_generation_job(db, job_id)
            if job is None:
                return
            finalize_generation_job(db, job, error_message=str(exc))
            db.commit()


@router.post(
    "/api/v1/generation-jobs",
    response_model=GenerationJobCreateResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def create_generation_job_endpoint(
    payload: GenerationJobCreateRequest,
    background_tasks: BackgroundTasks,
) -> GenerationJobCreateResponse:
    items = [item.model_dump(mode="json") for item in payload.items]

    with session_scope_optional() as db:
        if db is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database nao configurado para generation-jobs.",
            )

        job = create_generation_job(db, items=items)
        # import local to avoid global app coupling
        from ...core.config import get_settings

        settings = get_settings()
        background_tasks.add_task(_run_generation_job_background, job.id, items, settings.bk_base_path)
        return GenerationJobCreateResponse(
            job_id=job.id,
            status=job.status,
            total_items=job.total_items,
            message="Generation job criado e enfileirado para processamento em background.",
        )


@router.get("/api/v1/generation-jobs/{job_id}", response_model=GenerationJobStatusResponse)
def get_generation_job_status_endpoint(job_id: str) -> GenerationJobStatusResponse:
    with session_scope_optional() as db:
        if db is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database nao configurado para consulta de generation-jobs.",
            )
        job = get_generation_job(db, job_id)
        if job is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Generation job nao encontrado.")

        result_payload = job.result_payload or {}
        return GenerationJobStatusResponse(
            id=job.id,
            status=job.status,
            total_items=job.total_items,
            completed_items=job.completed_items,
            failed_items=job.failed_items,
            error_message=job.error_message,
            created_at=job.created_at,
            updated_at=job.updated_at,
            results=result_payload.get("results") or [],
        )


# Optional temporary aliases during Wave 1 rollout (ADR-000)
@router.post(
    "/api/v1/products/batch",
    response_model=GenerationJobCreateResponse,
    status_code=status.HTTP_202_ACCEPTED,
    deprecated=True,
)
def create_generation_job_alias(
    payload: GenerationJobCreateRequest,
    background_tasks: BackgroundTasks,
) -> GenerationJobCreateResponse:
    return create_generation_job_endpoint(payload, background_tasks)


@router.get("/api/v1/batches/{job_id}", response_model=GenerationJobStatusResponse, deprecated=True)
def get_generation_job_status_alias(job_id: str) -> GenerationJobStatusResponse:
    return get_generation_job_status_endpoint(job_id)
