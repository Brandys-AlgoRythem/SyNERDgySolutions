# SyNERDgy Solutions Website

Official public website repository for **SyNERDgy Solutions LLC**.

> Systems fail at the seams. We work at the seams.

## Project purpose

This repository contains the minimum viable public consulting website for SyNERDgy Solutions. The site explains the company’s services, capabilities, operating philosophy, and contact path in a clear, accessible, buyer-facing format.

## MVP scope

The launch website contains five public pages:

1. Home
2. Services
3. Capabilities
4. About
5. Contact

Contracting information is incorporated into the Capabilities page. Representative work and future resources are also introduced there until a dedicated Resources page is justified.

## Technical approach

The MVP is intentionally simple and durable:

- Semantic HTML5
- Modern CSS
- Minimal vanilla JavaScript
- No frontend framework
- No required package manager
- No backend
- No cookies or analytics
- Project-path-safe static deployment through GitHub Pages or Cloudflare Pages

## Repository workflow

- `main` preserves the frozen MVP baseline.
- Post-MVP refinements occur on `edit/v1-post-mvp`.
- Visual recovery work occurs on `repair/github-pages-visual-recovery`, based on `edit/v1-post-mvp`.
- The completed construction history remains on `build/v1-site-shell`.
- Production deployment, DNS, and domain changes require explicit approval.

## Public repository boundary

This repository is public. It must not contain passwords, API keys, portal credentials, private legal or medical records, internal operating documents, unpublished personal information, confidential Drive links, pricing not approved for publication, or unverified business claims.

Approved public content is sourced from the SyNERDgy Website & Brand Project Hub and its companion messaging materials. Missing facts must be documented in repository planning files rather than invented or exposed as public placeholders.

## Local preview

Run a simple local server from the repository root:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000` in a browser. To reproduce GitHub Pages project-path behavior, serve the repository as a subdirectory and open a URL such as `http://localhost:8000/SyNERDgySolutions/`.


## Validation

Run the repository gate before review or packaging:

```bash
python3 scripts/validate_site.py
```

The command uses only the Python standard library and is also executed by the GitHub Actions workflow.

## Production URL configuration

The repository deliberately contains no invented canonical domain. After the real production origin is approved, generate canonical URLs, social-image URLs, `robots.txt`, and the sitemap with either a domain root or a GitHub Pages project path:

```bash
python3 scripts/configure_site_url.py https://approved-domain.example
# or
python3 scripts/configure_site_url.py https://brandys-algorythem.github.io/SyNERDgySolutions
python3 scripts/validate_site.py
```

## Deployment

The source uses document-relative browser paths so the same build works at a domain root and beneath the GitHub Pages project path `/SyNERDgySolutions/`. Following explicit approval, `.github/workflows/deploy-pages.yml` publishes the repair branch through the isolated `github-pages-repair` environment. The workflow does not merge into or update `main`.

## Current status

Version `1.0.9` is live from `repair/github-pages-visual-recovery` at `https://brandys-algorythem.github.io/SyNERDgySolutions/`. It preserves the five-page structure, fixes GitHub Pages project-path handling, restores the approved dark hive-and-circuit presentation, rewrites public copy from connected source records, adds public notices, and strengthens automated path validation. The frozen `main` baseline remains unchanged.
