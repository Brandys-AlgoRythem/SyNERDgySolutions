# MVP QA Checklist

## Automated gate

Run:

```bash
python3 scripts/validate_site.py
```

Required result: exit code `0` and `Site validation passed.`

## Keyboard and interaction review

- Skip link becomes visible on focus and moves focus to the main landmark
- Navigation order follows the visible page order
- Mobile menu button exposes its expanded state
- Escape closes the mobile menu and restores focus to the toggle
- Selecting a navigation link closes the mobile menu
- Navigation remains visible if the external script is missing or JavaScript is disabled
- Focus indicators remain visible against light, gold, and dark surfaces

## Responsive review

Check Home, Services, Capabilities, About, Contact, and 404 at:

- 320 × 568
- 390 × 844
- 768 × 1024
- 1440 × 900

Confirm no horizontal overflow, clipped text, inaccessible controls, overlapping cards, or hidden navigation.

## Content and claim review

- Compare public facts with `docs/PUBLIC-CLAIM-REGISTER.md`
- Confirm no active SAM/CAGE or award-history implication
- Confirm Governance Hive remains labeled as representative applied work
- Confirm no private source links, personal records, pricing, or unapproved metrics
- Confirm the public email remains correct

## Deployment-only checks

After the final origin is selected:

- Run `scripts/configure_site_url.py`
- Rerun the validator
- Confirm canonical URLs and social previews on the deployed origin
- Test the sitemap and robots URLs directly
- Run Google URL Inspection and structured-data testing after deployment
