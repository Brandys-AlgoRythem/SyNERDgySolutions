# Post-MVP Edit Pass

The MVP architecture is frozen. Editing should improve clarity, credibility, and visual fit without reopening the sitemap unless a real user or buyer need justifies it.

## Review order

1. **Home** — headline rhythm, hero visual, section density, and CTA wording
2. **Services** — service names, ordering, buyer language, and scanability
3. **Capabilities** — contracting facts, representative-work treatment, and proof hierarchy
4. **About** — company story, leadership detail, and brand metaphor
5. **Contact** — inquiry guidance and accessibility contact language
6. **Brand assets** — final logo, favicon replacement, and social image
7. **Deployment** — domain, canonical URLs, GitHub publication, and Cloudflare preview

## Editing rules

- Keep the five-page MVP sitemap unless evidence supports expansion.
- Do not publish unverified registration, award, client, testimonial, insurance, or performance claims.
- Preserve the no-tracking and no-form statements unless the implementation changes first.
- Update `docs/PUBLIC-CLAIM-REGISTER.md` whenever a factual public claim changes.
- Run `python3 scripts/validate_site.py` before every package or deployment handoff.
