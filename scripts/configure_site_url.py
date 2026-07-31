#!/usr/bin/env python3
"""Configure or clear the production site base URL without inventing one in source.

Usage:
  python3 scripts/configure_site_url.py https://example.com
  python3 scripts/configure_site_url.py https://owner.github.io/repository-name
  python3 scripts/configure_site_url.py --clear
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse
from xml.sax.saxutils import escape as xml_escape

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "site.config.json"
START_MARKER = "  <!-- BEGIN SITE URL METADATA -->"
END_MARKER = "  <!-- END SITE URL METADATA -->"
EMPTY_BLOCK = (
    f"{START_MARKER}\n"
    "  <!-- Run: python3 scripts/configure_site_url.py https://your-domain.example -->\n"
    f"{END_MARKER}"
)


def normalize_site_url(raw: str) -> str:
    value = raw.strip().rstrip("/")
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(
            "Site URL must be an absolute http(s) base URL, such as "
            "https://example.com or https://owner.github.io/repository-name"
        )
    if parsed.params or parsed.query or parsed.fragment:
        raise ValueError("Site URL may include a project path but not parameters, a query, or a fragment")
    if any(part in {".", ".."} for part in parsed.path.split("/")):
        raise ValueError("Site URL project paths may not contain dot segments")
    return value


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def save_config(config: dict) -> None:
    CONFIG_PATH.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")


def page_url(site_url: str, route_path: str) -> str:
    if route_path == "/":
        return f"{site_url}/"
    return f"{site_url}{route_path}"


def replace_url_block(text: str, replacement: str, path: Path) -> str:
    pattern = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
        flags=re.S,
    )
    updated, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise RuntimeError(f"Missing or duplicate URL metadata markers in {path}")
    return updated


def configure_page(path: Path, route_path: str, site_url: str | None, social_image: str) -> None:
    text = path.read_text(encoding="utf-8")
    if site_url is None:
        text = replace_url_block(text, EMPTY_BLOCK, path)
    else:
        canonical = page_url(site_url, route_path)
        image_url = f"{site_url}{social_image}"
        block = "\n".join(
            [
                START_MARKER,
                f'  <link rel="canonical" href="{canonical}">',
                f'  <meta property="og:url" content="{canonical}">',
                f'  <meta property="og:image" content="{image_url}">',
                '  <meta property="og:image:width" content="1200">',
                '  <meta property="og:image:height" content="630">',
                '  <meta property="og:image:alt" content="SyNERDgy Solutions: Order isn’t accidental. It’s engineered.">',
                '  <meta name="twitter:card" content="summary_large_image">',
                f'  <meta name="twitter:image" content="{image_url}">',
                '  <meta name="twitter:image:alt" content="SyNERDgy Solutions: Order isn’t accidental. It’s engineered.">',
                END_MARKER,
            ]
        )
        text = replace_url_block(text, block, path)
    path.write_text(text, encoding="utf-8")


def update_structured_data(site_url: str | None, social_image: str) -> None:
    path = ROOT / "index.html"
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(
        r'(<script type="application/ld\+json" id="organization-schema">\s*)(.*?)(\s*</script>)',
        flags=re.S,
    )
    match = pattern.search(text)
    if not match:
        raise RuntimeError("Homepage organization schema block was not found")
    data = json.loads(match.group(2))
    graph = data.get("@graph", [])
    for node in graph:
        if node.get("@type") == "Organization":
            if site_url:
                node["url"] = f"{site_url}/"
                node["logo"] = f"{site_url}/assets/images/icon-512.png"
                node["image"] = f"{site_url}{social_image}"
            else:
                for key in ("url", "logo", "image"):
                    node.pop(key, None)
        elif node.get("@type") == "WebSite":
            if site_url:
                node["url"] = f"{site_url}/"
            else:
                node.pop("url", None)
    serialized = json.dumps(data, indent=2)
    text = pattern.sub(lambda m: m.group(1) + serialized + m.group(3), text, count=1)
    path.write_text(text, encoding="utf-8")


def write_robots(site_url: str | None) -> None:
    allowed_path = "/"
    if site_url:
        base_path = urlparse(site_url).path.rstrip("/")
        allowed_path = f"{base_path}/" if base_path else "/"
    lines = ["User-agent: *", f"Allow: {allowed_path}", ""]
    if site_url:
        lines.append(f"Sitemap: {site_url}/sitemap.xml")
    else:
        lines.extend(
            [
                "# The production sitemap URL is added by scripts/configure_site_url.py",
                "# after the final domain is approved.",
            ]
        )
    (ROOT / "robots.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_sitemap(config: dict, site_url: str | None) -> None:
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    if site_url is None:
        lines.append(
            "<!-- URL entries are generated by scripts/configure_site_url.py after the final domain is approved. -->"
        )
        lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>')
    else:
        lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
        for route in config["routes"]:
            if not route.get("indexable"):
                continue
            loc = xml_escape(page_url(site_url, route["path"]))
            lines.extend(["  <url>", f"    <loc>{loc}</loc>", "  </url>"])
        lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "site_url",
        nargs="?",
        help="Production base URL, such as https://example.com or https://owner.github.io/repository-name",
    )
    group.add_argument("--clear", action="store_true", help="Remove production URL metadata")
    args = parser.parse_args()

    config = load_config()
    site_url = None if args.clear else normalize_site_url(args.site_url)
    config["siteUrl"] = site_url

    for route in config["routes"]:
        configure_page(
            ROOT / route["file"],
            route["path"],
            site_url,
            config["defaultSocialImage"],
        )

    update_structured_data(site_url, config["defaultSocialImage"])
    write_robots(site_url)
    write_sitemap(config, site_url)
    save_config(config)

    state = "cleared" if site_url is None else f"set to {site_url}"
    print(f"Production URL metadata {state}.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, RuntimeError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
