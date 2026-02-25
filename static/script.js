// Theme handling
const THEME_KEY = 'portfolio-theme';

function applyStoredTheme() {
  if (typeof window === 'undefined') return;
  const stored = localStorage.getItem(THEME_KEY);
  if (stored === 'dark') {
    document.body.classList.add('dark-mode');
  }
}

function toggleTheme() {
  const isDark = document.body.classList.toggle('dark-mode');
  localStorage.setItem(THEME_KEY, isDark ? 'dark' : 'light');
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

// Theme toggle button
function setupThemeToggle() {
  const themeBtn = document.querySelector('.theme-toggle');
  if (!themeBtn) return;

  const iconSpan = themeBtn.querySelector('.theme-icon');

  function syncIcon() {
    const isDark = document.body.classList.contains('dark-mode');
    if (iconSpan) {
      iconSpan.textContent = isDark ? '☀️' : '🌙';
    }
  }

  syncIcon();

  themeBtn.addEventListener('click', () => {
    toggleTheme();
    syncIcon();
  });
}

window.addEventListener('DOMContentLoaded', () => {
  applyStoredTheme();
  setupNav();
  setupThemeToggle();
});

// static/script.js

// Example: Dark mode toggle
function toggleDarkMode() {
  document.body.classList.toggle('dark-mode');
}

// Example: Welcome alert
function greetUser() {
  alert("Hey Bombi! Welcome to my portfolio ✨");
}

// Run on page load
window.onload = function () {
  greetUser();
};
