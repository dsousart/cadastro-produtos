import argparse
import json
import os
import sys
from typing import Dict

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from core.bk_reader import read_base_conhecimento
from pipeline.pipeline import run_pipeline


def _compose_text(output: dict) -> str:
    parts = [
        output.get("titulo", ""),
        output.get("subtitulo", ""),
        output.get("descricao", ""),
        " ".join(output.get("bullet_points", [])),
    ]
    return "\n\n".join([p for p in parts if p])


def _extract_improvements(auditoria: dict) -> list:
    motivos = auditoria.get("motivos_reprovacao") or []
    return motivos


def _extract_bk_snippets(bk_data: Dict[str, list]) -> list:
    snippets = []
    for entries in bk_data.values():
        for entry in entries[:1]:
            content = entry.get("content", "")
            snippet = " ".join(content.split())
            if snippet:
                snippets.append(snippet[:200])
    return snippets


def _load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _write_json(path: str, data: dict) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser(description="Pipeline runner")
    parser.add_argument("--input", required=True, help="Path to product JSON")
    parser.add_argument("--out", required=True, help="Path to output JSON")
    parser.add_argument(
        "--bk",
        default=os.path.join(os.getcwd(), "base_conhecimento"),
        help="Base conhecimento path",
    )
    parser.add_argument("--max-iterations", type=int, default=2)
    args = parser.parse_args()

    product = _load_json(args.input)
    output = run_pipeline(
        product,
        base_conhecimento_path=args.bk,
        max_iterations=args.max_iterations,
    )
    bk_data = read_base_conhecimento(args.bk)

    bk_context = output.get("bk_context", {})
    response = {
        "texto_final": _compose_text(output),
        "scores": {
            "score_qualidade": output.get("score_qualidade"),
            "resultado": output.get("auditoria", {}).get("resultado"),
        },
        "melhorias_sugeridas": _extract_improvements(output.get("auditoria", {})),
        "trechos_BK_usados": bk_context.get("snippets") or _extract_bk_snippets(bk_data),
    }

    _write_json(args.out, response)


if __name__ == "__main__":
    main()
