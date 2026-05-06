/**
 * static/js/app.js - PathWise Learning Platform
 * Main client-side JavaScript
 */

'use strict';

// ── LOADING OVERLAY ────────────────────────────────────────────────────────

const LoadingOverlay = {
  el: null,

  show(steps = []) {
    this.el = document.createElement('div');
    this.el.className = 'loading-overlay fade-in';
    const stepsHtml = steps.map((s, i) =>
      `<div class="loading-step ${i === 0 ? 'active' : ''}" data-step="${i}">
        <span class="dot"></span><span>${s}</span>
      </div>`
    ).join('');
    this.el.innerHTML = `
      <div class="loading-spinner"></div>
      <div class="loading-text">Generating your personalized path…</div>
      ${steps.length ? `<div class="loading-steps">${stepsHtml}</div>` : ''}
    `;
    document.body.appendChild(this.el);
    if (steps.length) this._animateSteps(steps.length);
  },

  _animateSteps(total) {
    let current = 0;
    const interval = setInterval(() => {
      const allSteps = document.querySelectorAll('.loading-step');
      allSteps.forEach(s => s.classList.remove('active'));
      if (current < total) {
        allSteps[current]?.classList.add('done');
        current++;
        if (current < total) allSteps[current]?.classList.add('active');
      } else {
        clearInterval(interval);
      }
    }, 900);
  },

  hide() {
    if (this.el) {
      this.el.style.opacity = '0';
      this.el.style.transition = 'opacity 0.3s';
      setTimeout(() => this.el?.remove(), 300);
      this.el = null;
    }
  }
};


// ── FORM VALIDATION ────────────────────────────────────────────────────────

function validateRequired(form) {
  let valid = true;
  form.querySelectorAll('[required]').forEach(el => {
    if (!el.value.trim()) {
      el.style.borderColor = 'var(--error)';
      valid = false;
    } else {
      el.style.borderColor = '';
    }
  });
  return valid;
}


// ── PROGRESS BAR ANIMATION ─────────────────────────────────────────────────

function animateProgressBars() {
  document.querySelectorAll('.progress-bar[data-width]').forEach(bar => {
    setTimeout(() => {
      bar.style.width = bar.dataset.width + '%';
    }, 100);
  });
}


// ── AUTO-DISMISS ALERTS ────────────────────────────────────────────────────

function initAlerts() {
  const container = document.getElementById('alertContainer');
  if (!container) return;
  setTimeout(() => {
    container.style.transition = 'opacity 0.5s';
    container.style.opacity = '0';
    setTimeout(() => container.remove(), 500);
  }, 4000);
}


// ── QUIZ COUNTER ────────────────────────────────────────────────────────────

function initQuizCounter() {
  const counter = document.getElementById('answeredCount');
  const btn = document.getElementById('submitBtn');
  const note = document.getElementById('completeNote');
  if (!counter || !btn) return;

  const total = parseInt(document.getElementById('quizTotalHidden')?.value || '0');

  function update() {
    const names = new Set();
    document.querySelectorAll('input[type="radio"]:checked').forEach(r => names.add(r.name));
    counter.textContent = names.size;
    if (names.size >= total && total > 0) {
      btn.disabled = false;
      if (note) { note.textContent = '✓ All answered! Ready to submit.'; note.style.color = 'var(--success)'; }
    }
  }

  document.querySelectorAll('input[type="radio"]').forEach(r => r.addEventListener('change', update));
}


// ── OPTION CARD KEYBOARD NAV ───────────────────────────────────────────────

function initOptionCards() {
  document.querySelectorAll('.option-card label').forEach(label => {
    label.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        const input = label.previousElementSibling;
        if (input?.type === 'radio') { input.checked = true; input.dispatchEvent(new Event('change')); }
      }
    });
    label.setAttribute('tabindex', '0');
  });
}


// ── MODULE COMPLETION CHECK ────────────────────────────────────────────────

function initModuleForm() {
  const form = document.getElementById('assessForm');
  const btn  = document.getElementById('completeBtn');
  if (!form || !btn) return;

  const totalQ = form.querySelectorAll('.assess-question').length;

  function check() {
    const answered = new Set();
    form.querySelectorAll('input[type="radio"]:checked').forEach(r => answered.add(r.name));
    btn.disabled = answered.size < totalQ;
  }

  form.querySelectorAll('input[type="radio"]').forEach(r => r.addEventListener('change', check));
}


// ── GENERATE PATH LOADING ──────────────────────────────────────────────────

function initGeneratePath() {
  const link = document.querySelector('[data-generate-path]');
  if (!link) return;
  link.addEventListener('click', e => {
    LoadingOverlay.show([
      '🔍 Encoding your learning goal with BERT',
      '🧠 Retrieving similar learner cases (CBR)',
      '⚖️  Computing similarity scores',
      '🔧 Applying personalization rules (RBR)',
      '✅ Building your learning path',
    ]);
  });
}


// ── SMOOTH SCROLL ─────────────────────────────────────────────────────────

function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const target = document.querySelector(a.getAttribute('href'));
      if (target) { e.preventDefault(); target.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
    });
  });
}


// ── COPY TO CLIPBOARD ─────────────────────────────────────────────────────

function copyToClipboard(text, btn) {
  navigator.clipboard.writeText(text).then(() => {
    const orig = btn.textContent;
    btn.textContent = '✓ Copied!';
    btn.style.color = 'var(--success)';
    setTimeout(() => { btn.textContent = orig; btn.style.color = ''; }, 2000);
  });
}


// ── DOMAIN DETECTION (profile form) ───────────────────────────────────────

const DOMAIN_KW = {
  cybersecurity: ['hack','security','pentest','penetration','cyber','ctf','malware','firewall'],
  data_science:  ['data science','machine learning','ml','ai','neural','analytics','deep learning'],
  web_development: ['web','frontend','backend','html','css','javascript','react','node','api'],
  cloud_computing: ['cloud','aws','azure','gcp','docker','kubernetes','devops'],
  programming:   ['programming','coding','algorithm','software','java','python','data structure'],
};

function detectDomain(text) {
  text = text.toLowerCase();
  let best = '', bestScore = 0;
  for (const [domain, kws] of Object.entries(DOMAIN_KW)) {
    const score = kws.filter(k => text.includes(k)).length;
    if (score > bestScore) { bestScore = score; best = domain; }
  }
  return bestScore > 0 ? best : null;
}

function initDomainDetection() {
  const input = document.getElementById('goalInput');
  const div   = document.getElementById('domainDetected');
  const span  = document.getElementById('domainText');
  if (!input || !div || !span) return;
  input.addEventListener('input', () => {
    const domain = detectDomain(input.value);
    if (domain) {
      span.textContent = domain.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
      div.style.display = 'block';
    } else {
      div.style.display = 'none';
    }
  });
}


// ── INIT ALL ──────────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
  animateProgressBars();
  initAlerts();
  initQuizCounter();
  initOptionCards();
  initModuleForm();
  initGeneratePath();
  initSmoothScroll();
  initDomainDetection();
});
