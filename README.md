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

This repository contains the public consulting website for SyNERDgy Solutions. The site explains the company’s services, capabilities, operating philosophy, contracting profile, direct-buy digital resources, and contact path in a clear, accessible, buyer-facing format.

## Public site scope

The original `1.0.0-mvp` launch baseline contained five public pages. The site now contains six public pages:

1. Home
2. Services
3. Capabilities
4. Resources
5. About
6. Contact

Contracting information is incorporated into the Capabilities page. The dedicated Resources page contains the currently approved fixed-price digital resources and secure Stripe purchase links. Scoped consulting remains inquiry-first rather than direct-buy.

## Digital resources

The Resources page currently publishes six fixed-price digital products:

- **#21 AI Workflow Design & Control Document** — $279
- **#22 Automated Agent Role Specification** — $299
- **#23 Data Flow Documentation & Control Guide** — $299
- **#25 Software Testing & Acceptance Protocol** — $179
- **#26 Quality Assurance Procedure for AI Outputs** — $149
- **#30 Human-in-the-Loop AI Control & Oversight Plan** — $349

These are one-time purchases. Product checkout is handled through Stripe-hosted Payment Links. The public website does not represent these resources as subscriptions or as organization-specific consulting engagements.

## Technical approach

The site is intentionally simple and durable:

- Semantic HTML5
- Modern CSS
- Minimal vanilla JavaScript
- No frontend framework
- No required package manager
- No backend
- Static-host compatible
- GA4 analytics enabled through one shared site script and one central configuration

## Analytics and funnel measurement

The shared site script uses GA4 to measure the buyer funnel without scattering tracking code across individual pages. The current SyNERDgy web data stream uses measurement ID `G-LQPJNWQB9V` and records page views, contact CTA clicks, email clicks, general outbound clicks, dedicated Flevy outbound-click events, and dedicated Stripe outbound-click events. Product links can include `data-product-id` so product-level outbound interest is visible in analytics.

Google Signals and ad-personalization signals are disabled, browser Do Not Track can be respected, and the public footer disclosure is updated by the shared script when the site loads. See `docs/ANALYTICS.md` for the broader event model and measurement approach.

## Repository workflow

- `main` is the stable public baseline.
- Historical construction and post-MVP branches may remain for auditability and development history.
- Production deployment, DNS, and domain changes require explicit approval.

## Public repository boundary

This repository is public. It must not contain passwords, API keys, portal credentials, private legal or medical records, internal operating documents, unpublished personal information, confidential Drive links, pricing not approved for publication, or unverified business claims.

Approved public content is sourced from the SyNERDgy Website & Brand Project Hub and its companion messaging, capability, registration, commercialization, and approved product materials. Missing facts must be documented in repository planning files rather than invented or exposed as public placeholders.

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

Version `1.0.0-mvp` remains the historical five-page launch baseline. The public repository now includes a dedicated Resources route with six approved fixed-price digital products and Stripe-hosted purchase links, alongside current contracting identifiers, an approved capability-statement status, domain-neutral metadata, structured data, site assets, automated validation, claims controls, an explicit searchable company identity, and active funnel analytics. The remaining major publication gates are the final production host, canonical domain, GitHub repository sidebar metadata, and any intentionally public downloadable assets.