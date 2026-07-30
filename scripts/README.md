# Repository scripts

The website uses standard-library Python scripts so local and CI validation do not depend on a package manager.

## Validate the repository

```bash
python3 scripts/validate_site.py
```

The validator checks:

- Required pages and public assets
- Titles, descriptions, Open Graph fields, page landmarks, and skip links
- Internal links and anchor targets
- Manifest structure and icon dimensions
- Organization and website JSON-LD
- `robots.txt` and sitemap state
- Missing-script-safe static references
- Accidental secrets, private Drive links, unfinished public markers, and local paths

## Configure the production URL

Do not invent or commit a production domain. After the real origin is selected, run:

```bash
python3 scripts/configure_site_url.py https://example.com
python3 scripts/validate_site.py
```

That command adds canonical URLs, absolute Open Graph image and page URLs, Twitter large-card metadata, structured-data URLs, the sitemap entries, and the sitemap directive in `robots.txt`.

To return the repository to its domain-neutral state:

```bash
python3 scripts/configure_site_url.py --clear
```
