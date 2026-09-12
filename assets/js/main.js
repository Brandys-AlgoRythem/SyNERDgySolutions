(() => {
  'use strict';

  document.documentElement.classList.add('js');

  const measurementId = 'G-LQPJNWQB9V';
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

  const toggle = document.querySelector('[data-nav-toggle]');
  const navigation = document.querySelector('[data-site-nav]');

  const closeMenu = ({ restoreFocus = false } = {}) => {
    if (!toggle || !navigation) return;
    toggle.setAttribute('aria-expanded', 'false');
    navigation.dataset.open = 'false';
    if (restoreFocus) toggle.focus();
  };

  const openMenu = () => {
    if (!toggle || !navigation) return;
    toggle.setAttribute('aria-expanded', 'true');
    navigation.dataset.open = 'true';
  };

  if (toggle && navigation) {
    navigation.dataset.open = 'false';

    toggle.addEventListener('click', () => {
      const isOpen = toggle.getAttribute('aria-expanded') === 'true';
      if (isOpen) {
        closeMenu();
      } else {
        openMenu();
      }
    });

    navigation.addEventListener('click', (event) => {
      if (event.target.closest('a')) closeMenu();
    });

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        closeMenu({ restoreFocus: true });
      }
    });

    window.addEventListener('resize', () => {
      if (window.matchMedia('(min-width: 52.01rem)').matches) closeMenu();
    });
  }

  const year = String(new Date().getFullYear());
  document.querySelectorAll('[data-current-year]').forEach((element) => {
    element.textContent = year;
  });

  const analyticsDisclosure = document.querySelector('.site-footer__contact p');
  if (analyticsDisclosure) {
    analyticsDisclosure.textContent = 'This site uses privacy-conscious analytics to understand visits and outbound clicks. Google Signals and ad-personalization signals are disabled, browser Do Not Track is respected, and no contact-form processor is used.';
  }

  const safeText = (value) => String(value || '').trim().replace(/\s+/g, ' ').slice(0, 120);

  const sendAnalyticsEvent = (eventName, parameters = {}) => {
    if (!analyticsEnabled || typeof window.gtag !== 'function') return;
    window.gtag('event', eventName, parameters);
  };

  if (analyticsEnabled) {
    document.addEventListener('click', (event) => {
      const link = event.target.closest('a[href]');
      if (!link) return;

      const href = link.getAttribute('href') || '';
      const linkText = safeText(link.textContent || link.getAttribute('aria-label'));
      const sourcePage = window.location.pathname;

      if (href.startsWith('mailto:')) {
        if (analyticsConfig.trackContactCtas) {
          sendAnalyticsEvent('contact_email_click', {
            link_url: href,
            link_text: linkText,
            source_page: sourcePage
          });
        }
        return;
      }

      let url;
      try {
        url = new URL(href, window.location.href);
      } catch {
        return;
      }

      if (url.origin === window.location.origin) {
        if (analyticsConfig.trackContactCtas && /(^|\/)contact\/?$/.test(url.pathname)) {
          sendAnalyticsEvent('contact_cta_click', {
            link_url: url.href,
            link_text: linkText,
            source_page: sourcePage
          });
        }
        return;
      }

      const hostname = url.hostname.toLowerCase();
      const isFlevy = hostname === 'flevy.com' || hostname.endsWith('.flevy.com');

      if (isFlevy && analyticsConfig.trackFlevyOutbound) {
        sendAnalyticsEvent('flevy_outbound_click', {
          link_url: url.href,
          link_text: linkText,
          source_page: sourcePage,
          product_id: safeText(link.dataset.productId)
        });
        return;
      }

      if (analyticsConfig.trackGeneralOutbound) {
        sendAnalyticsEvent('outbound_click', {
          link_url: url.href,
          link_domain: hostname,
          link_text: linkText,
          source_page: sourcePage
        });
      }
    }, { capture: true });
  }
})();
