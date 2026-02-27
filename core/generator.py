import re
from typing import Dict, List


def _slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text).strip("-")
    text = re.sub(r"-{2,}", "-", text)
    return text


def _normalize_list(values: List[str]) -> List[str]:
    normalized = []
    for value in values or []:
        clean = " ".join(str(value).strip().split())
        if not clean:
            continue
        normalized.append(clean)
    return normalized


def _title_case(value: str) -> str:
    return " ".join(word.capitalize() for word in value.split())


def _unique(values: List[str]) -> List[str]:
    seen = set()
    result = []
    for value in values:
        key = value.lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(value)
    return result


def _paragraphs_from_blocks(blocks: dict) -> str:
    order = [
        "headline",
        "abertura",
        "beneficios",
        "autoridade",
        "uso",
        "risco",
    ]
    parts = []
    for key in order:
        value = blocks.get(key, "").strip()
        if value:
            parts.append(value)
    return "\n\n".join(parts)


def generate(product: dict, _bk_data: dict, bk_context: dict | None = None) -> dict:
    nome = product.get("nome_produto", "").strip()
    marca = product.get("marca", "").strip()
    categoria = product.get("categoria", "").strip()
    subcategoria = product.get("subcategoria", "").strip()
    tecido = product.get("tecido", "").strip()
    composicao = product.get("composicao", "").strip()
    modelagem = product.get("modelagem", "").strip()
    acabamento = product.get("acabamento", "").strip()
    colecao = product.get("colecao", "").strip()
    cores = _unique([_title_case(c) for c in _normalize_list(product.get("cores", []))])
    tamanhos = _unique([t.upper() for t in _normalize_list(product.get("tamanhos", []))])

    atributos_normalizados = {
        "categoria": categoria,
        "subcategoria": subcategoria,
        "tecido": tecido,
        "composicao": composicao,
        "modelagem": modelagem,
        "acabamento": acabamento,
        "colecao": colecao,
        "cores": cores,
        "tamanhos": tamanhos,
    }

    tags = _unique(
        [
            categoria,
            subcategoria,
            tecido,
            modelagem,
            acabamento,
            colecao,
            *cores,
        ]
    )
    tags = [t.lower().replace(" ", "-") for t in tags if t]

    base_title = " ".join(part for part in [categoria, nome, marca] if part)
    if len(base_title) < 55:
        base_title = f"{base_title} premium masculino"
    title = base_title[:70].strip()

    subtitle_parts = [
        f"{tecido} {modelagem}".strip(),
        f"acabamento {acabamento}".strip() if acabamento else "",
        f"colecao {colecao}".strip() if colecao else "",
        "ideal para uso versatil e duradouro",
    ]
    subtitle = ". ".join([p for p in subtitle_parts if p])

    headline = title
    abertura = (
        "Para homens 30+ que buscam uma peca versatil, com presenca discreta "
        "e qualidade perceptivel no uso diario."
    )
    beneficios = " ".join(
        [
            f"Tecido {tecido} com toque superior e maior estabilidade no uso.".strip(),
            f"Modelagem {modelagem} garante caimento equilibrado e conforto continuo.".strip(),
            f"Composicao {composicao} favorece respirabilidade e durabilidade.".strip()
            if composicao
            else "Construcao que preserva maciez e resistencia ao uso frequente.",
        ]
    )
    autoridade = " ".join(
        [
            f"Acabamento {acabamento} eleva a percepcao de qualidade.".strip()
            if acabamento
            else "Acabamento limpo e consistente reforca a proposta premium.",
            "Controle de qualidade focado em costuras e estabilidade do tecido.",
        ]
    )
    uso = (
        "Funciona em ambientes de trabalho casual, encontros e rotina urbana. "
        "Combina com jeans premium, alfaiataria casual e sobreposicoes leves."
    )
    risco = (
        "Tabela de medidas clara, orientacao de tamanho e cuidados de lavagem "
        "reduzem risco de troca e preservam a peca."
    )
    blocos = {
        "headline": headline,
        "abertura": abertura,
        "beneficios": beneficios,
        "autoridade": autoridade,
        "uso": uso,
        "risco": risco,
    }

    descricao = _paragraphs_from_blocks(blocos)

    bullet_points = [
        f"Tecido {tecido} com toque premium".strip(),
        f"Modelagem {modelagem} para bom caimento".strip(),
        f"Cores: {', '.join(cores)}".strip(),
        f"Tamanhos: {', '.join(tamanhos)}".strip(),
        "Versatil para diferentes ocasioes",
    ]
    bullet_points = [b for b in bullet_points if len(b) > 3]

    seo = {
        "meta_title": title[:60],
        "meta_description": subtitle[:160],
        "slug": _slugify(" ".join([categoria, nome, marca])),
    }

    return {
        "titulo": title,
        "subtitulo": subtitle,
        "descricao": descricao,
        "bullet_points": bullet_points[:6],
        "blocos": blocos,
        "atributos_normalizados": atributos_normalizados,
        "tags": tags,
        "seo": seo,
        "bk_context": bk_context or {},
    }
