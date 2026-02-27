from __future__ import annotations

from typing import Any, Optional

from sqlalchemy import Enum, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base
from .common import IdMixin, TimestampMixin


class Product(Base, IdMixin, TimestampMixin):
    __tablename__ = "products"

    tenant_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("tenants.id"), index=True)
    generation_job_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("generation_jobs.id"), nullable=True
    )
    sku: Mapped[str] = mapped_column(String(120), index=True)
    nome_produto: Mapped[str] = mapped_column(String(255))
    marca: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(
        Enum(
            "draft",
            "in_review",
            "generated",
            "approved",
            "rejected",
            "published",
            name="product_status",
        ),
        default="draft",
        index=True,
    )
    score_qualidade: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    input_payload: Mapped[dict[str, Any]] = mapped_column(JSON)
    output_payload: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON, nullable=True)
