import argparse
import datetime as dt
import os
import re
import unicodedata
from typing import Dict, List, Tuple


KEYWORDS = {
    "tecidos": [
        "algodao",
        "linho",
        "wool",
        "sarja",
        "oxford",
        "malha",
        "denim",
        "twill",
        "viscose",
        "poliester",
        "nylon",
    ],
    "modelagem": [
        "slim",
        "regular",
        "oversized",
        "alfaiataria",
        "caimento",
        "reta",
        "ajustada",
        "modelagem",
    ],
    "tecnologias": [
        "repelencia",
        "dry",
        "termico",
        "stretch",
        "anti-odor",
        "uv",
        "waterproof",
        "anti-manchas",
        "antibacteriano",
    ],
}


def _read_text(path: str) -> str:
    for encoding in ["utf-8", "latin-1"]:
        try:
            with open(path, "r", encoding=encoding) as handle:
                return handle.read()
        except UnicodeDecodeError:
            continue
        except OSError:
            return ""
    return ""


def _normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.replace("\r", " ").replace("\n", " ")
    text = re.sub(r"\s+", " ", text).strip()
    text = text.lower()
    replacements = {
        "algodao cru": "algodao",
        "poliéster": "poliester",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    return text


def _extract_useful_blocks(text: str) -> str:
    keep_markers = [
        "fabric",
        "details",
        "materials",
        "material",
        "care",
        "fit",
        "features",
        "benefits",
        "temperature",
        "odor",
        "anti-odor",
        "breath",
        "breathable",
        "moisture",
        "merino",
        "wool",
        "fiber",
        "micron",
        "gsm",
        "gramatura",
    ]
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    blocks = []
    current = []
    for line in lines:
        if any(marker in line.lower() for marker in keep_markers):
            current.append(line)
        else:
            if current:
                blocks.append(" ".join(current))
                current = []
    if current:
        blocks.append(" ".join(current))
    if not blocks:
        return text
    return " ".join(blocks)


def _filter_noise(text: str) -> str:
    noise_markers = [
        "cart",
        "reviews",
        "shipping",
        "returns",
        "exchange",
        "customer photos",
        "write a review",
        "add to cart",
        "bundle",
        "gift card",
        "privacy policy",
        "terms of service",
        "newsletter",
        "subscribe",
        "checkout",
        "help center",
    ]
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    cleaned = []
    for line in lines:
        lower = line.lower()
        if any(marker in lower for marker in noise_markers):
            continue
        cleaned.append(line)
    return " ".join(cleaned)


def _extract_between_anchors(text: str) -> str:
    anchors_start_priority = [
        "fabric and details",
        "fabric & details",
        "fabric details",
        "description",
        "features",
        "benefits",
        "materials",
    ]
    anchors_end = [
        "size guide",
        "reviews",
        "shipping",
        "returns",
    ]
    lower = text.lower()
    start_idx = -1
    for anchor in anchors_start_priority:
        idx = lower.find(anchor)
        if idx != -1:
            start_idx = idx
            break
    if start_idx == -1:
        return text
    end_candidates = [lower.find(a, start_idx + 10) for a in anchors_end if lower.find(a, start_idx + 10) != -1]
    end_idx = min(end_candidates) if end_candidates else len(text)
    return text[start_idx:end_idx].strip()


def _filter_sentences_useful(text: str) -> str:
    keep_markers = [
        "fabric",
        "details",
        "materials",
        "material",
        "care",
        "fit",
        "features",
        "benefits",
        "temperature",
        "odor",
        "anti-odor",
        "breath",
        "breathable",
        "moisture",
        "merino",
        "wool",
        "fiber",
        "micron",
        "gsm",
        "gramatura",
    ]
    noise_markers = [
        "cart",
        "reviews",
        "shipping",
        "returns",
        "exchange",
        "customer photos",
        "write a review",
        "add to cart",
        "bundle",
        "gift card",
        "privacy policy",
        "terms of service",
        "newsletter",
        "subscribe",
        "checkout",
        "help center",
        "shop ",
        "size guide",
        "sold out",
    ]
    sentences = _split_sentences(text)
    kept = []
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        lower = sentence.lower()
        if any(marker in lower for marker in noise_markers):
            continue
        if any(marker in lower for marker in keep_markers):
            kept.append(sentence)
    return ". ".join(kept).strip()


def _split_sentences(text: str) -> List[str]:
    # Avoid splitting decimal values like "17.5" while still breaking prose.
    protected = re.sub(r"(?<=\d)\.(?=\d)", "__DECIMAL_DOT__", text)
    sentences = re.split(r"[!?]+|(?<!\.)\.(?!\.)", protected)
    restored = [s.replace("__DECIMAL_DOT__", ".").strip() for s in sentences]
    return [s for s in restored if s]


def _build_summary(text: str) -> List[str]:
    sentences = _split_sentences(text)
    if len(sentences) >= 2:
        return sentences[:3]
    if not sentences:
        return []

    base = sentences[0]
    chunks = []

    # Split compact technical strings with known labels, e.g.:
    # "fabric and details: ... fiber micron: ... micron chart: ..."
    label_pattern = (
        r"\b(?:description|benefits(?:/features)?|the fit|fabric and details|"
        r"care instructions|fiber micron|micron chart):"
    )
    for part in re.split(rf"\s+(?={label_pattern})", base):
        clean = part.strip(" -.;")
        if clean:
            chunks.append(clean)

    if len(chunks) < 2:
        alt = []
        for part in re.split(r"\s*;\s*|\s+\|\s+", base):
            clean = part.strip(" -.;")
            if clean:
                alt.append(clean)
        chunks = alt or chunks

    if len(chunks) >= 2:
        return chunks[:3]
    return [base]


def _keywords_found(text: str) -> List[str]:
    found = []
    for group in KEYWORDS.values():
        for key in group:
            if key in text and key not in found:
                found.append(key)
    return found


def _extract_technical_signals(text: str) -> List[str]:
    patterns = [
        r"\b\d{2,3}\s?gsm\b",
        r"\b\d{1,3}(?:[.,]\d+)?\s?(?:micron|microns|um|μm)\b",
        r"\b100%\s+[a-z ]{3,40}\b",
        r"\b(?:merino wool|woolmark|oeko-tex|anti-wrinkle|moisture-wicking)\b",
    ]
    found: List[str] = []
    lower = text.lower()
    for pattern in patterns:
        for match in re.findall(pattern, lower, flags=re.IGNORECASE):
            signal = " ".join(str(match).split())
            if signal and signal not in found:
                found.append(signal)
    return found[:10]


def _score_category(text: str, filename: str) -> Tuple[str, int]:
    filename = filename.lower()
    for category in KEYWORDS:
        if category in filename:
            return category, 100
        if category[:-1] in filename:
            return category, 90

    scores: Dict[str, int] = {}
    for category, keywords in KEYWORDS.items():
        scores[category] = sum(text.count(k) for k in keywords)
    best = max(scores.values()) if scores else 0
    winners = [k for k, v in scores.items() if v == best and v > 0]
    if len(winners) == 1:
        return winners[0], best
    return "_pendente", best


def _title_from_filename(path: str) -> str:
    base = os.path.splitext(os.path.basename(path))[0]
    words = re.split(r"[_\\-]+", base)
    return " ".join(w.capitalize() for w in words if w)


def _slugify(text: str) -> str:
    text = re.sub(r"[^a-z0-9\s-]", "", text.lower())
    text = re.sub(r"\s+", "-", text).strip("-")
    return text


def _render_markdown(
    title: str,
    category: str,
    source: str,
    date_value: str,
    resumo: List[str],
    detalhes: str,
    termos: List[str],
    tags: List[str],
    sinais_tecnicos: List[str],
) -> str:
    resumo_lines = "\n".join([f"- {item}" for item in resumo]) or "-"
    termos_line = "- " + ", ".join(termos) if termos else "-"
    tags_line = "- " + " ".join(tags) if tags else "-"
    sinais_line = "\n".join([f"- {s}" for s in sinais_tecnicos]) if sinais_tecnicos else "-"

    return (
        "# TEMPLATE -- Base de Conhecimento\n\n"
        "## Titulo\n"
        f"{title}\n\n"
        "## Categoria\n"
        f"- {category}\n\n"
        "## Fonte\n"
        f"- {source}\n\n"
        "## Data\n"
        f"- {date_value}\n\n"
        "## Resumo\n"
        f"{resumo_lines}\n\n"
        "## Detalhes\n"
        f"- {detalhes}\n\n"
        "## Sinais Tecnicos Extraidos\n"
        f"{sinais_line}\n\n"
        "## Aplicacao no Cadastro\n"
        "- Usar para descrever caracteristicas relevantes no cadastro premium.\n\n"
        "## Termos e Sinonimos\n"
        f"{termos_line}\n\n"
        "## Regras e Restricoes\n"
        "- Evitar claims absolutos nao suportados pela fonte.\n\n"
        "## Tags\n"
        f"{tags_line}\n"
    )


def _write_markdown(base_path: str, category: str, title: str, markdown: str) -> str:
    slug = _slugify(title)
    name = f"{dt.datetime.now().strftime('%Y%m%d-%H%M%S')}-{slug}.md"
    target_dir = os.path.join(base_path, category)
    os.makedirs(target_dir, exist_ok=True)
    path = os.path.join(target_dir, name)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(markdown)
    return path


def run_normalize(input_path: str, out_base: str, source: str) -> List[str]:
    outputs = []
    if not os.path.isdir(input_path):
        raise FileNotFoundError(input_path)

    for root, _dirs, files in os.walk(input_path):
        for name in files:
            if not name.lower().endswith(".txt"):
                continue
            if name.startswith("_"):
                continue
            path = os.path.join(root, name)
            raw = _read_text(path)
            if not raw.strip():
                continue
            normalized = _normalize_text(raw)
            normalized = _extract_between_anchors(normalized)
            normalized = _filter_sentences_useful(normalized)
            if not normalized:
                normalized = _filter_noise(_normalize_text(raw))
                normalized = _extract_useful_blocks(normalized)
            if len(normalized) < 60:
                continue
            title = _title_from_filename(path)
            category, _score = _score_category(normalized, path)
            resumo = _build_summary(normalized)
            termos = _keywords_found(normalized)
            sinais_tecnicos = _extract_technical_signals(normalized)
            tags = [f"#{category}"] + [f"#{t}" for t in termos[:5]]
            markdown = _render_markdown(
                title=title,
                category=category,
                source=source,
                date_value=dt.date.today().isoformat(),
                resumo=resumo,
                detalhes=normalized,
                termos=termos,
                tags=tags,
                sinais_tecnicos=sinais_tecnicos,
            )
            outputs.append(_write_markdown(out_base, category, title, markdown))

    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize extracted text to markdown")
    parser.add_argument("--input", required=True, help="Path to extracted txt folder")
    parser.add_argument("--out", required=True, help="Base conhecimento path")
    parser.add_argument("--source", default="manual", help="Fonte do conteudo")
    args = parser.parse_args()

    outputs = run_normalize(args.input, args.out, args.source)
    for output in outputs:
        print(output)


if __name__ == "__main__":
    main()
