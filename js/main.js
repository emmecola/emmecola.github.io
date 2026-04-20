/* ── DNA Background (inside hero) ───────────────────────────────────── */
(function () {
  'use strict';

  var bases = ['A', 'T', 'C', 'G'];
  var bgColors = ['var(--dna-A)', 'var(--dna-T)', 'var(--dna-G)', 'var(--dna-C)'];

  var bg = document.getElementById('seqBg');
  if (!bg) return;

  /* Match row count to actual hero height */
  var heroHeight = bg.parentElement.offsetHeight || 300;
  var rows = Math.ceil(heroHeight / 19) + 2;

  for (var r = 0; r < rows; r++) {
    var el = document.createElement('div');
    el.className = 'seq-row';

    /* Double-length text for seamless drift loop */
    var rowHalf = '';
    for (var c = 0; c < 280; c++) {
      rowHalf += bases[(Math.random() * 4) | 0] + '\u00a0';
    }
    el.textContent = rowHalf + rowHalf;

    el.style.color             = bgColors[(Math.random() * 4) | 0];
    var dur                    = 55 + Math.random() * 70;
    el.style.animationDuration = dur + 's';
    el.style.animationDelay    = (-Math.random() * dur) + 's';
    el.style.opacity           = (0.08 + Math.random() * 0.10).toFixed(3);
    
    // Randomly assign animation direction (50% chance for each direction)
    if (Math.random() > 0.5) {
      el.style.animationName = 'seq-drift-reverse';
    }

    bg.appendChild(el);
  }
}());

/* ── Markdown loader ─────────────────────────────────────────────────── */
(function () {
  'use strict';

  function loadMarkdown(url, elementId) {
    var el = document.getElementById(elementId);
    if (!el) return;

    if (typeof marked === 'undefined') {
      el.innerHTML = '<p class="load-error">Markdown library not loaded.</p>';
      return;
    }

    fetch(url)
      .then(function (res) {
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return res.text();
      })
      .then(function (md) {
        el.innerHTML = marked.parse(md);
      })
      .catch(function (err) {
        console.warn('Could not load ' + url + ' \u2014 ' + err.message);
        el.innerHTML = '<p class="load-error">Serve over HTTP to load content (e.g.&nbsp;python3 -m http.server)</p>';
      });
  }

  loadMarkdown('content/summary.md',      'summary-content');
  loadMarkdown('content/skills.md',      'skills-content');
  loadMarkdown('content/projects.md',    'projects-content');
  loadMarkdown('content/publications.md','publications-content');
}());

/* ── ROT13 string encoder & email decoder ────────────────────────────── */
(function () {
  'use strict';

  function rot13(str) {
    return str.replace(/[a-zA-Z]/g, function(c) {
      return String.fromCharCode(
        (c <= 'Z' ? 90 : 122) >= (c = c.charCodeAt(0) + 13) ? c : c - 26
      );
    });
  }

  /* Decode email links on page load */
  var emailLinks = document.querySelectorAll('.email-link[data-email]');
  for (var i = 0; i < emailLinks.length; i++) {
    var link = emailLinks[i];
    var encoded = link.getAttribute('data-email');
    if (encoded) {
      var decoded = rot13(encoded);
      link.href = 'mailto:' + decoded;
      link.setAttribute('aria-label', 'Email: ' + decoded);
    }
  }

  /* Expose rot13 globally if needed */
  window.rot13 = rot13;
}());
