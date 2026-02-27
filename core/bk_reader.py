import os
from typing import Dict, List


def read_base_conhecimento(base_path: str) -> Dict[str, List[dict]]:
    """
    Read markdown files from base_conhecimento and return a dict by category.
    It ignores files starting with "_" (templates) and non-markdown files.
    """
    result: Dict[str, List[dict]] = {}
    if not os.path.isdir(base_path):
        return result

    for root, _dirs, files in os.walk(base_path):
        category = os.path.basename(root)
        for name in files:
            if not name.lower().endswith(".md"):
                continue
            if name.startswith("_"):
                continue
            path = os.path.join(root, name)
            try:
                with open(path, "r", encoding="utf-8") as handle:
                    content = handle.read()
            except OSError:
                continue

            entry = {
                "path": path,
                "category": category,
                "filename": name,
                "content": content,
            }
            result.setdefault(category, []).append(entry)

    return result


def _extract_terms(product: dict) -> List[str]:
    terms = []
    for key in [
        "categoria",
        "subcategoria",
        "tecido",
        "composicao",
        "modelagem",
        "acabamento",
        "colecao",
    ]:
        value = product.get(key)
        if not value:
            continue
        if isinstance(value, list):
            terms.extend([str(v) for v in value])
        else:
            terms.append(str(value))

    merged = []
    for term in terms:
        for piece in str(term).replace("/", " ").replace(",", " ").split():
            piece = piece.strip().lower()
            if len(piece) < 3:
                continue
            if piece not in merged:
                merged.append(piece)
    return merged


def _find_snippet(content: str, term: str, window: int = 160) -> str:
    lower = content.lower()
    idx = lower.find(term.lower())
    if idx == -1:
        return ""
    start = max(0, idx - window)
    end = min(len(content), idx + window)
    snippet = content[start:end].strip()
    return " ".join(snippet.split())


def build_context(product: dict, bk_data: Dict[str, List[dict]]) -> dict:
    terms = _extract_terms(product)
    hits = []
    snippets = []
    for entries in bk_data.values():
        for entry in entries:
            content = entry.get("content", "")
            lower = content.lower()
            for term in terms:
                if term in lower and term not in hits:
                    hits.append(term)
                    snippet = _find_snippet(content, term)
                    if snippet:
                        snippets.append(snippet)

    missing_terms = [t for t in terms if t not in hits]
    confidence_score = round(len(hits) / len(terms), 2) if terms else 0.0

    return {
        "confidence_score": confidence_score,
        "hits": hits,
        "missing_terms": missing_terms,
        "snippets": snippets[:10],
    }
