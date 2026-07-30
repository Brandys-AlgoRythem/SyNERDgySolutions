# Open Website Decisions

This register tracks unresolved items without placing inaccurate placeholders on the public website.

## Launch-critical

| Item | Current state | Required decision or evidence | Public treatment until resolved |
|---|---|---|---|
| GitHub contents write access | Blocked | Reauthorize the GitHub integration with repository contents write permission | Continue verified local development and package handoff |
| Final domain | Open | Select and verify production domain | Use no invented canonical domain |
| Cloudflare Pages project | Not connected | Approve project and repository connection | Document deployment only |
| Final logo files | Pending | Provide approved SVG and high-resolution PNG assets | Use text wordmark during shell build |
| Favicon | Pending | Approve favicon asset | Keep references out until asset exists |
| Social preview image | Pending | Approve 1200 × 630 image | Omit image URL until approved |
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
| Capability statement | Not created | Produce and approve public PDF | Show no broken download link |

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
| Exact gold | Working | Approve final accessible brand gold values | Use design-token placeholder |
| Typography | Working | Select licensed web fonts or retain system stack | Use system-font stack |
| Honeycomb pattern | Working | Approve scale, density, and placement | Keep subtle and decorative |
| Bee artwork | Pending | Provide approved assets | Do not use cartoon or stock bees |
| Circuit-board details | Future refinement | Determine where technology cues add value | Exclude from structural sprint |
| Accessibility statement | Pending | Approve wording and contact method | Provide accessibility contact language before launch |
| Motion | Deferred | Define restrained motion after shell review | Respect reduced-motion and avoid decorative animation initially |

## Deployment and review

| Item | Current state | Required decision or evidence | Public treatment until resolved |
|---|---|---|---|
| Production branch policy | Working | Confirm `main` as Cloudflare production branch | Do not deploy automatically |
| Preview deployment | Pending | Connect Cloudflare after initial pull request | Local preview only |
| Analytics | Excluded from MVP | Explicit later decision required | No analytics or cookies |
| Privacy language | Working | Verify implementation matches statement | State that the shell uses no tracking or cookies |
