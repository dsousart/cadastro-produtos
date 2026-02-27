from typing import List


def _fit_length(text: str, min_len: int, max_len: int, pad: str) -> str:
    text = " ".join((text or "").split())
    if len(text) > max_len:
        return text[:max_len].rstrip()
    while len(text) < min_len:
        text = f"{text} {pad}".strip()
        if len(text) > max_len:
            return text[:max_len].rstrip()
    return text


def _ensure_bullets(bullets: List[str], extras: List[str]) -> List[str]:
    result = [b for b in bullets if b]
    for extra in extras:
        if len(result) >= 6:
            break
        if extra and extra not in result:
            result.append(extra)
    if len(result) < 4:
        result.extend(["Acabamento premium", "Conforto no uso diario"])
    return result[:6]


def _remove_terms(text: str, terms: List[str]) -> str:
    updated = text
    for term in terms:
        if not term:
            continue
        updated = updated.replace(term, "").replace(term.lower(), "").replace(
            term.upper(), ""
        )
    return " ".join(updated.split())


def refine(product: dict, output: dict) -> dict:
    updated = dict(output)

    bloco_base = updated.get("blocos") or {}
    if not bloco_base:
        bloco_base = {
            "headline": updated.get("titulo", ""),
            "abertura": "Para homens 30+ que buscam versatilidade e qualidade discreta.",
            "beneficios": "Tecido e modelagem que equilibram conforto e durabilidade.",
            "autoridade": "Acabamento consistente e controle de qualidade.",
            "uso": "Ideal para uso diario e combinacoes inteligentes.",
            "risco": "Tabela de medidas clara e cuidados de lavagem definidos.",
        }

    updated["blocos"] = bloco_base
    updated["descricao"] = "\n\n".join(
        [value for value in bloco_base.values() if value]
    )

    updated["titulo"] = _fit_length(
        updated.get("titulo", ""), 55, 70, "premium masculino"
    )
    updated["subtitulo"] = _fit_length(
        updated.get("subtitulo", ""), 90, 130, "qualidade e versatilidade"
    )
    updated["descricao"] = _fit_length(
        updated.get("descricao", ""), 600, 900, "Qualidade e durabilidade para o dia a dia."
    )

    attributes = updated.get("atributos_normalizados", {})
    extras = [
        f"Tecido {attributes.get('tecido')}".strip(),
        f"Modelagem {attributes.get('modelagem')}".strip(),
        f"Cores: {', '.join(attributes.get('cores', []))}".strip(),
        f"Tamanhos: {', '.join(attributes.get('tamanhos', []))}".strip(),
    ]
    updated["bullet_points"] = _ensure_bullets(updated.get("bullet_points", []), extras)

    seo = dict(updated.get("seo", {}))
    seo["meta_title"] = _fit_length(seo.get("meta_title", updated["titulo"]), 10, 60, "")
    seo["meta_description"] = _fit_length(
        seo.get("meta_description", updated["subtitulo"]),
        140,
        160,
        "premium e duravel",
    )
    updated["seo"] = seo

    guidelines = product.get("guidelines_marca") or {}
    restricoes = product.get("restricoes_legais") or {}
    termos = (guidelines.get("termos_proibidos") or []) + (
        restricoes.get("claims_proibidos") or []
    )
    if termos:
        updated["titulo"] = _remove_terms(updated.get("titulo", ""), termos)
        updated["subtitulo"] = _remove_terms(updated.get("subtitulo", ""), termos)
        updated["descricao"] = _remove_terms(updated.get("descricao", ""), termos)
        updated["bullet_points"] = [
            _remove_terms(bp, termos) for bp in updated.get("bullet_points", [])
        ]

    return updated
