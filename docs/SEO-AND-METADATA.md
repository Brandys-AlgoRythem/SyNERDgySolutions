# SEO and Metadata Controls

## Current state

The repository is intentionally domain-neutral until the final production origin is selected. It includes complete page titles, descriptions, Open Graph titles and descriptions, favicon hooks, a web app manifest, a 1200 × 630 social preview asset, organization structured data, `robots.txt`, and sitemap infrastructure.

Absolute canonical URLs, `og:url`, `og:image`, Twitter large-card image metadata, structured-data URLs, and sitemap URL entries are generated only after an approved production origin is available.

## Production URL workflow

```bash
python3 scripts/configure_site_url.py https://approved-domain.example
python3 scripts/validate_site.py
```

The command is idempotent and updates:

- Every public page’s canonical URL
- Open Graph page and image URLs
- Twitter large-card image metadata
- Homepage Organization and WebSite structured data
- `robots.txt`
- `sitemap.xml`
- `site.config.json`

Use `--clear` to remove absolute URL metadata and return to the safe pre-deployment state.

## Indexable routes

- `/`
- `/services/`
- `/capabilities/`
- `/about/`
- `/contact/`

`/404.html` is explicitly marked `noindex` and excluded from the sitemap.

## Asset policy

The current favicon and social preview are controlled MVP assets built from the approved black, cream, and honey-gold system. They do not claim to be the final corporate logo. Replacing them later must preserve the existing filenames or update the page, manifest, validator, and configuration references together.
