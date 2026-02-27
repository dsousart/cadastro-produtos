from __future__ import annotations

from typing import Any, Dict, Literal, Optional

from sqlalchemy import Select, func, or_, select
from sqlalchemy.orm import Session

from ..db.models.product import Product


def create_product_record(
    db: Session,
    *,
    product_input: Dict[str, Any],
    core_output: Dict[str, Any],
    tenant_id: Optional[str] = None,
    generation_job_id: Optional[str] = None,
) -> Product:
    record = Product(
        tenant_id=tenant_id,
        generation_job_id=generation_job_id,
        sku=str(product_input.get("sku") or ""),
        nome_produto=str(product_input.get("nome_produto") or ""),
        marca=str(product_input.get("marca") or ""),
        status="generated",
        score_qualidade=core_output.get("score_qualidade"),
        input_payload=product_input,
        output_payload=core_output,
    )
    db.add(record)
    db.flush()
    db.refresh(record)
    return record


def list_products(
    db: Session,
    *,
    limit: int,
    offset: int,
    status: Optional[str] = None,
    min_score: Optional[int] = None,
    q: Optional[str] = None,
    sort_by: Literal["created_at", "score_qualidade", "sku", "nome_produto"] = "created_at",
    sort_dir: Literal["asc", "desc"] = "desc",
) -> tuple[list[Product], int]:
    filters = []
    if status:
        filters.append(Product.status == status)
    if min_score is not None:
        filters.append(Product.score_qualidade >= min_score)
    if q:
        term = f"%{q.strip()}%"
        if q.strip():
            filters.append(
                or_(
                    Product.sku.ilike(term),
                    Product.nome_produto.ilike(term),
                    Product.marca.ilike(term),
                )
            )

    sort_columns = {
        "created_at": Product.created_at,
        "score_qualidade": Product.score_qualidade,
        "sku": Product.sku,
        "nome_produto": Product.nome_produto,
    }
    sort_column = sort_columns.get(sort_by, Product.created_at)
    order_expr = sort_column.asc() if sort_dir == "asc" else sort_column.desc()

    query: Select[tuple[Product]] = select(Product)
    count_query = select(func.count()).select_from(Product)
    if filters:
        query = query.where(*filters)
        count_query = count_query.where(*filters)

    # Stable secondary sort improves pagination consistency.
    query = query.order_by(order_expr, Product.id.desc()).offset(offset).limit(limit)
    items = list(db.execute(query).scalars().all())
    total = int(db.execute(count_query).scalar_one())
    return items, total


def get_product_by_id(db: Session, product_id: str) -> Optional[Product]:
    stmt = select(Product).where(Product.id == product_id)
    return db.execute(stmt).scalar_one_or_none()
