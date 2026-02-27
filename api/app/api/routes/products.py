from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query, Request, status

from ...db.session import session_scope_optional
from ...schemas import (
    ProductCreateResponse,
    ProductInput,
    ProductListResponse,
    ProductRecordDetail,
    ProductRecordListItem,
    ProductStatusUpdateRequest,
    ProductStatusUpdateResponse,
)
from ...services.pipeline_service import (
    build_create_product_response,
    generate_product_content,
)
from ...services.product_persistence_service import (
    create_product_record,
    get_product_by_id,
    list_products,
    update_product_status,
)


router = APIRouter(prefix="/api/v1/products", tags=["products"])


@router.post("", response_model=ProductCreateResponse, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductInput, request: Request) -> ProductCreateResponse:
    settings = request.app.state.settings

    try:
        product_dict = payload.model_dump(mode="json")
        core_output = generate_product_content(
            product_dict,
            bk_base_path=settings.bk_base_path,
        )
        response_payload = build_create_product_response(core_output)
        with session_scope_optional() as db:
            if db is not None:
                record = create_product_record(
                    db,
                    product_input=product_dict,
                    core_output=core_output,
                )
                response_payload.setdefault("metadata", {})
                response_payload["metadata"].update(
                    {
                        "db_persisted": True,
                        "product_id": record.id,
                        "status": record.status,
                    }
                )
            else:
                response_payload.setdefault("metadata", {})
                response_payload["metadata"].update({"db_persisted": False})
        return ProductCreateResponse.model_validate(response_payload)
    except ValueError as exc:
        # Common core validation issue (e.g., duplicate SKU in process scope)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Falha ao processar produto no pipeline.",
        ) from exc


@router.get("", response_model=ProductListResponse)
def get_products(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    status_filter: str | None = Query(default=None, alias="status"),
    min_score: int | None = Query(default=None, ge=0, le=100),
    q: str | None = Query(default=None, min_length=1),
    sort_by: str = Query(default="created_at", pattern="^(created_at|score_qualidade|sku|nome_produto)$"),
    sort_dir: str = Query(default="desc", pattern="^(asc|desc)$"),
) -> ProductListResponse:
    with session_scope_optional() as db:
        if db is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database nao configurado para listagem de produtos.",
            )

        items, total = list_products(
            db,
            limit=limit,
            offset=offset,
            status=status_filter,
            min_score=min_score,
            q=q,
            sort_by=sort_by,  # type: ignore[arg-type]
            sort_dir=sort_dir,  # type: ignore[arg-type]
        )
        response_items = [
            ProductRecordListItem(
                id=item.id,
                sku=item.sku,
                nome_produto=item.nome_produto,
                marca=item.marca,
                status=item.status,
                score_qualidade=item.score_qualidade,
                created_at=item.created_at,
                updated_at=item.updated_at,
            )
            for item in items
        ]
        return ProductListResponse(
            items=response_items,
            pagination={"total": total, "limit": limit, "offset": offset},
        )


@router.get("/{product_id}", response_model=ProductRecordDetail)
def get_product_detail(product_id: str) -> ProductRecordDetail:
    with session_scope_optional() as db:
        if db is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database nao configurado para consulta de produto.",
            )

        item = get_product_by_id(db, product_id)
        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produto nao encontrado.",
            )

        return ProductRecordDetail(
            id=item.id,
            tenant_id=item.tenant_id,
            generation_job_id=item.generation_job_id,
            sku=item.sku,
            nome_produto=item.nome_produto,
            marca=item.marca,
            status=item.status,
            score_qualidade=item.score_qualidade,
            input_payload=item.input_payload,
            output_payload=item.output_payload,
            created_at=item.created_at,
            updated_at=item.updated_at,
        )


@router.patch("/{product_id}", response_model=ProductStatusUpdateResponse)
def patch_product_status(product_id: str, payload: ProductStatusUpdateRequest) -> ProductStatusUpdateResponse:
    with session_scope_optional() as db:
        if db is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database nao configurado para atualizar produto.",
            )

        item = update_product_status(db, product_id=product_id, status=payload.status)
        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produto nao encontrado.",
            )

        return ProductStatusUpdateResponse(id=item.id, status=item.status, updated_at=item.updated_at)
