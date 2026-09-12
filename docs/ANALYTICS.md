# SyNERDgy Website Analytics Plan

## Purpose

The website analytics layer is designed to answer practical funnel questions without turning the public site into a marketing-technology pileup.

The core questions are:

- Which pages attract visitors?
- Which traffic sources send qualified visitors?
- Which pages cause visitors to click through to Flevy?
- Which products receive outbound interest from the SyNERDgy site?
- Which pages cause visitors to contact SyNERDgy?
- Which external links receive meaningful buyer attention?

## Current state

Analytics support is present in the shared site script but disabled by default.

No Google Analytics script loads unless both of these conditions are true in `site.config.json`:

```json
"enabled": true,
"ga4MeasurementId": "G-XXXXXXXXXX"
```

The repository should remain disabled until a real GA4 web data stream exists and the privacy disclosure/consent approach for the production site has been approved.

## Event model

### Automatic GA4 page views

When analytics are enabled, the GA4 configuration sends the normal page-view event for each public page load.

### `flevy_outbound_click`

Sent when a visitor clicks any link whose hostname is `flevy.com` or a Flevy subdomain.

Parameters:

- `link_url`
- `link_text`
- `source_page`
- `product_id` when the link includes `data-product-id`

Recommended Flevy link markup:

```html
<a href="https://flevy.com/..." data-product-id="26">View on Flevy</a>
```

The hostname detection works even without the data attribute; `data-product-id` simply makes product-level reporting cleaner.

### `contact_cta_click`

Sent when a visitor clicks an internal link to `/contact/`.

Parameters:

- `link_url`
- `link_text`
- `source_page`

### `contact_email_click`

Sent when a visitor clicks a `mailto:` link.

Parameters:

- `link_url`
- `link_text`
- `source_page`

### `outbound_click`

Sent for external links that are not Flevy links.

Parameters:

- `link_url`
- `link_domain`
- `link_text`
- `source_page`

## Privacy-oriented defaults

The GA4 loader is configured to:

- remain fully disabled until explicitly activated
- disable Google Signals
- disable ad-personalization signals
- respect browser Do Not Track when `respectDoNotTrack` is enabled in `site.config.json`

A privacy notice should be published before production analytics activation. If the site later targets or materially serves jurisdictions that require prior consent for analytics storage, add an appropriate consent mechanism before enabling GA4 there.

## Activation sequence

1. Create the SyNERDgy GA4 property and web data stream for the actual public website origin.
2. Copy the GA4 Measurement ID in `G-...` format.
3. Publish the site privacy disclosure and make any required consent decision.
4. Update `site.config.json`:
   - set `analytics.enabled` to `true`
   - set `analytics.ga4MeasurementId` to the real Measurement ID
5. Deploy the site.
6. Visit the site and confirm the page view in GA4 Realtime.
7. Click one contact CTA and one test Flevy link, then confirm the custom events arrive.
8. Mark the useful custom events as key events in GA4 if desired.

## Two-week Flevy test readout

For the initial Core 50/Flevy commercialization test, review:

- website users and sessions
- traffic source / medium
- landing pages
- `flevy_outbound_click` count by `source_page`
- `product_id` where available
- contact CTA and email click counts
- Flevy sales during the same period

Interpretation:

- Search or social traffic with few Flevy clicks suggests a page/message or CTA problem.
- Strong Flevy click volume with no sales suggests a marketplace listing, preview, pricing, or value-conversion problem.
- Little qualified site traffic suggests a discovery/distribution problem.
- Product-specific clicks and sales identify which Core 50 assets deserve more promotion, derivative products, or bundles.
