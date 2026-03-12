const THEME_KEY = 'portfolio-theme';
const THEME_DARK = 'dark';
const THEME_LIGHT = 'light';

function getSystemTheme() {
  if (typeof window === 'undefined' || !window.matchMedia) return THEME_LIGHT;
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? THEME_DARK : THEME_LIGHT;
}

function getInitialTheme() {
  if (typeof window === 'undefined') return THEME_LIGHT;
  const stored = localStorage.getItem(THEME_KEY);
  if (stored === THEME_DARK || stored === THEME_LIGHT) return stored;
  return getSystemTheme();
}

function applyTheme(theme) {
  const isDark = theme === THEME_DARK;
  document.documentElement.classList.toggle('dark-mode', isDark);
  document.documentElement.dataset.theme = isDark ? THEME_DARK : THEME_LIGHT;

  const themeBtn = document.querySelector('.theme-toggle');
  if (themeBtn) {
    themeBtn.setAttribute('aria-pressed', String(isDark));
    themeBtn.setAttribute('aria-label', isDark ? 'Switch to light mode' : 'Switch to dark mode');
  }
}

function setStoredTheme(theme) {
  localStorage.setItem(THEME_KEY, theme);
  applyTheme(theme);
}

// Navigation and smooth scrolling
function setupNav() {
  const navToggle = document.querySelector('.nav-toggle');
  const navLinks = document.querySelector('.nav-links');

  if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
      navLinks.classList.toggle('nav-open');
    });

    navLinks.addEventListener('click', (event) => {
      if (event.target.tagName.toLowerCase() === 'a') {
        navLinks.classList.remove('nav-open');
      }
    });
  }

  // Smooth scroll for in-page anchors with offset for sticky header
  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener('click', (e) => {
      const targetId = link.getAttribute('href');
      if (!targetId || targetId === '#') return;
      const section = document.querySelector(targetId);
      if (!section) return;

      e.preventDefault();
      const headerOffset = 70;
      const rect = section.getBoundingClientRect();
      const offsetTop = rect.top + window.scrollY - headerOffset;

      window.scrollTo({ top: offsetTop, behavior: 'smooth' });
    });
  });
}

function setupThemeToggle() {
  const themeBtn = document.querySelector('.theme-toggle');
  if (!themeBtn) return;

  themeBtn.addEventListener('click', () => {
    const isDark = document.documentElement.classList.contains('dark-mode');
    setStoredTheme(isDark ? THEME_LIGHT : THEME_DARK);
  });
}

window.addEventListener('DOMContentLoaded', () => {
  applyTheme(getInitialTheme());
  setupNav();
  setupThemeToggle();
});
