import re
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Tuple


REQUIRED_FIELDS = ["sku", "nome_produto", "categoria", "preco", "imagens"]


def _length(value: str) -> int:
    return len(value or "")


def _contains_terms(text: str, terms: List[str]) -> List[str]:
    found = []
    lower = (text or "").lower()
    for term in terms:
        if term.lower() in lower:
            found.append(term)
    return found


def _gather_text(output: dict) -> str:
    parts = [
        output.get("titulo", ""),
        output.get("subtitulo", ""),
        output.get("descricao", ""),
        " ".join(output.get("bullet_points", [])),
    ]
    return " ".join(parts)


def _check_required_fields(product: dict) -> Tuple[bool, str]:
    missing = [f for f in REQUIRED_FIELDS if not product.get(f)]
    if missing:
        return False, f"Missing fields: {', '.join(missing)}"
    return True, "OK"


def _check_lengths(output: dict) -> Tuple[bool, str]:
    title_ok = 55 <= _length(output.get("titulo")) <= 70
    subtitle_ok = 90 <= _length(output.get("subtitulo")) <= 130
    desc_ok = 600 <= _length(output.get("descricao")) <= 900
    if title_ok and subtitle_ok and desc_ok:
        return True, "OK"
    return False, (
        f"Lengths - titulo:{_length(output.get('titulo'))} "
        f"subtitulo:{_length(output.get('subtitulo'))} "
        f"descricao:{_length(output.get('descricao'))}"
    )


def _check_seo(output: dict) -> Tuple[bool, str]:
    seo = output.get("seo", {})
    title_len = _length(seo.get("meta_title"))
    desc_len = _length(seo.get("meta_description"))
    title_ok = title_len <= 60
    desc_ok = 140 <= desc_len <= 160
    if title_ok and desc_ok:
        return True, "OK"
    return False, f"meta_title:{title_len} meta_description:{desc_len}"


def _check_images(product: dict) -> Tuple[bool, str]:
    images = product.get("imagens") or []
    if len(images) >= 3:
        return True, "OK"
    return False, f"Only {len(images)} images"


def _check_price(product: dict) -> Tuple[bool, str]:
    price = product.get("preco")
    if not isinstance(price, (int, float)) or price <= 0:
        return False, "Invalid price"
    promo = product.get("promocao")
    if promo:
        promo_price = promo.get("preco_promocional")
        if not isinstance(promo_price, (int, float)) or promo_price >= price:
            return False, "Invalid promocao.preco_promocional"
        if not promo.get("validade"):
            return False, "Missing promocao.validade"
    return True, "OK"


def _check_padronizacao(product: dict, output: dict) -> Tuple[str, str]:
    rules = product.get("regras_categoria") or {}
    tamanhos_validos = rules.get("tamanhos_validos")
    cores_validas = rules.get("cores_validas")

    if not tamanhos_validos and not cores_validas:
        return "skip", "No rules provided"

    invalid = []
    normalized = output.get("atributos_normalizados", {})
    if tamanhos_validos:
        for t in normalized.get("tamanhos", []):
            if t not in tamanhos_validos:
                invalid.append(f"tamanho:{t}")
    if cores_validas:
        for c in normalized.get("cores", []):
            if c not in cores_validas:
                invalid.append(f"cor:{c}")

    if invalid:
        return "fail", ", ".join(invalid)
    return "pass", "OK"


def _check_brand(product: dict, output: dict) -> Tuple[str, str]:
    guidelines = product.get("guidelines_marca") or {}
    termos_proibidos = guidelines.get("termos_proibidos") or []
    if not termos_proibidos:
        return "skip", "No termos_proibidos provided"
    text = _gather_text(output)
    found = _contains_terms(text, termos_proibidos)
    if found:
        return "fail", f"Prohibited terms: {', '.join(found)}"
    return "pass", "OK"


def _check_legal(product: dict, output: dict) -> Tuple[str, str]:
    restricoes = product.get("restricoes_legais") or {}
    claims_proibidos = restricoes.get("claims_proibidos") or []
    if not claims_proibidos:
        return "skip", "No claims_proibidos provided"
    text = _gather_text(output)
    found = _contains_terms(text, claims_proibidos)
    if found:
        return "fail", f"Claims proibidos: {', '.join(found)}"
    return "pass", "OK"


def _check_qualidade(output: dict) -> Tuple[bool, str]:
    text = output.get("descricao", "")
    if "  " in text:
        return False, "Double spaces found"
    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    if len(sentences) < 3:
        return False, "Few sentences"
    return True, "OK"


def _check_structure(output: dict) -> Tuple[bool, str]:
    blocos = output.get("blocos") or {}
    required = ["headline", "abertura", "beneficios", "autoridade", "uso", "risco"]
    missing = [k for k in required if not (blocos.get(k) or "").strip()]
    if missing:
        return False, f"Missing blocks: {', '.join(missing)}"
    return True, "OK"


def _check_bk_confidence(output: dict) -> Tuple[bool, str]:
    bk_context = output.get("bk_context") or {}
    confidence = bk_context.get("confidence_score", 0.0)
    if confidence >= 0.6:
        return True, f"confidence_score:{confidence}"
    return False, f"confidence_score:{confidence}"


def _score_area(status: str, weight: int) -> int:
    if status == "pass":
        return weight
    if status == "skip":
        return weight
    return 0


def audit(product: dict, output: dict) -> Dict[str, object]:
    results: List[dict] = []

    req_ok, req_ev = _check_required_fields(product)
    results.append(
        {
            "area": "Dados obrigatorios",
            "regra": "SKU, nome, categoria, preco, imagens presentes",
            "severidade": "Alta",
            "status": "pass" if req_ok else "fail",
            "evidencia": req_ev,
        }
    )

    pad_status, pad_ev = _check_padronizacao(product, output)
    results.append(
        {
            "area": "Padronizacao",
            "regra": "Tamanhos e cores seguem dicionario",
            "severidade": "Media",
            "status": pad_status,
            "evidencia": pad_ev,
        }
    )

    len_ok, len_ev = _check_lengths(output)
    results.append(
        {
            "area": "Conteudo",
            "regra": "Titulo 55-70, subtitulo 90-130, descricao 600-900",
            "severidade": "Media",
            "status": "pass" if len_ok else "fail",
            "evidencia": len_ev,
        }
    )

    brand_status, brand_ev = _check_brand(product, output)
    results.append(
        {
            "area": "Marca",
            "regra": "Tom de voz e termos proibidos respeitados",
            "severidade": "Alta",
            "status": brand_status,
            "evidencia": brand_ev,
        }
    )

    legal_status, legal_ev = _check_legal(product, output)
    results.append(
        {
            "area": "Legal",
            "regra": "Sem claims proibidos",
            "severidade": "Alta",
            "status": legal_status,
            "evidencia": legal_ev,
        }
    )

    seo_ok, seo_ev = _check_seo(output)
    results.append(
        {
            "area": "SEO",
            "regra": "Meta title <= 60, meta description 140-160",
            "severidade": "Baixa",
            "status": "pass" if seo_ok else "fail",
            "evidencia": seo_ev,
        }
    )

    img_ok, img_ev = _check_images(product)
    results.append(
        {
            "area": "Imagens",
            "regra": "Min 3 imagens, resolucao minima",
            "severidade": "Media",
            "status": "pass" if img_ok else "fail",
            "evidencia": img_ev,
        }
    )

    price_ok, price_ev = _check_price(product)
    results.append(
        {
            "area": "Preco/Promocao",
            "regra": "Preco valido, promocao consistente",
            "severidade": "Media",
            "status": "pass" if price_ok else "fail",
            "evidencia": price_ev,
        }
    )

    results.append(
        {
            "area": "Duplicidade",
            "regra": "Nao duplicar nome + marca + atributos-chave",
            "severidade": "Alta",
            "status": "skip",
            "evidencia": "No similarity index",
        }
    )

    qual_ok, qual_ev = _check_qualidade(output)
    results.append(
        {
            "area": "Qualidade editorial",
            "regra": "Ortografia e fluidez",
            "severidade": "Baixa",
            "status": "pass" if qual_ok else "fail",
            "evidencia": qual_ev,
        }
    )

    struct_ok, struct_ev = _check_structure(output)
    results.append(
        {
            "area": "Estrutura cadastro",
            "regra": "Blocos obrigatorios presentes",
            "severidade": "Media",
            "status": "pass" if struct_ok else "fail",
            "evidencia": struct_ev,
        }
    )

    bk_ok, bk_ev = _check_bk_confidence(output)
    results.append(
        {
            "area": "BK confianca",
            "regra": "confidence_score >= 0.6",
            "severidade": "Media",
            "status": "pass" if bk_ok else "fail",
            "evidencia": bk_ev,
        }
    )

    weights = {
        "Dados obrigatorios": 25,
        "Conteudo": 25,
        "Marca": 20,
        "Legal": 20,
        "SEO": 10,
        "Imagens": 10,
        "Consistencia atributos": 10,
    }

    score = 0
    score += _score_area("pass" if req_ok else "fail", weights["Dados obrigatorios"])
    score += _score_area("pass" if len_ok else "fail", weights["Conteudo"])
    score += _score_area(brand_status, weights["Marca"])
    score += _score_area(legal_status, weights["Legal"])
    score += _score_area("pass" if seo_ok else "fail", weights["SEO"])
    score += _score_area("pass" if img_ok else "fail", weights["Imagens"])
    score += _score_area(pad_status, weights["Consistencia atributos"])
    if not bk_ok:
        score -= 10
    if not struct_ok:
        score -= 10
    if score < 0:
        score = 0
    if score > 100:
        score = 100

    failed_high = [
        r for r in results if r["severidade"] == "Alta" and r["status"] == "fail"
    ]
    resultado = "reprovado" if failed_high else "aprovado"
    motivos = [f"{r['area']}: {r['evidencia']}" for r in results if r["status"] == "fail"]

    auditoria = {
        "audit_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "usuario": product.get("usuario", "system"),
        "versao_pipeline": product.get("versao_pipeline", "1.0.0"),
        "resultado": resultado,
        "motivos_reprovacao": motivos,
        "detalhes": results,
    }

    return {
        "score_qualidade": score,
        "auditoria": auditoria,
    }
