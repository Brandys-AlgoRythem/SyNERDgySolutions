# GitHub Pages Visual Recovery Report

Date: July 30, 2026  
Branch: `repair/github-pages-visual-recovery`  
Base: `edit/v1-post-mvp`

## Scope and controls

This repair preserves the existing five-page website: Home, Services, Capabilities, About, and Contact. It does not merge into `main`, change the production deployment source, or deploy the repair. Existing controlled imagery and functionality remain in place.

## Root-cause diagnosis

The published project site is hosted beneath `/SyNERDgySolutions/`, but the HTML and manifest used root-relative references such as `/assets/css/styles.css`, `/assets/js/main.js`, `/services/`, and `/assets/images/favicon.svg`.

At the project URL, the browser therefore requested:

```text
https://brandys-algorythem.github.io/assets/css/styles.css
```

instead of:

```text
https://brandys-algorythem.github.io/SyNERDgySolutions/assets/css/styles.css
```

The missing stylesheet produced the white page with plain black text. The same path error affected JavaScript, images, icons, the manifest, and navigation. The repair uses document-relative paths from each page, so assets and routes resolve correctly both at a domain root and beneath a repository project path. Centralized styles remain in the shared stylesheets; no emergency inline page CSS was added.

## Connected sources used

### Google Drive

- SyNERDgy Website & Brand Project Hub
- SyNERDgy Brand Messaging System — Seams & Hive
- SyNERDgy Master Capability, Skills, Assets & Classification Inventory
- Final Procurement Capability Statement
- Technical Proposal — Final Selection Rationale
- Cost Proposal and Commercial Terms
- Internal Governance Operations Charter
- Quarterly Operational Review

The Project Hub tabs reviewed included Project Hub, Messaging Library, Website Copy Map, Content Inventory, Build Tracker, GitHub Code Plan, Decision Log, and Reference Links.

### Notion

- SyNERDgy Solutions, LLC.
- About SyNERDgy Solutions
- Capabilities & Qualifications
- Company & Contracting Information
- Leadership & Key Personnel
- Security, Confidentiality & AI Controls
- Classification Code Register
- Methodology & Delivery Framework
- Proposal & Acquisition Support
- Consulting & Advisory

Only public-safe facts and adapted public language were added to the repository. Controlled source documents, private links, internal procedures, personal details, and confidential examples were not copied.

## Visual repairs

- Restored the shared hive wordmark, black and deep-charcoal foundations, cream reading surfaces, warm-gold accents, brass boundaries, circuit details, and controlled stylized bee art.
- Preserved the eighteen-cell hero comb and its responsive treatment.
- Repaired the common header, active navigation, footer, calls to action, section boundaries, cards, buttons, and responsive spacing on all pages.
- Added centralized layouts for contact details, inquiry guidance, engagement steps, and public notices.
- Preserved visible keyboard focus, skip navigation, touch-sized controls, responsive typography, high-contrast text, and reduced-motion behavior.
- Improved the mobile menu’s open/close label and outside-click behavior.

## Copy repairs

- Restored “Systems fail at the seams. We work at the seams.” as the central approved message.
- Replaced abstract problem labels with specific operating problems such as knowledge trapped with one employee, records scattered across systems, unclear handoff ownership, overdue corrective actions, and inconsistent reporting.
- Aligned Services and Capabilities to the six confirmed engagement types: regulatory or program study, operational diagnostic, process rebuild, corrective-action support, administrative surge, and prime or subcontract support.
- Separated buyer problems, practical activities, deliverables, controls, and outcomes.
- Preserved “Fast where it matters. Controlled where it counts.” and “Easy to engage. Built to remain accountable.”
- Added verified business contact, location, leadership, vendor, UEI, and NAICS information while avoiding unsupported clients, contracts, certifications, results, SAM/CAGE status, or past-performance claims.
- Clarified that regulatory research is not legal representation or individualized legal advice.
- Added public-safe privacy, accessibility, website-terms, records, confidentiality, secure-exchange, written-communication, and commencement language based on connected operating materials.

## Page-by-page result

| Page | Final treatment |
|---|---|
| Home | Dark archival hero with the approved seams message, architectural hive, circuit details, intentional bee branding, specific warning signs, six engagement types, delivery controls, and a direct contact path. |
| Services | Six practical engagement types organized by the problem addressed, work performed, and typical deliverables. |
| Capabilities | Six capability families, a controlled delivery sequence, verified contracting profile, procurement boundaries, and engagement models. |
| About | Clear company purpose, origin and service area, operating principles, leadership roles, and public-scope boundaries. |
| Contact | Verified email, telephone, and service area; safe inquiry guidance; engagement and commencement steps; and public privacy, accessibility, terms, records, confidentiality, and communication notices. |

## Deployment state

The production GitHub Pages site continues to serve the frozen `main` baseline by instruction. The repair branch is reviewable but is not deployed to production. The production URL will remain:

```text
https://brandys-algorythem.github.io/SyNERDgySolutions/
```

Live Pages confirmation is therefore a launch gate that can occur only after separate approval to promote and deploy the reviewed repair. Branch-level rendering, local project-path checks, repository validation, and GitHub Actions provide the pre-deployment evidence.
