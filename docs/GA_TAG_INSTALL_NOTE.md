# Exact Google tag installation

Measurement ID: `G-LQPJNWQB9V`

The repository includes a one-time installer that places Google's exact gtag snippet immediately after `<head>` on every HTML page and removes the duplicate JavaScript-created base loader. Custom Flevy/contact/outbound event tracking remains in `assets/js/main.js` and uses the global `gtag` created by the exact snippet.
