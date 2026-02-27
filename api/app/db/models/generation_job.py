from __future__ import annotations

from typing import Any, Optional

from sqlalchemy import Enum, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base
from .common import IdMixin, TimestampMixin


class GenerationJob(Base, IdMixin, TimestampMixin):
    __tablename__ = "generation_jobs"

    tenant_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("tenants.id"), index=True)
    status: Mapped[str] = mapped_column(
        Enum("pending", "running", "completed", "failed", name="generation_job_status"),
        default="pending",
        index=True,
    )
    total_items: Mapped[int] = mapped_column(Integer, default=0)
    completed_items: Mapped[int] = mapped_column(Integer, default=0)
    failed_items: Mapped[int] = mapped_column(Integer, default=0)
    request_payload: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON, nullable=True)
    result_payload: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
