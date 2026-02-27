import os
import re
from typing import Any, Dict, List


REQUIRED_SECTIONS = [
    "Titulo",
    "Categoria",
    "Fonte",
    "Data",
    "Resumo",
    "Detalhes",
    "Aplicacao no Cadastro",
    "Termos e Sinonimos",
    "Regras e Restricoes",
    "Tags",
]

OPTIONAL_SECTIONS = [
    "Sinais Tecnicos Extraidos",
]

TECHNICAL_MARKERS = [
    "gsm",
    "micron",
    "merino",
    "wool",
    "algodao",
    "linho",
    "oxford",
    "sarja",
    "malha",
    "jersey",
    "caimento",
    "modelagem",
    "anti-odor",
    "antiodor",
    "anti-wrinkle",
    "anti-pilling",
    "pilling",
    "uv",
    "stretch",
    "dry",
    "breathable",
    "respir",
    "encolh",
    "dimensional",
    "abras",
    "umidade",
    "ventil",
]

NOISE_MARKERS = [
    "add to cart",
    "cart",
    "checkout",
    "shipping",
    "returns",
    "exchange",
    "reviews",
    "review",
    "newsletter",
    "subscribe",
    "privacy policy",
    "terms of service",
    "gift card",
    "help center",
    "account",
    "shop now",
    "sort most recent",
    "verified buyer",
]


def _read_text(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read()
    except OSError:
        return ""


def _parse_sections(text: str) -> Dict[str, str]:
    matches = list(re.finditer(r"(?m)^##\s+(.+?)\s*$", text))
    sections: Dict[str, str] = {}
    for idx, match in enumerate(matches):
        name = match.group(1).strip()
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        sections[name] = text[start:end].strip()
    return sections


def _normalize_whitespace(text: str) -> str:
    return " ".join((text or "").split())


def _bullet_count(section_text: str) -> int:
    return len(re.findall(r"(?m)^\s*-\s+\S+", section_text or ""))


def _count_markers(text: str, markers: List[str]) -> int:
    lower = (text or "").lower()
    return sum(lower.count(marker) for marker in markers)


def _extract_category(sections: Dict[str, str]) -> str:
    raw = _normalize_whitespace(sections.get("Categoria", ""))
    if raw.startswith("-"):
        raw = raw[1:].strip()
    return raw.lower()


def _validate_structure(sections: Dict[str, str]) -> Dict[str, List[str]]:
    errors: List[str] = []
    warnings: List[str] = []

    for section in REQUIRED_SECTIONS:
        content = sections.get(section, "")
        if section not in sections:
            errors.append(f"Estrutura: Missing section: ## {section}")
            continue
        if not _normalize_whitespace(content):
            errors.append(f"Estrutura: Empty section: ## {section}")

    # Explicit support for optional sections: no error if absent; validate only if present.
    for section in OPTIONAL_SECTIONS:
        if section in sections and not _normalize_whitespace(sections[section]):
            warnings.append(f"Estrutura: Optional section empty: ## {section}")

    return {"errors": errors, "warnings": warnings}


def _validate_quality(path: str, sections: Dict[str, str]) -> Dict[str, List[str]]:
    errors: List[str] = []
    warnings: List[str] = []

    category = _extract_category(sections)
    resumo = _normalize_whitespace(sections.get("Resumo", ""))
    detalhes = _normalize_whitespace(sections.get("Detalhes", ""))
    termos = _normalize_whitespace(sections.get("Termos e Sinonimos", ""))
    sinais = _normalize_whitespace(sections.get("Sinais Tecnicos Extraidos", ""))
    all_quality_text = " ".join([resumo, detalhes, termos, sinais]).strip()

    detalhes_len = len(detalhes)
    resumo_bullets = _bullet_count(sections.get("Resumo", ""))
    sinais_bullets = _bullet_count(sections.get("Sinais Tecnicos Extraidos", ""))
    termos_bullets = _bullet_count(sections.get("Termos e Sinonimos", ""))

    if detalhes_len < 40:
        errors.append(f"Qualidade: Detalhes muito curto ({detalhes_len} chars)")
    elif detalhes_len < 120:
        warnings.append(f"Qualidade: Detalhes curto ({detalhes_len} chars)")

    if resumo_bullets == 0:
        errors.append("Qualidade: Resumo sem bullets")
    elif resumo_bullets < 2:
        warnings.append(f"Qualidade: Resumo com poucos bullets ({resumo_bullets})")

    technical_hits = _count_markers(all_quality_text, TECHNICAL_MARKERS)
    if category != "_pendente" and technical_hits == 0:
        warnings.append("Qualidade: Sem sinais tecnicos detectados")
    elif category in {"tecidos", "tecnologias"} and technical_hits < 2:
        warnings.append(
            f"Qualidade: Poucos sinais tecnicos para categoria {category} ({technical_hits})"
        )

    if "Sinais Tecnicos Extraidos" in sections and sinais_bullets == 0:
        warnings.append("Qualidade: Secao opcional de sinais tecnicos presente mas vazia")

    if category != "_pendente" and termos_bullets == 0 and termos.strip() in {"", "-"}:
        warnings.append("Qualidade: Termos e sinonimos vazio")

    noise_hits = _count_markers(detalhes, NOISE_MARKERS)
    if noise_hits >= 8:
        errors.append(f"Ruido: Excesso de termos de ruído ({noise_hits})")
    elif noise_hits >= 3:
        warnings.append(f"Ruido: Possivel ruido de ecommerce ({noise_hits})")

    if "verified buyer" in detalhes.lower() or "rated 5 out of 5 stars" in detalhes.lower():
        errors.append("Ruido: Conteudo de reviews detectado em Detalhes")

    if category == "_pendente":
        warnings.append("Qualidade: Categoria _pendente requer revisao manual")

    if path.lower().endswith("desktop.md") and detalhes_len < 80:
        warnings.append("Qualidade: Arquivo potencialmente residual de OCR/asset curto")

    return {"errors": errors, "warnings": warnings}


def validate_file(path: str) -> Dict[str, Any]:
    text = _read_text(path)
    if not text:
        return {
            "ok": False,
            "errors": ["Estrutura: Arquivo vazio ou nao legivel"],
            "warnings": [],
            "meta": {},
        }

    sections = _parse_sections(text)
    structure = _validate_structure(sections)
    quality = _validate_quality(path, sections)

    errors = structure["errors"] + quality["errors"]
    warnings = structure["warnings"] + quality["warnings"]

    meta = {
        "category": _extract_category(sections),
        "detalhes_chars": len(_normalize_whitespace(sections.get("Detalhes", ""))),
        "has_sinais_tecnicos": "Sinais Tecnicos Extraidos" in sections,
    }

    return {
        "ok": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "meta": meta,
    }


def scan_base(base_path: str) -> Dict[str, Any]:
    files: Dict[str, Dict[str, Any]] = {}
    summary = {
        "files_scanned": 0,
        "files_with_errors": 0,
        "files_with_warnings": 0,
        "error_count": 0,
        "warning_count": 0,
    }

    for root, _dirs, filenames in os.walk(base_path):
        for name in filenames:
            if not name.lower().endswith(".md"):
                continue
            if name.startswith("_"):
                continue
            path = os.path.join(root, name)
            result = validate_file(path)
            summary["files_scanned"] += 1
            if result["errors"]:
                summary["files_with_errors"] += 1
                summary["error_count"] += len(result["errors"])
            if result["warnings"]:
                summary["files_with_warnings"] += 1
                summary["warning_count"] += len(result["warnings"])
            if result["errors"] or result["warnings"]:
                files[path] = result

    return {"summary": summary, "files": files}
