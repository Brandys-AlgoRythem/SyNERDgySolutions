# SyNERDgy Solutions LLC | Systems & Operations Consulting

Official public website repository for **SyNERDgy Solutions LLC**, a Lexington, Kentucky systems and operations consulting firm. The company name may also appear in search as **SyNERDgy Solutions**, **SyNERDgy**, or **SyNERDgySolutions**.

> Systems fail at the seams. We work at the seams.

## About SyNERDgy Solutions LLC

SyNERDgy Solutions helps organizations reconnect the people, processes, requirements, records, governance, and technology that must work together for operations to remain clear, consistent, and defensible.

Core public capability areas include:

- Governance, risk, and compliance
- Operations and process improvement
- Workflow engineering and implementation readiness
- Evidence and records architecture
- Research and decision support
- AI governance and responsible technology
- Human-centered systems design

**Location:** Lexington, Kentucky, United States  
**Legal name:** SyNERDgy Solutions LLC  
**Primary NAICS:** `541611`  
**Public GitHub repository:** `Brandys-AlgoRythem/SyNERDgySolutions`

## Project purpose

This repository contains the minimum viable public consulting website for SyNERDgy Solutions. The site explains the company’s services, capabilities, operating philosophy, contracting profile, and contact path in a clear, accessible, buyer-facing format.

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
- Static-host compatible

## Repository workflow

- `main` is the stable public baseline.
- Historical construction and post-MVP branches may remain for auditability and development history.
- Production deployment, DNS, and domain changes require explicit approval.

## Public repository boundary

This repository is public. It must not contain passwords, API keys, portal credentials, private legal or medical records, internal operating documents, unpublished personal information, confidential Drive links, pricing not approved for publication, or unverified business claims.

Approved public content is sourced from the SyNERDgy Website & Brand Project Hub and its companion messaging, capability, and registration materials. Missing facts must be documented in repository planning files rather than invented or exposed as public placeholders.

## Verified contracting identifiers

The public Capabilities page currently publishes the verified identifiers approved for public use:

- Kentucky Vendor ID: `KS0031871`
- UEI: `SNVGAWQLG8Q3`
- CAGE: `232V9`
- Primary NAICS: `541611`

These identifiers do not, by themselves, imply government award history, certification status, or eligibility for every procurement. Live registration status should be rechecked when material to a procurement submission.

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

The site is static-host compatible. A final production host and canonical domain have not yet been approved. The existing temporary public site is not treated as the canonical production identity. An approved static-site host or production ChatGPT Site can be connected after that decision.

## Current status

Version `1.0.0-mvp` remains the original five-page baseline. The public repository includes current contracting identifiers, an approved capability-statement status, domain-neutral metadata, structured data, site assets, automated validation, claims controls, and an explicit searchable company identity. The remaining major publication gates are the final production host, canonical domain, GitHub repository sidebar metadata, and any intentionally public downloadable assets.
