# SyNERDgy Solutions LLC

Official public website repository for **SyNERDgy Solutions LLC**, a Lexington, Kentucky applied R&D and operational intelligence firm focused on root-cause analysis, governance, compliance, systems analysis, and implementation.

> Systems fail at the seams. We work at the seams.

## Public links

- Website: https://brandys-algorythem.github.io/SyNERDgySolutions/
- LinkedIn: https://www.linkedin.com/company/synerdgy-solutions-llc/
- GitHub: https://github.com/Brandys-AlgoRythem/SyNERDgySolutions

## Project purpose

This repository contains SyNERDgy Solutions LLC's public website and search-identity configuration. The site explains the company’s services, capabilities, operating philosophy, applied research and operational-intelligence focus, and contact path in a clear, accessible, buyer-facing format.

The repository also maintains the public entity signals used to help search engines connect the website, company identity, public profiles, location, expertise, canonical URLs, and social metadata to the same organization.

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
- Build-time canonical and social URL generation
- Organization and WebSite structured data
- Search-engine indexing directives and sitemap generation
- Cross-profile identity signals through structured-data `sameAs` and HTML `rel="me"`

## Public identity configuration

`site.config.json` is the source of truth for public search identity. It contains the legal company name, homepage search title and description, verified identity profiles, search topics, areas of expertise, social-image path, and indexable routes.

When another verified public company profile is established, add its canonical URL to `identityProfiles`. The build then publishes that relationship into the site metadata and Organization schema without requiring the same link to be edited manually across every page.

Only verified SyNERDgy-controlled or authoritative profiles should be added. Do not add guessed directory URLs or unrelated mentions merely because they rank in search.

## Repository workflow

- `main` preserves the frozen MVP baseline.
- Post-MVP refinements occur on `edit/v1-post-mvp`.
- Visual recovery and current public deployment work occurs on `repair/github-pages-visual-recovery`.
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

## Public URL configuration

The same source can be published at the current GitHub Pages project path or a future custom domain. Generate canonical URLs, social-image URLs, robots directives, Organization/WebSite IDs, and the sitemap with either base URL:

```bash
python3 scripts/configure_site_url.py https://brandys-algorythem.github.io/SyNERDgySolutions
# later, if a custom domain is adopted:
python3 scripts/configure_site_url.py https://approved-domain.example
python3 scripts/validate_site.py
```

A domain migration therefore changes the canonical base URL without changing the underlying company identity graph.

## Deployment

The source uses document-relative browser paths so the same build works at a domain root and beneath the GitHub Pages project path `/SyNERDgySolutions/`. `.github/workflows/deploy-pages.yml` publishes the repair branch through the isolated `github-pages-repair` environment and injects the current GitHub Pages base URL before validation and deployment. The workflow does not merge into or update `main`.

## Current status

The active repair branch is the current GitHub Pages deployment source. It preserves the five-page structure and dark hive-and-circuit presentation while carrying deploy-time canonical URLs, social metadata, search indexing directives, structured organization identity, verified cross-profile links, robots configuration, and sitemap generation for public discovery. The frozen `main` baseline remains unchanged.
