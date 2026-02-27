import argparse
import json
import os
import sys
from typing import Dict, Optional

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from core.auditor import audit
from core.bk_reader import build_context, read_base_conhecimento
from core.generator import generate
from core.refiner import refine


def run_pipeline(
    product: dict,
    base_conhecimento_path: str,
    max_iterations: int = 2,
    seen_skus: Optional[set] = None,
) -> Dict[str, object]:
    if seen_skus is None:
        seen_skus = set()

    sku = product.get("sku")
    if sku in seen_skus:
        raise ValueError(f"Duplicate SKU: {sku}")
    seen_skus.add(sku)

    bk_data = read_base_conhecimento(base_conhecimento_path)
    bk_context = build_context(product, bk_data)
    output = generate(product, bk_data, bk_context)

    audit_result = audit(product, output)
    output.update(audit_result)

    iterations = 0
    while iterations < max_iterations and output["auditoria"]["resultado"] == "reprovado":
        output = refine(product, output)
        audit_result = audit(product, output)
        output.update(audit_result)
        iterations += 1

    return output


def _load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _write_json(path: str, data: dict) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser(description="Premium cadastro pipeline")
    parser.add_argument("--input", required=True, help="Path to product JSON")
    parser.add_argument(
        "--bk",
        default=os.path.join(os.getcwd(), "base_conhecimento"),
        help="Base conhecimento path",
    )
    parser.add_argument("--output", required=True, help="Path to output JSON")
    parser.add_argument("--max-iterations", type=int, default=2)
    args = parser.parse_args()

    product = _load_json(args.input)
    result = run_pipeline(
        product,
        base_conhecimento_path=args.bk,
        max_iterations=args.max_iterations,
    )
    _write_json(args.output, result)


if __name__ == "__main__":
    main()
