#!/usr/bin/env python3
"""Configure or clear the production site base URL and public identity metadata.

Usage:
  python3 scripts/configure_site_url.py https://example.com
  python3 scripts/configure_site_url.py https://owner.github.io/repository-name
  python3 scripts/configure_site_url.py --clear
"""

from __future__ import annotations

import argparse
import html
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


def meta_escape(value: str) -> str:
    return html.escape(value, quote=True)


def configure_page(
    path: Path,
    route_path: str,
    site_url: str | None,
    social_image: str,
    indexable: bool,
    identity_profiles: list[str],
    keywords: list[str],
    site_name: str,
    legal_name: str,
) -> None:
    text = path.read_text(encoding="utf-8")
    if site_url is None:
        text = replace_url_block(text, EMPTY_BLOCK, path)
    else:
        canonical = page_url(site_url, route_path)
        image_url = f"{site_url}{social_image}"
        robots = (
            "index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"
            if indexable
            else "noindex,follow"
        )
        keyword_text = ", ".join(keywords)
        block_lines = [
            START_MARKER,
            f'  <link rel="canonical" href="{meta_escape(canonical)}">',
            f'  <meta name="robots" content="{robots}">',
            f'  <meta name="googlebot" content="{robots}">',
            f'  <meta name="author" content="{meta_escape(legal_name)}">',
            f'  <meta name="publisher" content="{meta_escape(legal_name)}">',
            f'  <meta name="application-name" content="{meta_escape(site_name)}">',
            '  <meta name="geo.region" content="US-KY">',
            '  <meta name="geo.placename" content="Lexington, Kentucky">',
            f'  <meta property="og:url" content="{meta_escape(canonical)}">',
            f'  <meta property="og:image" content="{meta_escape(image_url)}">',
            '  <meta property="og:image:width" content="1200">',
            '  <meta property="og:image:height" content="630">',
            '  <meta property="og:image:alt" content="SyNERDgy Solutions: Order isn’t accidental. It’s engineered.">',
            '  <meta name="twitter:card" content="summary_large_image">',
            f'  <meta name="twitter:image" content="{meta_escape(image_url)}">',
            '  <meta name="twitter:image:alt" content="SyNERDgy Solutions: Order isn’t accidental. It’s engineered.">',
        ]
        if keyword_text:
            block_lines.append(f'  <meta name="keywords" content="{meta_escape(keyword_text)}">')
        for profile in identity_profiles:
            safe_profile = meta_escape(profile)
            block_lines.append(f'  <link rel="me" href="{safe_profile}">')
            block_lines.append(f'  <meta property="og:see_also" content="{safe_profile}">')
        block_lines.append(END_MARKER)
        text = replace_url_block(text, "\n".join(block_lines), path)
    path.write_text(text, encoding="utf-8")


def replace_single(text: str, pattern: str, replacement: str, label: str) -> str:
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.S | re.I)
    if count != 1:
        raise RuntimeError(f"Could not update {label}")
    return updated


def update_homepage_identity(config: dict) -> None:
    path = ROOT / "index.html"
    text = path.read_text(encoding="utf-8")
    title = config.get("homeTitle", "").strip()
    description = config.get("homeDescription", "").strip()
    if not title or not description:
        return

    safe_title = meta_escape(title)
    safe_description = meta_escape(description)
    text = replace_single(text, r"<title>.*?</title>", f"<title>{safe_title}</title>", "homepage title")
    text = replace_single(
        text,
        r'<meta\s+name="description"\s+content="[^"]*">',
        f'<meta name="description" content="{safe_description}">',
        "homepage meta description",
    )
    text = replace_single(
        text,
        r'<meta\s+property="og:title"\s+content="[^"]*">',
        f'<meta property="og:title" content="{safe_title}">',
        "homepage Open Graph title",
    )
    text = replace_single(
        text,
        r'<meta\s+property="og:description"\s+content="[^"]*">',
        f'<meta property="og:description" content="{safe_description}">',
        "homepage Open Graph description",
    )
    text = replace_single(
        text,
        r'<meta\s+name="twitter:title"\s+content="[^"]*">',
        f'<meta name="twitter:title" content="{safe_title}">',
        "homepage Twitter title",
    )
    text = replace_single(
        text,
        r'<meta\s+name="twitter:description"\s+content="[^"]*">',
        f'<meta name="twitter:description" content="{safe_description}">',
        "homepage Twitter description",
    )
    path.write_text(text, encoding="utf-8")


def service_offer_catalog(service_catalog: list[dict], organization_id: str) -> dict | None:
    if not service_catalog:
        return None
    offers = []
    for service in service_catalog:
        name = service.get("name", "").strip()
        if not name:
            continue
        item = {
            "@type": "Service",
            "name": name,
            "provider": {"@id": organization_id},
            "areaServed": {
                "@type": "Country",
                "name": "United States",
            },
        }
        service_type = service.get("serviceType", "").strip()
        description = service.get("description", "").strip()
        if service_type:
            item["serviceType"] = service_type
        if description:
            item["description"] = description
        offers.append({"@type": "Offer", "itemOffered": item})
    if not offers:
        return None
    return {
        "@type": "OfferCatalog",
        "name": "SyNERDgy Solutions Consulting, Workflow, Compliance, Operations, and R&D Services",
        "itemListElement": offers,
    }


def credential_nodes(credentials: list[dict]) -> list[dict]:
    nodes = []
    for credential in credentials:
        name = credential.get("name", "").strip()
        if not name:
            continue
        node = {
            "@type": "Credential",
            "name": name,
        }
        category = credential.get("credentialCategory", "").strip()
        if category:
            node["credentialCategory"] = category
        recognized_by = credential.get("recognizedBy") or {}
        recognized_name = recognized_by.get("name", "").strip()
        recognized_url = recognized_by.get("url", "").strip()
        if recognized_name or recognized_url:
            authority = {"@type": "Organization"}
            if recognized_name:
                authority["name"] = recognized_name
            if recognized_url:
                authority["url"] = recognized_url
            node["recognizedBy"] = authority
        nodes.append(node)
    return nodes


def update_structured_data(
    site_url: str | None,
    social_image: str,
    identity_profiles: list[str],
    organization_description: str,
    knows_about: list[str],
    service_catalog: list[dict],
    credentials: list[dict],
) -> None:
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
    organization_id = f"{site_url}/#organization" if site_url else "#organization"
    website_id = f"{site_url}/#website" if site_url else "#website"

    for node in graph:
        if node.get("@type") == "Organization":
            node["@id"] = organization_id
            node["sameAs"] = identity_profiles
            node["slogan"] = "Systems fail at the seams. We work there."
            if organization_description:
                node["description"] = organization_description
            if knows_about:
                node["knowsAbout"] = knows_about
            node["foundingLocation"] = {
                "@type": "Place",
                "name": "Lexington, Kentucky, United States",
            }
            node["contactPoint"] = {
                "@type": "ContactPoint",
                "contactType": "business inquiries",
                "email": "synerdgysolutions@gmail.com",
                "areaServed": "US",
                "availableLanguage": "en",
            }
            catalog = service_offer_catalog(service_catalog, organization_id)
            if catalog:
                node["hasOfferCatalog"] = catalog
            else:
                node.pop("hasOfferCatalog", None)
            credential_list = credential_nodes(credentials)
            if credential_list:
                node["hasCredential"] = credential_list
            else:
                node.pop("hasCredential", None)
            if site_url:
                node["url"] = f"{site_url}/"
                node["logo"] = f"{site_url}/assets/images/icon-512.png"
                node["image"] = f"{site_url}{social_image}"
            else:
                for key in ("url", "logo", "image"):
                    node.pop(key, None)
        elif node.get("@type") == "WebSite":
            node["@id"] = website_id
            node["publisher"] = {"@id": organization_id}
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
    lines = [
        "User-agent: *",
        f"Allow: {allowed_path}",
        "",
    ]
    if site_url:
        lines.append(f"Sitemap: {site_url}/sitemap.xml")
    else:
        lines.extend(
            [
                "# The production sitemap URL is added by scripts/configure_site_url.py",
                "# after the public site URL is configured.",
            ]
        )
    (ROOT / "robots.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_sitemap(config: dict, site_url: str | None) -> None:
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    if site_url is None:
        lines.append(
            "<!-- URL entries are generated by scripts/configure_site_url.py after the public site URL is configured. -->"
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
        help="Public site base URL, such as https://example.com or https://owner.github.io/repository-name",
    )
    group.add_argument("--clear", action="store_true", help="Remove public URL metadata")
    args = parser.parse_args()

    config = load_config()
    site_url = None if args.clear else normalize_site_url(args.site_url)
    config["siteUrl"] = site_url

    identity_profiles = config.get("identityProfiles", [])
    keywords = config.get("keywords", [])
    organization_description = config.get("organizationDescription", "")
    knows_about = config.get("knowsAbout", [])
    service_catalog = config.get("serviceCatalog", [])
    credentials = config.get("credentials", [])
    site_name = config.get("siteName", "SyNERDgy Solutions")
    legal_name = config.get("legalName", "SyNERDgy Solutions LLC")

    update_homepage_identity(config)

    for route in config["routes"]:
        configure_page(
            ROOT / route["file"],
            route["path"],
            site_url,
            config["defaultSocialImage"],
            route.get("indexable", False),
            identity_profiles,
            keywords,
            site_name,
            legal_name,
        )

    update_structured_data(
        site_url,
        config["defaultSocialImage"],
        identity_profiles,
        organization_description,
        knows_about,
        service_catalog,
        credentials,
    )
    write_robots(site_url)
    write_sitemap(config, site_url)
    save_config(config)

    state = "cleared" if site_url is None else f"set to {site_url}"
    print(f"Public URL and identity metadata {state}.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, RuntimeError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
