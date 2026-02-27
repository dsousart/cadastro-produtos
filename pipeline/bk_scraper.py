import argparse
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import urllib.robotparser
from html.parser import HTMLParser
from typing import Dict, Iterable, List, Optional, Set, Tuple

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from pipeline.bk_ingest import ingest


USER_AGENT = "BKIngestBot/1.0 (+https://example.local)"
DEFAULT_LIMIT_MIN = 200
DEFAULT_LIMIT_MAX = 500

INCLUDE_KEYWORDS = [
    "/men",
    "/man",
    "/masculino",
    "/homem",
    "/mens",
]
EXCLUDE_KEYWORDS = [
    "/women",
    "/female",
    "/feminino",
    "/girl",
    "/kids",
    "/infantil",
]


class LinkExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: List[str] = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        if tag != "a":
            return
        for key, value in attrs:
            if key == "href" and value:
                self.links.append(value)


def _read_config(path: str) -> Dict[str, List[str]]:
    if not os.path.isfile(path):
        raise FileNotFoundError(path)
    text = _read_text(path)
    sections: Dict[str, List[str]] = {}
    current = None
    for raw_line in text.splitlines():
        line = raw_line.strip().lstrip("\ufeff")
        if not line:
            continue
        if line.endswith(":"):
            current = line[:-1].lower()
            sections[current] = []
            continue
        if line.startswith("-") and current:
            sections[current].append(line[1:].strip())
        elif current:
            sections[current].append(line)
    return sections


def _parse_domain_rules(lines: List[str]) -> Dict[str, List[str]]:
    rules: Dict[str, List[str]] = {}
    for line in lines:
        if ":" not in line:
            continue
        domain, patterns = line.split(":", 1)
        domain = domain.strip()
        items = [p.strip() for p in patterns.split(",") if p.strip()]
        if domain and items:
            rules[domain] = items
    return rules


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


def _normalize_url(base: str, link: str) -> Optional[str]:
    if link.startswith("mailto:") or link.startswith("tel:"):
        return None
    parsed = urllib.parse.urljoin(base, link)
    parsed = parsed.split("#")[0]
    return parsed


def _is_same_domain(url: str, domain: str) -> bool:
    return urllib.parse.urlparse(url).netloc == urllib.parse.urlparse(domain).netloc


def _filter_url(url: str, include: Iterable[str], exclude: Iterable[str]) -> bool:
    lower = url.lower()
    if any(bad in lower for bad in exclude):
        return False
    if any(good in lower for good in include):
        return True
    return False


def _fetch(url: str, timeout: int = 10) -> Tuple[int, str]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        body = resp.read().decode(charset, errors="ignore")
        return resp.status, body


def _fetch_headless(url: str, timeout: int = 20) -> Tuple[int, str]:
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
    except Exception:
        return 0, ""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            resp = page.goto(url, wait_until="domcontentloaded", timeout=timeout * 1000)
            status = resp.status if resp else 200
            html = page.content()
        finally:
            browser.close()
    return status, html


def _fetch_sitemap(url: str, timeout: int = 15) -> Tuple[int, str]:
    return _fetch(url, timeout=timeout)


def _save_html(base_path: str, domain: str, url: str, html: str) -> str:
    raw_dir = os.path.join(base_path, "_raw_web")
    os.makedirs(raw_dir, exist_ok=True)
    host = urllib.parse.urlparse(domain).netloc.replace(":", "_")
    slug = re.sub(r"[^a-z0-9]+", "-", url.lower()).strip("-")
    name = f"{host}-{slug[:120]}.html"
    path = os.path.join(raw_dir, name)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(html)
    return path


def _robots_parser(domain: str) -> urllib.robotparser.RobotFileParser:
    robots_url = urllib.parse.urljoin(domain, "/robots.txt")
    parser = urllib.robotparser.RobotFileParser()
    parser.set_url(robots_url)
    try:
        parser.read()
    except Exception:
        pass
    return parser


def _parse_sitemap_urls(xml_text: str) -> List[str]:
    if not xml_text:
        return []
    return re.findall(r"<loc>(.*?)</loc>", xml_text, flags=re.IGNORECASE)


def _discover_sitemap_urls(domain: str, use_headless: bool) -> List[str]:
    candidates = [
        urllib.parse.urljoin(domain, "/sitemap.xml"),
        urllib.parse.urljoin(domain, "/sitemap_index.xml"),
    ]
    urls: List[str] = []
    for sitemap_url in candidates:
        try:
            status, xml_text = (
                _fetch_headless(sitemap_url) if use_headless else _fetch_sitemap(sitemap_url)
            )
        except Exception:
            continue
        if status >= 400 or not xml_text:
            continue
        locs = _parse_sitemap_urls(xml_text)
        for loc in locs:
            if loc.endswith(".xml") and "sitemap" in loc:
                try:
                    status_child, xml_child = _fetch_sitemap(loc)
                except Exception:
                    continue
                if status_child < 400:
                    urls.extend(_parse_sitemap_urls(xml_child))
            else:
                urls.append(loc)
    return urls


def crawl_domain(
    domain: str,
    limit: int,
    include: Iterable[str],
    exclude: Iterable[str],
    include_domain: Iterable[str],
    exclude_domain: Iterable[str],
    rate_seconds: float,
    out_base: str,
    use_headless: bool,
) -> Tuple[List[str], Dict[str, int]]:
    rp = _robots_parser(domain)
    visited: Set[str] = set()
    queue: List[str] = [domain]
    saved: List[str] = []
    stats = {
        "visited": 0,
        "saved": 0,
        "filtered": 0,
        "robots_blocked": 0,
        "http_error": 0,
        "fetch_error": 0,
    }

    while queue and len(saved) < limit:
        url = queue.pop(0)
        if url in visited:
            continue
        visited.add(url)
        stats["visited"] += 1
        if not _is_same_domain(url, domain):
            continue
        if not rp.can_fetch(USER_AGENT, url):
            stats["robots_blocked"] += 1
            continue
        merged_include = list(include) + list(include_domain)
        merged_exclude = list(exclude) + list(exclude_domain)
        if not _filter_url(url, merged_include, merged_exclude) and url != domain:
            stats["filtered"] += 1
            continue

        try:
            status, html = (
                _fetch_headless(url) if use_headless else _fetch(url)
            )
        except Exception:
            stats["fetch_error"] += 1
            continue
        if status == 0 and use_headless:
            stats["fetch_error"] += 1
            continue
        if status >= 400:
            stats["http_error"] += 1
            continue

        saved.append(_save_html(out_base, domain, url, html))
        stats["saved"] = len(saved)

        extractor = LinkExtractor()
        try:
            extractor.feed(html)
        except Exception:
            continue
        for link in extractor.links:
            normalized = _normalize_url(url, link)
            if not normalized:
                continue
            if normalized not in visited and normalized not in queue:
                queue.append(normalized)

        time.sleep(rate_seconds)

    return saved, stats


def _crawl_from_sitemaps(
    domain: str,
    limit: int,
    include: Iterable[str],
    exclude: Iterable[str],
    include_domain: Iterable[str],
    exclude_domain: Iterable[str],
    rate_seconds: float,
    out_base: str,
    use_headless: bool,
) -> Tuple[List[str], Dict[str, int]]:
    rp = _robots_parser(domain)
    sitemap_urls = _discover_sitemap_urls(domain, use_headless)
    saved: List[str] = []
    stats = {
        "visited": 0,
        "saved": 0,
        "filtered": 0,
        "robots_blocked": 0,
        "http_error": 0,
        "fetch_error": 0,
        "sitemap_urls": len(sitemap_urls),
    }
    merged_include = list(include) + list(include_domain)
    merged_exclude = list(exclude) + list(exclude_domain)

    for url in sitemap_urls:
        if len(saved) >= limit:
            break
        if not _is_same_domain(url, domain):
            continue
        stats["visited"] += 1
        if not rp.can_fetch(USER_AGENT, url):
            stats["robots_blocked"] += 1
            continue
        if not _filter_url(url, merged_include, merged_exclude):
            stats["filtered"] += 1
            continue
        try:
            status, html = (
                _fetch_headless(url) if use_headless else _fetch(url)
            )
        except Exception:
            stats["fetch_error"] += 1
            continue
        if status >= 400:
            stats["http_error"] += 1
            continue
        saved.append(_save_html(out_base, domain, url, html))
        stats["saved"] = len(saved)
        time.sleep(rate_seconds)

    return saved, stats


def _choose_limit(min_limit: int, max_limit: int) -> int:
    if max_limit < min_limit:
        return min_limit
    return max_limit


def run_scraper(
    config_path: str,
    out_base: str,
    limit_min: int,
    limit_max: int,
    rate_seconds: float,
    include: Iterable[str],
    exclude: Iterable[str],
    ingest_after: bool,
    source: str,
    use_headless: bool,
    use_sitemaps: bool,
) -> List[str]:
    config = _read_config(config_path)
    domains = config.get("domains", [])
    urls = config.get("urls_especificas", [])
    include_by_domain = _parse_domain_rules(config.get("include_paths", []))
    exclude_by_domain = _parse_domain_rules(config.get("exclude_paths", []))
    outputs: List[str] = []
    report = {
        "timestamp": dt.datetime.now().isoformat(),
        "domains": {},
        "urls_especificas": {"requested": len(urls), "saved": 0},
    }

    for domain in domains:
        limit = _choose_limit(limit_min, limit_max)
        if use_sitemaps:
            domain_outputs, stats = _crawl_from_sitemaps(
                domain=domain,
                limit=limit,
                include=include,
                exclude=exclude,
                include_domain=include_by_domain.get(domain, []),
                exclude_domain=exclude_by_domain.get(domain, []),
                rate_seconds=rate_seconds,
                out_base=out_base,
                use_headless=use_headless,
            )
        else:
            domain_outputs, stats = crawl_domain(
                domain=domain,
                limit=limit,
                include=include,
                exclude=exclude,
                include_domain=include_by_domain.get(domain, []),
                exclude_domain=exclude_by_domain.get(domain, []),
                rate_seconds=rate_seconds,
                out_base=out_base,
                use_headless=use_headless,
            )
        outputs.extend(domain_outputs)
        report["domains"][domain] = stats

    for url in urls:
        try:
            status, html = (
                _fetch_headless(url) if use_headless else _fetch(url)
            )
        except Exception:
            continue
        if status == 0 and use_headless:
            continue
        if status >= 400:
            continue
        outputs.append(_save_html(out_base, url, url, html))
        report["urls_especificas"]["saved"] += 1

    if ingest_after and outputs:
        ingest(outputs, out_base, source)

    _write_report(out_base, report)

    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description="BK scraper pipeline")
    parser.add_argument(
        "--config",
        default=os.path.join(os.getcwd(), "docs", "scraper-sources.txt"),
        help="Path to config file",
    )
    parser.add_argument(
        "--out",
        default=os.path.join(os.getcwd(), "base_conhecimento"),
        help="Base conhecimento path",
    )
    parser.add_argument("--limit-min", type=int, default=DEFAULT_LIMIT_MIN)
    parser.add_argument("--limit-max", type=int, default=DEFAULT_LIMIT_MAX)
    parser.add_argument("--rate-seconds", type=float, default=1.5)
    parser.add_argument("--include", nargs="*", default=INCLUDE_KEYWORDS)
    parser.add_argument("--exclude", nargs="*", default=EXCLUDE_KEYWORDS)
    parser.add_argument("--ingest", action="store_true")
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--use-sitemaps", action="store_true")
    parser.add_argument("--source", default="scraper")
    args = parser.parse_args()

    outputs = run_scraper(
        config_path=args.config,
        out_base=args.out,
        limit_min=args.limit_min,
        limit_max=args.limit_max,
        rate_seconds=args.rate_seconds,
        include=args.include,
        exclude=args.exclude,
        ingest_after=args.ingest,
        source=args.source,
        use_headless=args.headless,
        use_sitemaps=args.use_sitemaps,
    )
    for output in outputs:
        print(output)


def _write_report(out_base: str, report: dict) -> str:
    report_dir = os.path.join(out_base, "_reports")
    os.makedirs(report_dir, exist_ok=True)
    name = f"scrape-{dt.datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    path = os.path.join(report_dir, name)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2)
    return path


if __name__ == "__main__":
    main()
