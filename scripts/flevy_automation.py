#!/usr/bin/env python3
"""Build tracked Flevy redirects and snapshot public Flevy listing signals.

Commands:
  python3 scripts/flevy_automation.py build
  python3 scripts/flevy_automation.py watch
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "flevy-products.json"
GO_DIR = ROOT / "go"
VISIBILITY_DIR = ROOT / "data" / "flevy-visibility"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36 "
    "SyNERDgy-Flevy-Visibility/1.0"
)


def load_registry() -> dict:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    required = {"ga4_measurement_id", "public_base_url", "sources", "destinations"}
    missing = required - set(data)
    if missing:
        raise ValueError(f"Registry missing required keys: {sorted(missing)}")

    if not re.fullmatch(r"G-[A-Z0-9]+", str(data["ga4_measurement_id"])):
        raise ValueError("ga4_measurement_id must be a GA4 G- measurement ID")

    keys: set[str] = set()
    for item in data["destinations"]:
        key = str(item.get("key", "")).strip()
        if not key or key in keys:
            raise ValueError(f"Destination key missing or duplicated: {key!r}")
        keys.add(key)
        url = item.get("destination_url")
        if url:
            parsed = urlparse(url)
            host = parsed.hostname.lower() if parsed.hostname else ""
            if parsed.scheme != "https" or not (host == "flevy.com" or host.endswith(".flevy.com")):
                raise ValueError(f"Destination {key} is not an https://flevy.com URL")
    return data


def js_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def redirect_html(*, measurement_id: str, destination: dict, source: str) -> str:
    target = str(destination["destination_url"])
    item_key = str(destination["key"])
    item_type = str(destination.get("type") or "unknown")
    core_id = destination.get("core_id")
    title = str(destination.get("title") or item_key)
    product_id = "" if core_id is None else str(core_id)

    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex,nofollow">
  <title>Opening Flevy | SyNERDgy Solutions</title>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={html.escape(measurement_id, quote=True)}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', {js_string(measurement_id)}, {{
      send_page_view: false,
      allow_google_signals: false,
      allow_ad_personalization_signals: false
    }});
  </script>
</head>
<body>
  <p>Opening Flevy…</p>
  <p><a id="fallback-link" href="{html.escape(target, quote=True)}">Continue to Flevy</a></p>
  <script>
    (() => {{
      const target = {js_string(target)};
      const params = new URLSearchParams(window.location.search);
      const campaign = (params.get('campaign') || '').slice(0, 120);
      let redirected = false;
      const go = () => {{
        if (redirected) return;
        redirected = true;
        window.location.replace(target);
      }};

      const fallback = window.setTimeout(go, 1100);
      try {{
        gtag('event', 'flevy_redirect', {{
          source: {js_string(source)},
          destination_type: {js_string(item_type)},
          destination_key: {js_string(item_key)},
          product_id: {js_string(product_id)},
          product_title: {js_string(title[:100])},
          campaign: campaign,
          link_url: target,
          transport_type: 'beacon',
          event_callback: () => {{
            window.clearTimeout(fallback);
            go();
          }},
          event_timeout: 900
        }});
      }} catch (error) {{
        go();
      }}
    }})();
  </script>
</body>
</html>
'''


def build_redirects() -> int:
    registry = load_registry()
    if GO_DIR.exists():
        shutil.rmtree(GO_DIR)
    GO_DIR.mkdir(parents=True)

    base = str(registry["public_base_url"]).rstrip("/")
    measurement_id = str(registry["ga4_measurement_id"])
    sources = [str(value).strip().lower() for value in registry["sources"] if str(value).strip()]
    manifest: list[dict] = []

    for item in registry["destinations"]:
        if not item.get("destination_url"):
            continue
        key = str(item["key"])
        for source in sources:
            route_dir = GO_DIR / key / source
            route_dir.mkdir(parents=True, exist_ok=True)
            (route_dir / "index.html").write_text(
                redirect_html(
                    measurement_id=measurement_id,
                    destination=item,
                    source=source,
                ),
                encoding="utf-8",
            )
            manifest.append(
                {
                    "destination_key": key,
                    "product_id": item.get("core_id"),
                    "title": item.get("title"),
                    "destination_type": item.get("type"),
                    "source": source,
                    "tracking_url": f"{base}/go/{key}/{source}/",
                    "destination_url": item["destination_url"],
                }
            )

    (GO_DIR / "links.json").write_text(
        json.dumps(
            {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "count": len(manifest),
                "links": manifest,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Built {len(manifest)} tracked Flevy redirect routes in {GO_DIR}")
    return 0


def strip_html(text: str) -> str:
    text = re.sub(r"(?is)<script\b.*?</script>", " ", text)
    text = re.sub(r"(?is)<style\b.*?</style>", " ", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def fetch_public_page(url: str) -> dict:
    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    try:
        with urlopen(request, timeout=30) as response:
            raw = response.read(3_000_000).decode("utf-8", errors="replace")
            final_url = response.geturl()
            status = getattr(response, "status", 200)
    except HTTPError as exc:
        return {"ok": False, "status_code": exc.code, "error": f"HTTP {exc.code}", "final_url": url}
    except URLError as exc:
        return {"ok": False, "status_code": None, "error": str(exc.reason), "final_url": url}
    except Exception as exc:  # pragma: no cover - defensive network guard
        return {"ok": False, "status_code": None, "error": str(exc), "final_url": url}

    text = strip_html(raw)
    title_match = re.search(r"(?is)<title[^>]*>(.*?)</title>", raw)
    page_title = strip_html(title_match.group(1)) if title_match else None

    prices = []
    for match in re.findall(r"\$\s?\d[\d,]*(?:\.\d{2})?", text):
        normalized = match.replace(" ", "")
        if normalized not in prices:
            prices.append(normalized)

    count_match = re.search(r"Total document\(s\):\s*(\d+)", text, flags=re.I)
    document_count = int(count_match.group(1)) if count_match else None

    return {
        "ok": 200 <= int(status) < 400,
        "status_code": int(status),
        "final_url": final_url,
        "page_title": page_title,
        "prices_detected": prices[:10],
        "document_count": document_count,
        "has_add_to_cart": "Add to Cart" in text,
        "has_immediate_download": "Immediate download" in text,
        "body_mentions_synerdgy": "SyNERDgy" in text,
        "error": None,
    }


def comparable(entry: dict) -> dict:
    fields = [
        "ok",
        "status_code",
        "final_url",
        "page_title",
        "prices_detected",
        "document_count",
        "has_add_to_cart",
        "has_immediate_download",
    ]
    return {field: entry.get(field) for field in fields}


def watch_visibility() -> int:
    registry = load_registry()
    VISIBILITY_DIR.mkdir(parents=True, exist_ok=True)
    history_dir = VISIBILITY_DIR / "history"
    history_dir.mkdir(parents=True, exist_ok=True)
    latest_path = VISIBILITY_DIR / "latest.json"

    previous = {}
    if latest_path.exists():
        try:
            previous_data = json.loads(latest_path.read_text(encoding="utf-8"))
            previous = {str(item["key"]): item for item in previous_data.get("entries", [])}
        except Exception:
            previous = {}

    checked_at = datetime.now(timezone.utc)
    entries = []
    changes = []

    for item in registry["destinations"]:
        url = item.get("destination_url")
        if not url:
            continue
        key = str(item["key"])
        result = fetch_public_page(str(url))
        entry = {
            "key": key,
            "type": item.get("type"),
            "core_id": item.get("core_id"),
            "title": item.get("title"),
            "registry_status": item.get("status"),
            "destination_url": url,
            **result,
        }
        entries.append(entry)
        old = previous.get(key)
        if old and comparable(old) != comparable(entry):
            changed_fields = [
                field
                for field in comparable(entry)
                if comparable(old).get(field) != comparable(entry).get(field)
            ]
            changes.append({"key": key, "changed_fields": changed_fields})
        elif not old:
            changes.append({"key": key, "changed_fields": ["new_snapshot"]})

    snapshot = {
        "checked_at": checked_at.isoformat(),
        "source": "public_flevy_pages",
        "limitations": (
            "Public-page monitoring does not expose Flevy-native visitor/pageview counts. "
            "It records only public listing/catalog signals available without seller analytics."
        ),
        "entries": entries,
        "changes": changes,
    }

    payload = json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n"
    latest_path.write_text(payload, encoding="utf-8")
    day_path = history_dir / f"{checked_at.date().isoformat()}.json"
    day_path.write_text(payload, encoding="utf-8")

    summary_lines = [
        "# Flevy public visibility snapshot",
        "",
        f"Checked: `{checked_at.isoformat()}`",
        "",
        "| Key | Type | HTTP | Public signal | Price(s) | Catalog docs |",
        "|---|---|---:|---|---|---:|",
    ]
    for entry in entries:
        public_signal = "reachable" if entry.get("ok") else f"error: {entry.get('error') or 'unknown'}"
        prices = ", ".join(entry.get("prices_detected") or []) or "—"
        count = entry.get("document_count")
        summary_lines.append(
            f"| {entry['key']} | {entry.get('type') or '—'} | {entry.get('status_code') or '—'} | "
            f"{public_signal} | {prices} | {count if count is not None else '—'} |"
        )

    summary_lines.extend(["", "## Changes since previous snapshot", ""])
    if changes:
        for change in changes:
            summary_lines.append(f"- **{change['key']}**: {', '.join(change['changed_fields'])}")
    else:
        summary_lines.append("- No public-page signal changes detected.")

    summary_lines.extend(
        [
            "",
            "> Native Flevy pageviews remain a blind spot unless Flevy exposes seller-side traffic analytics. "
            "This watcher does not infer visitors from rankings, prices, or catalog state.",
            "",
        ]
    )
    summary = "\n".join(summary_lines)
    (VISIBILITY_DIR / "summary.md").write_text(summary, encoding="utf-8")
    print(summary)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build", "watch"))
    args = parser.parse_args()
    try:
        if args.command == "build":
            return build_redirects()
        return watch_visibility()
    except Exception as exc:
        print(f"Flevy automation failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
