from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Dict


REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from pipeline.pipeline import run_pipeline  # noqa: E402


def generate_product_content(
    product: Dict[str, Any],
    *,
    bk_base_path: str,
    max_iterations: int = 2,
) -> Dict[str, Any]:
    """Run the legacy core pipeline and return the original output contract."""
    base_path = bk_base_path or str(REPO_ROOT / "base_conhecimento")
    return run_pipeline(
        product,
        base_conhecimento_path=base_path,
        max_iterations=max_iterations,
    )


def build_create_product_response(core_output: Dict[str, Any]) -> Dict[str, Any]:
    """Keep CR2 fields intact and add top-level convenience fields for API clients."""
    auditoria = core_output.get("auditoria") or {}
    response = dict(core_output)
    response["audit_id"] = auditoria.get("audit_id")
    response["timestamp"] = auditoria.get("timestamp")
    response.setdefault("metadata", {})
    return response

