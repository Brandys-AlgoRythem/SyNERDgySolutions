# Open Website Decisions

This register tracks unresolved items without placing inaccurate placeholders on the public website.

## Launch-critical

| Item | Current state | Required decision or evidence | Public treatment until resolved |
|---|---|---|---|
| GitHub repair branch | Deployed for live review | Review the visual-recovery pull request into `edit/v1-post-mvp` | Do not merge into `main` |
| Current GitHub Pages site | Serves the approved repair-branch build with styling and navigation restored | Complete stakeholder and device-level review | Keep `main` frozen; deploy only through the approved repair workflow |
| Custom domain | Open | Select and verify a custom production domain if desired | Keep project-path-safe relative URLs and no invented canonical domain |
| Deployment platform | GitHub Pages approved for repair review | Confirm the long-term production platform before any custom-domain change | Preserve project-path compatibility and the documented deployment workflow |
| Final standalone corporate logo files | Not located in connected sources | Approve an SVG and high-resolution PNG if a standalone corporate mark is required | Use the repository’s controlled hive wordmark and approved stylized bee assets |
| Favicon | MVP asset complete | Replace only if the final corporate mark is approved | Use current controlled hexagonal mark and manifest hooks |
| Social preview image | MVP asset complete | Replace only if a final campaign image is approved | Use current 1200 × 630 brand card; absolute URL generated after domain selection |
| Contact workflow | Decided for MVP | Revisit only if a form or intake service is needed | Use `synerdgysolutions@gmail.com` mailto |

## MVP architecture

| Item | Current state | Required decision or evidence | Public treatment until resolved |
|---|---|---|---|
| Five-page sitemap | Final for MVP | Revisit after launch evidence shows a need | Home, Services, Capabilities, About, Contact |
| Contracting content location | Final for MVP | Separate page only when content volume justifies it | Place verified contracting profile within Capabilities |
| Resources content location | Deferred | Separate page after public assets are approved | Introduce Governance Hive within Capabilities |
| Six service categories | Final for MVP | Revisit only after buyer feedback or content expansion | Publish six top-level service areas |

## Content and contracting

| Item | Current state | Required decision or evidence | Public treatment until resolved |
|---|---|---|---|
| Legal company-name display | Verified | Revisit only with a legal-name change | Use SyNERDgy Solutions LLC where legal name is needed |
| Business address format | Requires verification | Select public address or service-area wording | Omit street address |
| UEI | Verified for publication | Recheck before procurement submissions | Publish SNVGAWQLG8Q3 without implying active SAM/CAGE status |
| Kentucky Vendor ID | Verified for publication | Recheck if the state profile changes | Publish KS0031871 |
| Primary NAICS | Verified for publication | Recheck if the corporate profile changes | Publish 541611 |
| Registration status | Requires verification | Confirm current active status from official source | Do not describe as active until verified |
| Geographic service area | Verified | Revisit if delivery capacity changes | Kentucky statewide; remote nationwide |
| Leadership details | Verified for MVP | Recheck when roles change | Publish selected technical and contracting authority only |
| Capability statement | Final procurement statement located in controlled Drive | Approve a public, web-safe distribution copy before adding a download | Offer the current statement through an authorized contact; show no private Drive link |

## Resources and proof

| Item | Current state | Required decision or evidence | Public treatment until resolved |
|---|---|---|---|
| Governance Hive visuals | Working | Product screenshots remain optional and must be sanitized | Use the current CSS conceptual dashboard, not private product screens |
| Governance Hive description | Final for MVP | Revisit after product release or client use | Label as SyNERDgy-developed representative applied work, not client past performance |
| Sample work product | Not created | Produce sanitized public sample | Omit download control |
| Research publications | Pending | Confirm publication and preprint status | Omit from MVP navigation |
| Authoritative resource links | Pending | Curate and verify selected links | Do not create an unreviewed link dump |

## Design and accessibility

| Item | Current state | Required decision or evidence | Public treatment until resolved |
|---|---|---|---|
| Exact gold | Final for MVP | Revisit with a formal brand package | Use approved accessible design tokens |
| Typography | Final for MVP | Revisit only if licensed web fonts are approved | Use durable system-font stack |
| Honeycomb pattern | Final for MVP | Revisit during aesthetic review | Keep subtle, decorative, and non-essential |
| Bee artwork | Implemented | Replace only with separately approved brand assets | Use the existing controlled stylized bee assets as decorative images |
| Circuit-board details | Implemented | Revisit only during an approved brand refinement | Keep decorative, restrained, and outside the reading order |
| Accessibility statement | Implemented | Recheck after any structural or integration change | Publish the contact-page statement and verified contact channels |
| Motion | Implemented conservatively | Recheck after any animation change | Respect reduced motion and keep content understandable without motion |

## Deployment and review

| Item | Current state | Required decision or evidence | Public treatment until resolved |
|---|---|---|---|
| Production branch policy | Explicit repair exception approved | Revisit only if deployment architecture changes | Keep `main` frozen; publish this recovery only from `repair/github-pages-visual-recovery` |
| Repair preview | Live and technically verified | Complete stakeholder and physical-device review | Review at `https://brandys-algorythem.github.io/SyNERDgySolutions/` |
| Analytics | Excluded from MVP | Explicit later decision required | No analytics or cookies |
| Privacy language | Implemented for current static site | Re-review before adding forms, analytics, cookies, accounts, or third-party scripts | State the current implementation and safe-inquiry boundary only |
