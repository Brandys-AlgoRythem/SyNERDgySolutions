#!/usr/bin/env python3
"""Validate the static SyNERDgy website using only the Python standard library."""

from __future__ import annotations

import json
import re
import struct
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "site.config.json").read_text(encoding="utf-8"))
URL_MARKER = "BEGIN SITE URL METADATA"


@dataclass
class PageData:
    path: Path
    title: str = ""
    description: str = ""
    lang: str = ""
    charset: str = ""
    viewport: str = ""
    h1_count: int = 0
    main_count: int = 0
    skip_links: list[str] = field(default_factory=list)
    ids: set[str] = field(default_factory=set)
    links: list[str] = field(default_factory=list)
    scripts: list[str] = field(default_factory=list)
    assets: list[str] = field(default_factory=list)
    meta_name: dict[str, str] = field(default_factory=dict)
    meta_property: dict[str, str] = field(default_factory=dict)
    link_rels: list[tuple[set[str], str, dict[str, str]]] = field(default_factory=list)
    jsonld: list[str] = field(default_factory=list)


class StaticHTMLParser(HTMLParser):
    def __init__(self, path: Path):
        super().__init__(convert_charrefs=True)
        self.data = PageData(path=path)
        self._in_title = False
        self._title_parts: list[str] = []
        self._jsonld_active = False
        self._jsonld_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = {key: (value or "") for key, value in attrs_list}
        if tag == "html":
            self.data.lang = attrs.get("lang", "")
        elif tag == "title":
            self._in_title = True
        elif tag == "meta":
            if "charset" in attrs:
                self.data.charset = attrs["charset"]
            name = attrs.get("name", "").lower()
            prop = attrs.get("property", "").lower()
            content = attrs.get("content", "")
            if name:
                self.data.meta_name[name] = content
                if name == "description":
                    self.data.description = content
                elif name == "viewport":
                    self.data.viewport = content
            if prop:
                self.data.meta_property[prop] = content
        elif tag == "h1":
            self.data.h1_count += 1
        elif tag == "main":
            self.data.main_count += 1
        elif tag == "a":
            href = attrs.get("href", "")
            if href:
                self.data.links.append(href)
            classes = set(attrs.get("class", "").split())
            if "skip-link" in classes:
                self.data.skip_links.append(href)
        elif tag == "link":
            rels = set(attrs.get("rel", "").lower().split())
            self.data.link_rels.append((rels, attrs.get("href", ""), attrs))
        elif tag == "script":
            src = attrs.get("src", "")
            if src:
                self.data.scripts.append(src)
            if attrs.get("type") == "application/ld+json":
                self._jsonld_active = True
                self._jsonld_parts = []
        elif tag in {"img", "source", "video", "audio", "iframe"}:
            src = attrs.get("src", "")
            if src:
                self.data.assets.append(src)

        element_id = attrs.get("id")
        if element_id:
            self.data.ids.add(element_id)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False
            self.data.title = "".join(self._title_parts).strip()
        elif tag == "script" and self._jsonld_active:
            self.data.jsonld.append("".join(self._jsonld_parts).strip())
            self._jsonld_active = False
            self._jsonld_parts = []

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self._title_parts.append(data)
        if self._jsonld_active:
            self._jsonld_parts.append(data)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def route_to_file(route_path: str) -> Path:
    if route_path == "/":
        return ROOT / "index.html"
    if route_path.endswith("/"):
        return ROOT / route_path.lstrip("/") / "index.html"
    return ROOT / route_path.lstrip("/")


def is_root_relative_reference(value: str) -> bool:
    parsed = urlparse(value)
    return not parsed.scheme and not value.startswith("//") and parsed.path.startswith("/")


def resolve_internal(source: Path, href: str) -> tuple[Path | None, str | None]:
    parsed = urlparse(href)
    if parsed.scheme or href.startswith("//") or href.startswith("mailto:") or href.startswith("tel:"):
        return None, None
    fragment = unquote(parsed.fragment) if parsed.fragment else None
    raw_path = unquote(parsed.path)
    if not raw_path:
        return source, fragment
    if raw_path.startswith("/"):
        target = route_to_file(raw_path)
    else:
        target = (source.parent / raw_path).resolve()
        try:
            target.relative_to(ROOT.resolve())
        except ValueError:
            return target, fragment
        if raw_path.endswith("/"):
            target = target / "index.html"
        elif target.is_dir():
            target = target / "index.html"
    return target, fragment


def png_dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        signature = handle.read(8)
        if signature != b"\x89PNG\r\n\x1a\n":
            raise ValueError("not a PNG")
        length = struct.unpack(">I", handle.read(4))[0]
        chunk = handle.read(4)
        if chunk != b"IHDR" or length < 8:
            raise ValueError("missing PNG IHDR")
        width, height = struct.unpack(">II", handle.read(8))
        return width, height


def iter_text_files() -> list[Path]:
    suffixes = {".html", ".css", ".js", ".json", ".md", ".txt", ".xml", ".yml", ".yaml", ".svg", ".py"}
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() in suffixes or path.name in {"robots.txt"}:
            files.append(path)
    return files


def validate() -> list[str]:
    errors: list[str] = []
    pages: dict[Path, PageData] = {}
    route_files: set[Path] = set()

    for route in CONFIG["routes"]:
        path = ROOT / route["file"]
        route_files.add(path.resolve())
        if not path.exists():
            fail(errors, f"Missing required page: {route['file']}")
            continue
        parser = StaticHTMLParser(path)
        parser.feed(path.read_text(encoding="utf-8"))
        pages[path.resolve()] = parser.data

    titles: dict[str, Path] = {}
    descriptions: dict[str, Path] = {}
    required_links = {
        "manifest": ROOT / "site.webmanifest",
        "apple-touch-icon": ROOT / "assets/images/apple-touch-icon.png",
        "icon-svg": ROOT / "assets/images/favicon.svg",
    }

    for path, page in pages.items():
        rel = path.relative_to(ROOT.resolve())
        if page.lang.lower() != "en":
            fail(errors, f"{rel}: html lang must be en")
        if page.charset.lower() != "utf-8":
            fail(errors, f"{rel}: missing UTF-8 charset")
        if "width=device-width" not in page.viewport:
            fail(errors, f"{rel}: missing responsive viewport")
        if not page.title:
            fail(errors, f"{rel}: missing title")
        elif page.title in titles:
            fail(errors, f"{rel}: duplicate title also used by {titles[page.title].relative_to(ROOT)}")
        else:
            titles[page.title] = path
        if not page.description:
            fail(errors, f"{rel}: missing meta description")
        elif page.description in descriptions:
            fail(errors, f"{rel}: duplicate description also used by {descriptions[page.description].relative_to(ROOT)}")
        else:
            descriptions[page.description] = path
        if page.h1_count != 1:
            fail(errors, f"{rel}: expected exactly one h1, found {page.h1_count}")
        if page.main_count != 1:
            fail(errors, f"{rel}: expected exactly one main, found {page.main_count}")
        if "#main-content" not in page.skip_links or "main-content" not in page.ids:
            fail(errors, f"{rel}: skip link must target #main-content")
        if page.meta_name.get("theme-color", "").lower() != "#11100e":
            fail(errors, f"{rel}: missing approved theme-color")
        for key in ("og:type", "og:site_name", "og:title", "og:description", "og:locale"):
            if not page.meta_property.get(key):
                fail(errors, f"{rel}: missing {key}")
        if page.meta_property.get("og:title") != page.title:
            fail(errors, f"{rel}: og:title must match title")
        if page.meta_property.get("og:description") != page.description:
            fail(errors, f"{rel}: og:description must match meta description")
        if page.meta_name.get("twitter:title") != page.title:
            fail(errors, f"{rel}: twitter:title must match title")
        if page.meta_name.get("twitter:description") != page.description:
            fail(errors, f"{rel}: twitter:description must match description")

        rel_map: dict[str, list[tuple[str, dict[str, str]]]] = {}
        for rels, href, attrs in page.link_rels:
            for relation in rels:
                rel_map.setdefault(relation, []).append((href, attrs))
        def relation_targets(relation: str, expected: Path) -> bool:
            for href, _attrs in rel_map.get(relation, []):
                target, _fragment = resolve_internal(path, href)
                if target is not None and target.resolve() == expected.resolve():
                    return True
            return False

        if not relation_targets("manifest", required_links["manifest"]):
            fail(errors, f"{rel}: missing site manifest hook")
        if not relation_targets("apple-touch-icon", required_links["apple-touch-icon"]):
            fail(errors, f"{rel}: missing apple-touch-icon hook")
        if not relation_targets("icon", required_links["icon-svg"]):
            fail(errors, f"{rel}: missing SVG favicon hook")

        browser_references = (
            page.links
            + page.scripts
            + page.assets
            + [href for _rels, href, _attrs in page.link_rels if href]
        )
        for reference in browser_references:
            if is_root_relative_reference(reference):
                fail(
                    errors,
                    f"{rel}: root-relative browser reference {reference} will bypass a GitHub Pages project path",
                )

        raw = path.read_text(encoding="utf-8")
        if URL_MARKER not in raw:
            fail(errors, f"{rel}: missing URL metadata marker block")
        is_404 = rel.as_posix() == "404.html"
        robots = page.meta_name.get("robots", "").lower()
        if is_404 and "noindex" not in robots:
            fail(errors, "404.html: must be noindex")
        if not is_404 and "noindex" in robots:
            fail(errors, f"{rel}: public page must not be noindex")

    # Internal link and anchor validation.
    for path, page in pages.items():
        rel = path.relative_to(ROOT.resolve())
        references = (
            page.links
            + page.scripts
            + page.assets
            + [href for _rels, href, _attrs in page.link_rels if href]
        )
        for href in references:
            target, fragment = resolve_internal(path, href)
            if target is None:
                continue
            if not target.exists():
                fail(errors, f"{rel}: broken internal reference {href} -> {target.relative_to(ROOT.resolve()) if target.is_relative_to(ROOT.resolve()) else target}")
                continue
            if fragment and target.suffix.lower() == ".html":
                target_page = pages.get(target.resolve())
                if target_page is None:
                    parser = StaticHTMLParser(target)
                    parser.feed(target.read_text(encoding="utf-8"))
                    target_page = parser.data
                    pages[target.resolve()] = target_page
                if fragment not in target_page.ids:
                    fail(errors, f"{rel}: missing anchor #{fragment} in {target.relative_to(ROOT)}")

    # Homepage structured data.
    home = pages.get((ROOT / "index.html").resolve())
    if home is not None:
        parsed_jsonld = []
        for block in home.jsonld:
            try:
                parsed_jsonld.append(json.loads(block))
            except json.JSONDecodeError as exc:
                fail(errors, f"index.html: invalid JSON-LD: {exc}")
        org_found = False
        website_found = False
        for data in parsed_jsonld:
            nodes = data.get("@graph", [data]) if isinstance(data, dict) else []
            for node in nodes:
                if node.get("@type") == "Organization":
                    org_found = True
                    for key in ("name", "legalName", "description", "foundingDate", "email", "address"):
                        if not node.get(key):
                            fail(errors, f"index.html: Organization schema missing {key}")
                if node.get("@type") == "WebSite":
                    website_found = True
        if not org_found:
            fail(errors, "index.html: Organization structured data missing")
        if not website_found:
            fail(errors, "index.html: WebSite structured data missing")

    # Manifest and asset checks.
    manifest_path = ROOT / "site.webmanifest"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(errors, f"site.webmanifest: invalid or missing: {exc}")
        manifest = {}
    for key in ("name", "short_name", "description", "start_url", "scope", "display", "background_color", "theme_color", "icons"):
        if not manifest.get(key):
            fail(errors, f"site.webmanifest: missing {key}")
    if manifest.get("start_url") != "./":
        fail(errors, "site.webmanifest: start_url must be project-path-safe (./)")
    if manifest.get("scope") != "./":
        fail(errors, "site.webmanifest: scope must be project-path-safe (./)")
    expected_icons = {
        "assets/images/icon-192.png": (192, 192),
        "assets/images/icon-512.png": (512, 512),
    }
    for src, dims in expected_icons.items():
        path = ROOT / src
        if not path.exists():
            fail(errors, f"Missing manifest icon: {src}")
            continue
        try:
            actual = png_dimensions(path)
            if actual != dims:
                fail(errors, f"{src}: expected {dims}, found {actual}")
        except ValueError as exc:
            fail(errors, f"{src}: {exc}")
    social = ROOT / CONFIG["defaultSocialImage"].lstrip("/")
    if not social.exists():
        fail(errors, "Missing default social preview image")
    else:
        try:
            if png_dimensions(social) != (1200, 630):
                fail(errors, "Social preview image must be 1200x630")
        except ValueError as exc:
            fail(errors, f"Social preview image: {exc}")

    # robots and sitemap state must match configured origin.
    site_url = CONFIG.get("siteUrl")
    robots_text = (ROOT / "robots.txt").read_text(encoding="utf-8")
    try:
        sitemap_root = ET.parse(ROOT / "sitemap.xml").getroot()
    except (OSError, ET.ParseError) as exc:
        fail(errors, f"sitemap.xml: invalid or missing: {exc}")
        sitemap_root = None
    if "User-agent: *" not in robots_text:
        fail(errors, "robots.txt: must allow public crawling")
    if site_url:
        base_path = urlparse(site_url).path.rstrip("/")
        expected_allow = f"{base_path}/" if base_path else "/"
        if f"Allow: {expected_allow}" not in robots_text:
            fail(errors, "robots.txt: allow path does not match the configured site base URL")
        if f"Sitemap: {site_url}/sitemap.xml" not in robots_text:
            fail(errors, "robots.txt: configured sitemap URL does not match site.config.json")
        expected_urls = {
            (site_url.rstrip("/") + (route["path"] if route["path"] != "/" else "/"))
            for route in CONFIG["routes"]
            if route.get("indexable")
        }
        actual_urls = set()
        if sitemap_root is not None:
            ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            actual_urls = {node.text or "" for node in sitemap_root.findall("sm:url/sm:loc", ns)}
        if actual_urls != expected_urls:
            fail(errors, f"sitemap.xml: expected {sorted(expected_urls)}, found {sorted(actual_urls)}")
        for path, page in pages.items():
            rel = path.relative_to(ROOT.resolve())
            canonical = [href for rels, href, _ in page.link_rels if "canonical" in rels]
            if len(canonical) != 1:
                fail(errors, f"{rel}: configured site requires exactly one canonical URL")
            if not page.meta_property.get("og:url") or not page.meta_property.get("og:image"):
                fail(errors, f"{rel}: configured site requires og:url and og:image")
    else:
        if "Allow: /" not in robots_text:
            fail(errors, "robots.txt: must allow public crawling")
        if re.search(r"^Sitemap:\s*https?://", robots_text, flags=re.M):
            fail(errors, "robots.txt: must not invent a sitemap origin before domain approval")
        if sitemap_root is not None:
            urls = [node for node in sitemap_root.iter() if node.tag.endswith("loc")]
            if urls:
                fail(errors, "sitemap.xml: must remain empty until a real domain is configured")
        for path, page in pages.items():
            rel = path.relative_to(ROOT.resolve())
            canonical = [href for rels, href, _ in page.link_rels if "canonical" in rels]
            if canonical or page.meta_property.get("og:url") or page.meta_property.get("og:image"):
                fail(errors, f"{rel}: URL-dependent metadata must be absent while siteUrl is null")

    # Repository content and secret scanning.
    secret_patterns = {
        "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
        "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
        "generic API key assignment": re.compile(r"(?i)\b(?:api[_-]?key|secret[_-]?key|password)\s*[:=]\s*['\"][^'\"]{8,}['\"]"),
    }
    local_path_patterns = [re.compile(r"/mnt/data/"), re.compile(r"file://", re.I), re.compile(r"[A-Za-z]:\\\\")]
    public_suffixes = {".html", ".css", ".js", ".json", ".txt", ".xml", ".svg"}
    for path in iter_text_files():
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8", errors="replace")
        for label, pattern in secret_patterns.items():
            if pattern.search(text):
                fail(errors, f"{rel}: possible {label}")
        if path.suffix.lower() in public_suffixes or path.name in {"robots.txt"}:
            if re.search(r"\b(?:TBD|TODO|FIXME)\b", text, flags=re.I):
                fail(errors, f"{rel}: public file contains unfinished marker")
            if "drive.google.com" in text or "docs.google.com" in text:
                fail(errors, f"{rel}: public file contains a Drive link")
            for pattern in local_path_patterns:
                if pattern.search(text):
                    fail(errors, f"{rel}: public file contains a local filesystem path")
            if path.suffix.lower() == ".css" and re.search(
                r"url\(\s*['\"]?/(?!/)", text, flags=re.I
            ):
                fail(errors, f"{rel}: CSS contains a root-relative url() that is unsafe on project Pages")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print(f"Site validation failed with {len(errors)} issue(s):", file=sys.stderr)
        for issue in errors:
            print(f"- {issue}", file=sys.stderr)
        return 1
    print("Site validation passed.")
    print(f"Validated {len(CONFIG['routes'])} HTML documents, metadata, links, assets, manifest, robots, sitemap state, structured data, and repository content controls.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
