import argparse
import datetime as dt
import os
import re
import shutil
import unicodedata
from typing import Dict, Iterable, List, Tuple


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
        "retao",
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


def _now_stamp() -> str:
    return dt.datetime.now().strftime("%Y%m%d-%H%M%S")


def _ensure_dirs(base_path: str) -> None:
    for name in ["_raw", "_pendente", "tecidos", "modelagem", "tecnologias"]:
        os.makedirs(os.path.join(base_path, name), exist_ok=True)


def _list_files(input_path: str) -> List[str]:
    if os.path.isdir(input_path):
        collected = []
        for root, _dirs, files in os.walk(input_path):
            for name in files:
                collected.append(os.path.join(root, name))
        return collected
    return [input_path]


def _copy_raw(path: str, raw_dir: str) -> str:
    stamp = _now_stamp()
    base = os.path.basename(path)
    target = os.path.join(raw_dir, f"{stamp}-{base}")
    shutil.copy2(path, target)
    return target


def _extract_text(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext in [".txt", ".md"]:
        return _read_text(path)
    if ext in [".html", ".htm"]:
        return _extract_html(path)
    if ext == ".pdf":
        return _extract_pdf(path)
    return ""


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


def _extract_html(path: str) -> str:
    raw = _read_text(path)
    raw = re.sub(r"(?is)<script.*?>.*?</script>", " ", raw)
    raw = re.sub(r"(?is)<style.*?>.*?</style>", " ", raw)
    raw = re.sub(r"(?is)<[^>]+>", " ", raw)
    return raw


def _extract_pdf(path: str) -> str:
    try:
        from PyPDF2 import PdfReader  # type: ignore
    except Exception:
        return ""

    try:
        reader = PdfReader(path)
    except Exception:
        return ""

    parts = []
    for page in reader.pages:
        try:
            parts.append(page.extract_text() or "")
        except Exception:
            continue
    return "\n".join(parts)


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


def _split_sentences(text: str) -> List[str]:
    sentences = re.split(r"[.!?]+", text)
    return [s.strip() for s in sentences if s.strip()]


def _build_summary(text: str) -> List[str]:
    sentences = _split_sentences(text)
    return sentences[:3] if sentences else []


def _keywords_found(text: str) -> List[str]:
    found = []
    for group in KEYWORDS.values():
        for key in group:
            if key in text and key not in found:
                found.append(key)
    return found


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
    words = re.split(r"[_\-]+", base)
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
) -> str:
    resumo_lines = "\n".join([f"- {item}" for item in resumo]) or "-"
    termos_line = "- " + ", ".join(termos) if termos else "-"
    tags_line = "- " + " ".join(tags) if tags else "-"

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
        "## Aplicacao no Cadastro\n"
        "- Usar para descrever caracteristicas relevantes no cadastro premium.\n\n"
        "## Termos e Sinonimos\n"
        f"{termos_line}\n\n"
        "## Regras e Restricoes\n"
        "- Evitar claims absolutos nao suportados pela fonte.\n\n"
        "## Tags\n"
        f"{tags_line}\n"
    )


def _write_markdown(
    base_path: str, category: str, title: str, markdown: str
) -> str:
    slug = _slugify(title)
    name = f"{_now_stamp()}-{slug}.md"
    target_dir = os.path.join(base_path, category)
    os.makedirs(target_dir, exist_ok=True)
    path = os.path.join(target_dir, name)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(markdown)
    return path


def ingest(paths: Iterable[str], out_base: str, source: str) -> List[str]:
    _ensure_dirs(out_base)
    outputs = []
    for path in paths:
        raw_path = _copy_raw(path, os.path.join(out_base, "_raw"))
        extracted = _extract_text(raw_path)
        if not extracted.strip():
            category = "_pendente"
            title = _title_from_filename(path)
            markdown = _render_markdown(
                title=title,
                category=category,
                source=source,
                date_value=dt.date.today().isoformat(),
                resumo=["Conteudo nao extraido."],
                detalhes="Extracao falhou ou arquivo vazio.",
                termos=[],
                tags=[f"#{category}"],
            )
            outputs.append(_write_markdown(out_base, category, title, markdown))
            continue

        normalized = _normalize_text(extracted)
        title = _title_from_filename(path)
        category, _score = _score_category(normalized, path)
        resumo = _build_summary(normalized)
        termos = _keywords_found(normalized)
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
        )
        outputs.append(_write_markdown(out_base, category, title, markdown))

    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description="BK ingest pipeline")
    parser.add_argument("--input", required=True, help="File or folder path")
    parser.add_argument(
        "--out",
        default=os.path.join(os.getcwd(), "base_conhecimento"),
        help="Base conhecimento path",
    )
    parser.add_argument("--source", default="manual", help="Fonte do conteudo")
    args = parser.parse_args()

    files = _list_files(args.input)
    outputs = ingest(files, args.out, args.source)
    for output in outputs:
        print(output)


if __name__ == "__main__":
    main()
