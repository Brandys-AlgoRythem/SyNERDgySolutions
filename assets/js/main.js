(() => {
  'use strict';

  // Enable enhanced navigation only after this file loads successfully.
  document.documentElement.classList.add('js');

  const toggle = document.querySelector('[data-nav-toggle]');
  const navigation = document.querySelector('[data-site-nav]');
  const toggleLabel = toggle?.querySelector('.nav-toggle__label');

  const setToggleLabel = (isOpen) => {
    if (toggleLabel) toggleLabel.textContent = isOpen ? 'Close' : 'Menu';
  };

  const closeMenu = ({ restoreFocus = false } = {}) => {
    if (!toggle || !navigation) return;
    toggle.setAttribute('aria-expanded', 'false');
    navigation.dataset.open = 'false';
    setToggleLabel(false);
    if (restoreFocus) toggle.focus();
  };

  const openMenu = () => {
    if (!toggle || !navigation) return;
    toggle.setAttribute('aria-expanded', 'true');
    navigation.dataset.open = 'true';
    setToggleLabel(true);
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
      if (event.target instanceof Element && event.target.closest('a')) closeMenu();
    });

    document.addEventListener('click', (event) => {
      if (
        toggle.getAttribute('aria-expanded') === 'true'
        && event.target instanceof Node
        && !toggle.contains(event.target)
        && !navigation.contains(event.target)
      ) {
        closeMenu();
      }
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

  // BEGIN SYNERDGY FUNNEL ANALYTICS
  const safeAnalyticsText = (value) => String(value || '').trim().replace(/\s+/g, ' ').slice(0, 120);

  const sendAnalyticsEvent = (eventName, parameters = {}) => {
    if (typeof window.gtag !== 'function') return;
    window.gtag('event', eventName, parameters);
  };

  document.addEventListener('click', (event) => {
    if (!(event.target instanceof Element)) return;
    const link = event.target.closest('a[href]');
    if (!link) return;

    const href = link.getAttribute('href') || '';
    const linkText = safeAnalyticsText(link.textContent || link.getAttribute('aria-label'));
    const sourcePage = window.location.pathname;

    if (href.startsWith('mailto:')) {
      sendAnalyticsEvent('contact_email_click', {
        link_url: href,
        link_text: linkText,
        source_page: sourcePage
      });
      return;
    }

    let url;
    try {
      url = new URL(href, window.location.href);
    } catch {
      return;
    }

    const hostname = url.hostname.toLowerCase();
    const isFlevy = hostname === 'flevy.com' || hostname.endsWith('.flevy.com');

    if (isFlevy) {
      sendAnalyticsEvent('flevy_outbound_click', {
        link_url: url.href,
        link_text: linkText,
        source_page: sourcePage,
        product_id: safeAnalyticsText(link.dataset.productId)
      });
      return;
    }

    if (url.origin === window.location.origin) {
      if (/(^|\/)contact\/?$/.test(url.pathname)) {
        sendAnalyticsEvent('contact_cta_click', {
          link_url: url.href,
          link_text: linkText,
          source_page: sourcePage
        });
      }
      return;
    }

    sendAnalyticsEvent('outbound_click', {
      link_url: url.href,
      link_domain: hostname,
      link_text: linkText,
      source_page: sourcePage
    });
  }, { capture: true });
  // END SYNERDGY FUNNEL ANALYTICS

})();
