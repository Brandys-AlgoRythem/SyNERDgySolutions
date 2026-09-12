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

GA4 analytics are activated in `site.config.json` using the SyNERDgy web data stream measurement ID `G-LQPJNWQB9V`.

The shared site script loads Google Analytics only when both of these conditions are true:

```json
"enabled": true,
"ga4MeasurementId": "G-LQPJNWQB9V"
```

The public footer disclosure is updated at runtime by the shared script to state that privacy-conscious analytics are in use. Google Signals and ad-personalization signals remain disabled, and browser Do Not Track is respected when `respectDoNotTrack` is enabled.

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

- load only when analytics are explicitly enabled with a valid measurement ID
- disable Google Signals
- disable ad-personalization signals
- respect browser Do Not Track when `respectDoNotTrack` is enabled in `site.config.json`
- disclose analytics use in the public site footer at runtime

If the site later targets or materially serves jurisdictions that require prior consent for analytics storage, add an appropriate consent mechanism before relying on analytics there.

## Activation verification

1. Deploy the current `main` branch after the GA4 activation change is merged.
2. Visit the live site and confirm the page view in GA4 Realtime.
3. Click one contact CTA and one test Flevy link, then confirm the custom events arrive.
4. Mark the useful custom events as key events in GA4 if desired.

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
