from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field

from .product import ProductInput


class GenerationJobCreateRequest(BaseModel):
    items: List[ProductInput] = Field(..., min_length=1, max_length=20)


class GenerationJobCreateResponse(BaseModel):
    job_id: str
    status: Literal["pending", "running", "completed", "failed"]
    total_items: int
    message: str


class GenerationJobItemResult(BaseModel):
    index: int
    sku: Optional[str] = None
    status: Literal["completed", "failed"]
    product_id: Optional[str] = None
    error: Optional[str] = None
    output: Optional[Dict[str, Any]] = None


class GenerationJobStatusResponse(BaseModel):
    id: str
    status: Literal["pending", "running", "completed", "failed"]
    total_items: int
    completed_items: int
    failed_items: int
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    results: List[GenerationJobItemResult] = Field(default_factory=list)

