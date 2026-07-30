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
- Static deployment through Cloudflare Pages

## Repository workflow

- `main` is the stable branch.
- Active MVP development occurs on `build/v1-site-shell`.
- Changes are reviewed through a draft pull request before merge or deployment.
- Production deployment, DNS, and domain changes require explicit approval.

## Public repository boundary

This repository is public. It must not contain passwords, API keys, portal credentials, private legal or medical records, internal operating documents, unpublished personal information, confidential Drive links, pricing not approved for publication, or unverified business claims.

Approved public content is sourced from the SyNERDgy Website & Brand Project Hub and its companion messaging materials. Missing facts must be documented in repository planning files rather than invented or exposed as public placeholders.

## Local preview

Run a simple local server from the repository root:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000` in a browser.


## Validation

Run the repository gate before review or packaging:

```bash
python3 scripts/validate_site.py
```

The command uses only the Python standard library and is also executed by the GitHub Actions workflow.

## Production URL configuration

The repository deliberately contains no invented canonical domain. After the real production origin is approved, generate canonical URLs, social-image URLs, `robots.txt`, and the sitemap with:

```bash
python3 scripts/configure_site_url.py https://approved-domain.example
python3 scripts/validate_site.py
```

## Deployment

Cloudflare Pages is the planned deployment platform. Deployment is deferred until the site passes content, accessibility, mobile, and visual review.

## Current status

Phase Six completes the domain-neutral metadata, site-file, and automated-validation infrastructure. The repository now includes page-specific social metadata, organization structured data, manifest and icon assets, robots and sitemap controls, a production-URL generator, a standard-library validator, a public claim register, and a GitHub Actions validation workflow. The final domain, remote GitHub publication, deployment, and launch review remain separate gates.