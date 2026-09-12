#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEASUREMENT_ID = "G-LQPJNWQB9V"

TAG = f'''  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={MEASUREMENT_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());

    gtag('config', '{MEASUREMENT_ID}');
  </script>'''

PAGES = [
    ROOT / "index.html",
    ROOT / "services/index.html",
    ROOT / "capabilities/index.html",
    ROOT / "about/index.html",
    ROOT / "contact/index.html",
    ROOT / "404.html",
]

OLD_DISCLOSURE = "This static MVP uses no analytics, tracking scripts, cookies, or contact-form processors."
NEW_DISCLOSURE = "This site uses Google Analytics to understand visits and outbound clicks. No contact-form processor is used."

for path in PAGES:
    text = path.read_text(encoding="utf-8")
    if f"googletagmanager.com/gtag/js?id={MEASUREMENT_ID}" not in text:
        text = text.replace("<head>\n", "<head>\n" + TAG + "\n", 1)
    text = text.replace(OLD_DISCLOSURE, NEW_DISCLOSURE)
    path.write_text(text, encoding="utf-8")

js_path = ROOT / "assets/js/main.js"
js = js_path.read_text(encoding="utf-8")
old = '''  const measurementId = 'G-LQPJNWQB9V';
  const analyticsEnabled = navigator.doNotTrack !== '1';
  const analyticsConfig = {
    trackFlevyOutbound: true,
    trackGeneralOutbound: true,
    trackContactCtas: true
  };

  if (analyticsEnabled) {
    window.dataLayer = window.dataLayer || [];
    window.gtag = function gtag() {
      window.dataLayer.push(arguments);
    };

    window.gtag('js', new Date());
    window.gtag('config', measurementId, {
      send_page_view: true,
      allow_google_signals: false,
      allow_ad_personalization_signals: false
    });

    const analyticsScript = document.createElement('script');
    analyticsScript.async = true;
    analyticsScript.src = `https://www.googletagmanager.com/gtag/js?id=${measurementId}`;
    analyticsScript.dataset.synerdgyAnalytics = 'ga4';
    document.head.appendChild(analyticsScript);
  }
'''
new = '''  const analyticsEnabled = typeof window.gtag === 'function';
  const analyticsConfig = {
    trackFlevyOutbound: true,
    trackGeneralOutbound: true,
    trackContactCtas: true
  };
'''
if old in js:
    js = js.replace(old, new, 1)
elif "const measurementId = 'G-LQPJNWQB9V';" in js:
    raise SystemExit("GA loader block changed unexpectedly; refusing partial edit")

js_path.write_text(js, encoding="utf-8")
print("Exact Google tag installed across all HTML pages; duplicate JS loader removed.")
