import argparse
import html as html_lib
import os
import re
from typing import List, Tuple

OCR_ASSET_ALLOWLIST = [
    "feature",
    "benefit",
    "fabric",
    "material",
    "care",
    "micron",
    "wool",
]

OCR_ASSET_DENYLIST = [
    "gallery",
    "thumbnail",
    "thumb",
    "model",
    "lifestyle",
    "logo",
    "testimonial",
    "review",
    "menu",
]


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


def _clean_text(text: str) -> str:
    text = html_lib.unescape(text or "")
    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _strip_html_tags(text: str) -> str:
    text = re.sub(r"(?is)<script.*?>.*?</script>", " ", text)
    text = re.sub(r"(?is)<style.*?>.*?</style>", " ", text)
    text = re.sub(r"(?is)<svg.*?>.*?</svg>", " ", text)
    text = re.sub(r"(?is)<noscript.*?>.*?</noscript>", " ", text)
    text = re.sub(r"(?is)<[^>]+>", " ", text)
    return _clean_text(text)


def _extract_html_generic(text: str) -> str:
    try:
        from bs4 import BeautifulSoup  # type: ignore
    except Exception:
        return _strip_html_tags(text)

    soup = BeautifulSoup(text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
        tag.decompose()

    # Prefer main content areas when available.
    preferred = []
    for selector in [
        "main",
        "article",
        "section",
        "[id*=product]",
        "[class*=product]",
        "[id*=description]",
        "[class*=description]",
        "[id*=details]",
        "[class*=details]",
        "[id*=fabric]",
        "[class*=fabric]",
    ]:
        preferred.extend(soup.select(selector))

    if preferred:
        chunks = [el.get_text(" ", strip=True) for el in preferred]
        return " ".join(chunks)

    body = soup.body or soup
    return body.get_text(" ", strip=True)


def _extract_between_markers(text: str, start_marker: str, end_markers: List[str]) -> str:
    idx = text.lower().find(start_marker.lower())
    if idx == -1:
        return ""
    end_positions = []
    for marker in end_markers:
        pos = text.lower().find(marker.lower(), idx + len(start_marker))
        if pos != -1:
            end_positions.append(pos)
    end = min(end_positions) if end_positions else len(text)
    return text[idx:end]


def _extract_unboundmerino_features(text: str) -> List[str]:
    items = re.findall(
        r'(?is)<li class="product-features__list-item".*?<span>(.*?)</span>',
        text,
    )
    cleaned = []
    for item in items:
        value = _strip_html_tags(item)
        if value and value not in cleaned:
            cleaned.append(value)
    return cleaned


def _extract_unboundmerino_tab(text: str, tab_class_fragment: str) -> str:
    chunk = _extract_between_markers(
        text,
        f'<div class="product-tab {tab_class_fragment}',
        ['<div class="product-tab ', '<div id="shopify-section-'],
    )
    if not chunk:
        return ""
    if "external-video__container" in chunk:
        chunk = chunk.split("external-video__container", 1)[0]

    items = []
    for raw_item in re.findall(r"(?is)<li\b[^>]*>(.*?)</li>", chunk):
        value = _strip_html_tags(raw_item)
        value = re.sub(r"(?i)\bsee measurements\b", "See Measurements", value)
        value = _clean_text(value)
        if value and value not in items:
            items.append(value)

    if tab_class_fragment == "tab-the-details":
        micron_values = []
        for raw_value in re.findall(
            r'(?is)<span class="micron-chart__(?:start|end|progress-value)".*?>(.*?)</span>',
            chunk,
        ):
            value = _clean_text(_strip_html_tags(raw_value))
            if value and value not in micron_values:
                micron_values.append(value)
        if micron_values:
            items.append("Micron chart: " + " / ".join(micron_values))

    return " ".join(items)


def _extract_unboundmerino_description(text: str) -> str:
    match = re.search(
        r'(?is)<div class="product-description js-product-description">\s*(.*?)\s*</div>',
        text,
    )
    if not match:
        return ""
    return _strip_html_tags(match.group(1))


def _extract_html_unboundmerino(text: str) -> str:
    blocks = []

    description = _extract_unboundmerino_description(text)
    if description:
        blocks.append(f"Description: {description}")

    features = _extract_unboundmerino_features(text)
    if features:
        blocks.append("Benefits/Features: " + "; ".join(features))

    tab_map = [
        ("The Fit", "tab-the-fit"),
        ("Fabric and Details", "tab-the-details"),
        ("Care Instructions", "tab-care"),
    ]
    for label, tab_class in tab_map:
        content = _extract_unboundmerino_tab(text, tab_class)
        if not content:
            continue
        # Remove repeated tab labels and common UI leftovers after tag stripping.
        content = re.sub(rf"(?i)^{re.escape(label)}\s*", "", content).strip()
        content = re.sub(r"(?i)\bwatch video\b", " ", content)
        content = re.sub(r"(?i)\blearn more\b", " ", content)
        content = _clean_text(content)
        if content:
            blocks.append(f"{label}: {content}")

    combined = "\n".join(blocks)
    # If selectors fail or yield weak output, degrade gracefully to generic extraction.
    if len(combined) < 120:
        return ""
    return combined


def _extract_html(text: str, source_path: str = "") -> str:
    source_hint = f"{source_path} {text[:20000]}".lower()
    if "unboundmerino" in source_hint or "unbound merino" in source_hint:
        parsed = _extract_html_unboundmerino(text)
        if parsed:
            return parsed
    return _extract_html_generic(text)


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


def extract_file(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext in [".txt", ".md"]:
        return _read_text(path)
    if ext in [".html", ".htm"]:
        return _extract_html(_read_text(path), source_path=path)
    if ext == ".pdf":
        return _extract_pdf(path)
    return ""


def _list_files(input_path: str, include_assets: bool = False) -> List[str]:
    if os.path.isdir(input_path):
        collected = []
        has_main_html = any(
            name.lower().endswith(".html") for name in os.listdir(input_path)
        )
        for root, _dirs, files in os.walk(input_path):
            in_assets_dir = os.path.basename(root).lower().endswith("_files")
            if in_assets_dir and not include_assets:
                continue
            for name in files:
                lower = name.lower()
                if lower.startswith("saved_resource"):
                    continue
                if in_assets_dir and has_main_html and lower.endswith((".html", ".htm")):
                    continue
                if not include_assets and lower.endswith((".png", ".jpg", ".jpeg", ".webp")):
                    continue
                collected.append(os.path.join(root, name))
        return collected
    return [input_path]


def _extract_image_ocr(
    path: str, lang: str = "eng", tesseract_cmd: str | None = None
) -> str:
    try:
        from PIL import Image  # type: ignore
        import pytesseract  # type: ignore
    except Exception:
        return ""

    try:
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        image = Image.open(path)
        return pytesseract.image_to_string(image, lang=lang)
    except Exception:
        return ""


def _is_low_value_text(text: str) -> bool:
    clean = " ".join((text or "").split())
    if not clean:
        return True
    if len(clean) < 12:
        return True
    alnum = [ch for ch in clean if ch.isalnum()]
    if len(alnum) < 6:
        return True
    return False


def _is_image_file(path: str) -> bool:
    return path.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))


def _should_ocr_asset(path: str) -> bool:
    lower = path.lower().replace("\\", "/")
    filename = os.path.basename(lower)

    has_allow = any(token in filename or token in lower for token in OCR_ASSET_ALLOWLIST)
    has_deny = any(token in filename or token in lower for token in OCR_ASSET_DENYLIST)

    # Allowlist wins when an asset name strongly hints technical content
    # (e.g., product-fabric-1.jpg, product-care-1.jpg).
    if has_allow:
        return True
    if has_deny:
        return False

    # Last-resort exclusions for common low-value ecommerce assets.
    if any(token in filename for token in ["_40x", "_80x", "_160x", "small", "medium"]):
        return False

    return False


def _write_text(out_dir: str, src_path: str, text: str) -> str:
    base = os.path.splitext(os.path.basename(src_path))[0]
    target = os.path.join(out_dir, f"{base}.txt")
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(text)
    return target


def run_extract(
    input_path: str,
    out_dir: str,
    use_ocr: bool = False,
    ocr_lang: str = "eng",
    tesseract_cmd: str | None = None,
) -> List[Tuple[str, str]]:
    os.makedirs(out_dir, exist_ok=True)
    outputs = []
    ocr_assets_eligible = 0
    ocr_assets_discarded = 0
    for path in _list_files(input_path, include_assets=use_ocr):
        content = extract_file(path) or ""
        if use_ocr and not content.strip():
            if _is_image_file(path):
                if not _should_ocr_asset(path):
                    ocr_assets_discarded += 1
                    continue
                ocr_assets_eligible += 1
                content = _extract_image_ocr(
                    path, lang=ocr_lang, tesseract_cmd=tesseract_cmd
                ) or ""
        if not content.strip():
            continue
        if _is_low_value_text(content):
            continue
        target = _write_text(out_dir, path, content)
        outputs.append((path, target))

    if use_ocr:
        print(
            f"OCR assets: elegiveis={ocr_assets_eligible} descartados={ocr_assets_discarded}"
        )
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract RAW files to text")
    parser.add_argument("--input", required=True, help="Path to raw files or folder")
    parser.add_argument("--out", required=True, help="Output folder for extracted text")
    parser.add_argument("--ocr", action="store_true", help="Enable OCR for images")
    parser.add_argument("--ocr-lang", default="eng", help="OCR language (tesseract)")
    parser.add_argument(
        "--tesseract-cmd",
        help="Full path to tesseract.exe (use when tesseract is not in PATH)",
    )
    args = parser.parse_args()

    outputs = run_extract(
        args.input,
        args.out,
        use_ocr=args.ocr,
        ocr_lang=args.ocr_lang,
        tesseract_cmd=args.tesseract_cmd,
    )
    for src, dest in outputs:
        print(f"{src} -> {dest}")


if __name__ == "__main__":
    main()
