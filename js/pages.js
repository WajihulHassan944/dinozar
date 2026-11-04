/* ===== shared page behaviour: menu, sticky header, filters, gallery, stories, forms ===== */
(function () {
  var root = document.documentElement;
  var $ = function (q, c) { return (c || document).querySelector(q); };
  var $$ = function (q, c) { return [].slice.call((c || document).querySelectorAll(q)); };
  var fmt = function (d) { return new Date(d + 'T00:00:00').toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' }); };
  var arrow = '<svg viewBox="0 0 14 10"><path d="M0 5h12M8 1l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1"/></svg>';
  var lenisStop = function () { if (window.__lenis) window.__lenis.stop(); };
  var lenisGo = function () { if (window.__lenis) window.__lenis.start(); };

  /* full-screen menu */
  var mo = $('#mo'), btn = $('.menu');
  function menu(open) {
    if (!mo) return;
    mo.classList.toggle('open', open);
    root.classList.toggle('menu-open', open);
    btn.setAttribute('aria-expanded', String(open));
    mo.setAttribute('aria-hidden', String(!open));
    open ? lenisStop() : lenisGo();
    document.body.style.overflow = open ? 'hidden' : '';
  }
  if (btn && mo) {
    btn.addEventListener('click', function () { menu(!mo.classList.contains('open')); });
    addEventListener('keydown', function (e) { if (e.key === 'Escape') menu(false); });
    $$('a', mo).forEach(function (a) {
      a.addEventListener('click', function () {
        var h = a.getAttribute('href') || '';
        var file = h.split('#')[0];
        if (h.indexOf('#') === 0 || (file && file === location.pathname.split('/').pop())) menu(false);
      });
    });
  }

  /* header: sticky, hides on scroll down, returns on scroll up */
  var hd = $('header'), lastY = 0;
  if (hd) {
    addEventListener('scroll', function () {
      var y = scrollY;
      if (root.classList.contains('menu-open')) return;
      hd.classList.toggle('stuck', y > 140);
      if (y > 420 && y > lastY + 2) hd.classList.add('hide');
      else if (y < lastY - 2) hd.classList.remove('hide');
      lastY = y;
    }, { passive: true });
  }

  /* timeline progress line */
  $$('.tl').forEach(function (t) {
    function up() {
      var r = t.getBoundingClientRect(), p = (innerHeight * 0.6 - r.top) / r.height;
      t.style.setProperty('--p', Math.max(0, Math.min(1, p)).toFixed(3));
    }
    addEventListener('scroll', up, { passive: true });
    addEventListener('resize', up);
    up();
  });

  /* generic list filter (wiki) */
  var si = $('[data-filter-input]');
  if (si) {
    var items = $$('[data-filter-item]'), chips = $$('[data-chip]'), empty = $('.empty'), cur = 'all';
    var run = function () {
      var q = si.value.trim().toLowerCase(), n = 0;
      items.forEach(function (it) {
        var ok = (cur === 'all' || it.dataset.letter === cur) && (!q || it.textContent.toLowerCase().indexOf(q) > -1);
        it.hidden = !ok;
        if (ok) n++;
      });
      if (empty) empty.hidden = n > 0;
    };
    si.addEventListener('input', run);
    chips.forEach(function (c) {
      c.addEventListener('click', function () {
        cur = c.dataset.chip;
        chips.forEach(function (x) { x.classList.toggle('on', x === c); });
        run();
      });
    });
  }

  /* gallery: filter (sliding indicator) + premium lightbox (counter, thumbnails, swipe) */
  var gal = $('.gal');
  if (gal) {
    var gs = $$('.g', gal), gc = $$('[data-gcat]'), lb = $('#lb'), idx = 0, vis = [], ind = $('.gf-ind'),
        thumbs = $$('.lb-t', lb), big = $('.lb-img img', lb), bg = $('.lb-bg img', lb);
    var moveInd = function (c) { if (!ind || !c) return; ind.style.width = c.offsetWidth + 'px'; ind.style.transform = 'translateX(' + c.offsetLeft + 'px)'; };
    gc.forEach(function (c) {
      c.addEventListener('click', function () {
        gc.forEach(function (x) { x.classList.toggle('on', x === c); x.setAttribute('aria-selected', x === c); });
        moveInd(c);
        gal.classList.toggle('filtered', c.dataset.gcat !== 'all');
        gs.forEach(function (g) {
          var keep = c.dataset.gcat === 'all' || g.dataset.cat === c.dataset.gcat;
          if (keep && g.hidden) {
            g.hidden = false; g.classList.add('g-in');
            requestAnimationFrame(function () { requestAnimationFrame(function () { g.classList.toggle('g-in', false); }); });
          } else if (!keep) { g.hidden = true; }
        });
      });
    });
    moveInd($('[data-gcat].on'));
    addEventListener('resize', function () { moveInd($('[data-gcat].on')); });
    addEventListener('load', function () { moveInd($('[data-gcat].on')); });
    var show = function (i) {
      vis = gs.filter(function (g) { return !g.hidden; });
      idx = (i + vis.length) % vis.length;
      var g = vis[idx], src = $('img', g).src;
      big.classList.toggle('in', false); void big.offsetWidth;
      big.src = src; bg.src = src; big.alt = $('img', g).alt;
      big.classList.toggle('in', true);
      $('.lb-ttl', lb).textContent = $('b', g).textContent;
      $('small', lb).textContent = $('figcaption small', g).textContent + ' · ' + $('figcaption span', g).textContent;
      $('.lb-i', lb).textContent = (idx < 9 ? '0' : '') + (idx + 1);
      $('.lb-n', lb).textContent = (vis.length < 10 ? '0' : '') + vis.length;
      thumbs.forEach(function (t, k) { t.hidden = gs[k].hidden; t.classList.toggle('on', gs[k] === g); });
      var at = thumbs[gs.indexOf(g)];
      if (at && lb.classList.contains('open')) at.scrollIntoView({ block: 'nearest', inline: 'center', behavior: 'smooth' });
    };
    var openLb = function (g) {
      show(gs.filter(function (x) { return !x.hidden; }).indexOf(g));
      lb.classList.add('open'); lb.setAttribute('aria-hidden', 'false'); lenisStop();
      $('.x', lb).focus({ preventScroll: true });
    };
    var closeLb = function () { lb.classList.toggle('open', false); lb.setAttribute('aria-hidden', 'true'); lenisGo(); };
    gs.forEach(function (g) {
      g.addEventListener('click', function () { openLb(g); });
      g.addEventListener('pointermove', function (e) {
        var r = g.getBoundingClientRect();
        g.style.setProperty('--x', (e.clientX - r.left) + 'px'); g.style.setProperty('--y', (e.clientY - r.top) + 'px');
      });
    });
    thumbs.forEach(function (t, k) { t.addEventListener('click', function () { show(vis.indexOf(gs[k])); }); });
    $('.x', lb).addEventListener('click', closeLb);
    $('.pv', lb).addEventListener('click', function () { show(idx - 1); });
    $('.nx', lb).addEventListener('click', function () { show(idx + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb || e.target.classList.contains('lb-img')) closeLb(); });
    var sx = null;
    lb.addEventListener('pointerdown', function (e) { sx = e.clientX; });
    lb.addEventListener('pointerup', function (e) {
      if (sx === null) return; var dx = e.clientX - sx; sx = null;
      if (Math.abs(dx) > 50) show(idx + (dx < 0 ? 1 : -1));
    });
    addEventListener('keydown', function (e) {
      if (!lb.classList.contains('open')) return;
      if (e.key === 'Escape') closeLb();
      if (e.key === 'ArrowLeft') show(idx - 1);
      if (e.key === 'ArrowRight') show(idx + 1);
    });
  }

  /* stories list: category tabs, search, pagination */
  var list = $('#posts');
  if (list && window.POSTS) {
    var P = window.POSTS, PER = 7, page = 1, cat = 'all', q = '';
    var fq = $('#st-q'), tabs = $$('[data-cat]'), pg = $('#pager');
    var card = function (p, i, feat) {
      var cats = p.cats.map(function (c) { return '<span>' + c + '</span>'; }).join('');
      return '<a class="post' + (feat ? ' feature' : '') + '" style="--i:' + i + '" href="post.html?p=' + p.slug + '"' + (p.lang ? ' lang="' + p.lang + '"' : '') + '>'
        + '<div class="ph"><img loading="lazy" src="images/' + p.img + '" alt=""><div class="badge">' + cats + '</div></div>'
        + '<div class="tx"><div class="meta"><span>' + fmt(p.date) + '</span>' + (p.locked ? '<span class="lock">&#9679; Protected</span>' : '') + (p.tag ? '<span>#' + p.tag + '</span>' : '') + '</div>'
        + '<h3>' + (p.locked ? 'Protected: ' : '') + p.title + '</h3><p>' + p.excerpt + '</p><span class="more">Read story ' + arrow + '</span></div></a>';
    };
    var filtered = function () {
      return P.filter(function (p) {
        return (cat === 'all' || p.cats.indexOf(cat) > -1) && (!q || (p.title + ' ' + p.excerpt).toLowerCase().indexOf(q) > -1);
      });
    };
    var render = function () {
      var f = filtered(), pages = Math.max(1, Math.ceil(f.length / PER));
      page = Math.min(page, pages);
      var slice = f.slice((page - 1) * PER, page * PER);
      list.innerHTML = slice.length
        ? slice.map(function (p, i) { return card(p, i, i === 0 && page === 1 && cat === 'all' && !q); }).join('')
        : '<p class="empty" style="grid-column:1/-1">No stories match your search.</p>';
      var h = '';
      if (pages > 1) {
        h += '<button class="nx" data-p="' + (page - 1) + '"' + (page === 1 ? ' disabled' : '') + '>Prev</button>';
        for (var i = 1; i <= pages; i++) h += '<button data-p="' + i + '" class="' + (i === page ? 'on' : '') + '">' + i + '</button>';
        h += '<button class="nx" data-p="' + (page + 1) + '"' + (page === pages ? ' disabled' : '') + '>Next</button>';
      }
      pg.innerHTML = h;
    };
    pg.addEventListener('click', function (e) {
      var b = e.target.closest('button');
      if (!b) return;
      page = +b.dataset.p; render();
      $('#st-top').scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
    var setTab = function (t) { cat = t.dataset.cat; tabs.forEach(function (x) { x.classList.toggle('on', x === t); }); };
    tabs.forEach(function (t) {
      t.addEventListener('click', function () {
        setTab(t); page = 1;
        history.replaceState(null, '', '#' + (cat === 'all' ? '' : encodeURIComponent(cat)));
        render();
      });
    });
    fq.addEventListener('input', function () { q = fq.value.trim().toLowerCase(); page = 1; render(); });
    var hs = decodeURIComponent(location.hash.slice(1));
    if (hs) {
      var t0 = tabs.filter(function (x) { return x.dataset.cat.toLowerCase() === hs.toLowerCase(); })[0];
      if (t0) setTab(t0);
    }
    render();
    var rc = $('#recent');
    if (rc) rc.innerHTML = P.slice(0, 5).map(function (p) { return '<li><a href="post.html?p=' + p.slug + '">' + p.title + '<small>' + fmt(p.date) + '</small></a></li>'; }).join('');
  }

  /* single story template */
  var art = $('#article');
  if (art && window.POSTS) {
    var P2 = window.POSTS;
    var slug = new URLSearchParams(location.search).get('p') || location.hash.slice(1);
    var i2 = P2.findIndex(function (p) { return p.slug === slug; });
    if (i2 < 0) i2 = 0;
    var p = P2[i2];
    document.title = p.title + ' – Dex World';
    $('#a-title').textContent = (p.locked ? 'Protected: ' : '') + p.title;
    $('#a-cats').textContent = p.cats.join(' · ') + ' — ' + fmt(p.date);
    $('#a-crumb').textContent = p.title.length > 34 ? p.title.slice(0, 34) + '…' : p.title;
    $('.cover img', art).src = 'images/' + p.img;
    $('#a-body').innerHTML = p.locked
      ? '<p class="big">This story is password protected.</p><form class="cf" onsubmit="return false" style="max-width:420px;margin-top:30px"><div class="fld"><label for="pw">Password</label><input id="pw" type="password" autocomplete="off"></div><button class="btn" type="submit">Unlock ' + arrow + '</button></form>'
      : '<p class="big">' + p.excerpt + '</p><div class="note">Placeholder article body. The full story text will be migrated here from the existing site (or pulled from the CMS). This page is the single-story template: cover image, meta line, lead paragraph, body, and previous / next navigation.</div>';
    var older = P2[i2 + 1], newer = P2[i2 - 1];
    $('#a-nav').innerHTML = (older ? '<a class="btn" href="post.html?p=' + older.slug + '">&larr; Older</a>' : '<span></span>')
      + (newer ? '<a class="btn" href="post.html?p=' + newer.slug + '">Newer ' + arrow + '</a>' : '<span></span>');
  }

  /* contact form: front-end validation only; wire it to a back end later */
  var cf = $('#cf');
  if (cf) {
    cf.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true;
      $$('.fld[data-req]', cf).forEach(function (f) {
        var i = $('input,textarea', f), v = i.value.trim();
        var bad = !v || (i.type === 'email' && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v));
        f.classList.toggle('err', bad);
        if (bad) ok = false;
      });
      var c = $('#consent');
      c.closest('.chk').style.color = c.checked ? '' : '#d9826e';
      if (!c.checked) ok = false;
      if (!ok) return;
      cf.hidden = true;
      $('#cf-ok').classList.add('show');
      $('#cf-ok').scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
    $$('.fld input,.fld textarea', cf).forEach(function (i) {
      i.addEventListener('input', function () { i.closest('.fld').classList.remove('err'); });
    });
  }

  /* privacy table of contents highlight */
  var toc = $$('.toc a');
  if (toc.length && 'IntersectionObserver' in window) {
    var io2 = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) toc.forEach(function (a) { a.classList.toggle('on', a.getAttribute('href') === '#' + e.target.id); });
      });
    }, { rootMargin: '-30% 0px -60% 0px' });
    toc.forEach(function (a) { var s = $(a.getAttribute('href')); if (s) io2.observe(s); });
  }
})();
