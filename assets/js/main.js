(() => {
  'use strict';

  // Enable enhanced navigation only after this file loads successfully.
  document.documentElement.classList.add('js');

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
})();
