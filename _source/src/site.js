(function(){
  var d = document, w = window, root = d.documentElement;
  var reduced = w.matchMedia && w.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var SVGNS = 'http://www.w3.org/2000/svg';
  function $(s, el){ return (el || d).querySelector(s); }
  function $$(s, el){ return Array.prototype.slice.call((el || d).querySelectorAll(s)); }
  function clamp(v, a, b){ return v < a ? a : v > b ? b : v; }
  function el(tag, attrs, parent){
    var n = d.createElementNS(SVGNS, tag);
    for(var k in attrs){ n.setAttribute(k, attrs[k]); }
    if(parent){ parent.appendChild(n); }
    return n;
  }

  /* ---------------- header: tuck away on scroll down, return on scroll up ---------------- */
  var header = $('.site-header'), lastY = w.scrollY;
  function headerOnScroll(y){
    if(!header || d.body.classList.contains('nav-open')) return;
    var down = y > lastY && y > 140;
    header.classList.toggle('tuck', down);
    lastY = y;
  }

  /* ---------------- mobile navigation ---------------- */
  var btn = $('.menu-btn'), panel = d.getElementById('mobile-nav');
  function setMenu(open){
    if(!btn || !panel) return;
    btn.setAttribute('aria-expanded', String(open));
    btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    panel.hidden = !open;
    d.body.classList.toggle('nav-open', open);
    if(open){ header.classList.remove('tuck'); }
  }
  if(btn && panel){
    btn.addEventListener('click', function(){ setMenu(btn.getAttribute('aria-expanded') !== 'true'); });
    $$('a', panel).forEach(function(a){ a.addEventListener('click', function(){ setMenu(false); }); });
    d.addEventListener('keydown', function(e){ if(e.key === 'Escape'){ setMenu(false); } });
    w.addEventListener('resize', function(){ if(w.innerWidth > 920){ setMenu(false); } });
  }

  /* ---------------- artwork: draw in once, loop only while on screen ---------------- */
  var arts = $$('[data-art]');
  if(reduced || !('IntersectionObserver' in w)){
    arts.forEach(function(a){ a.classList.add('on'); });
  } else {
    var artIO = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if(e.isIntersecting){ e.target.classList.add('on'); }
        e.target.classList.toggle('run', e.isIntersecting);
      });
    }, { threshold:0.18 });
    arts.forEach(function(a){
      // the hero draws itself as part of the page-load sequence
      if(a.classList.contains('hero-art') || a.classList.contains('phero-art')){ setTimeout(function(){ a.classList.add('on', 'run'); }, 250); }
      artIO.observe(a);
    });
  }

  /* ---------------- pinned stages ---------------- */
  var pins = $$('[data-pin]');
  var hscrolls = $$('[data-hscroll]');
  var sequences = $$('[data-seq]');
  var scrubs = $$('[data-scrub]');

  function sizePins(){
    if(reduced) return;
    var vh = w.innerHeight;
    pins.forEach(function(p){
      if(p.hasAttribute('data-hscroll')){
        var track = $('.track', p), vp = $('.track-viewport', p);
        var travel = Math.max(0, track.scrollWidth - vp.clientWidth);
        p._travel = travel;
        p.style.height = (vh + travel * 1.1) + 'px';
      } else {
        var steps = +p.getAttribute('data-steps') || 0;
        p.style.setProperty('--len', steps ? steps * 0.85 + 0.6 : 2.4);
      }
    });
  }

  function updatePins(vh){
    pins.forEach(function(p){
      var r = p.getBoundingClientRect();
      var span = r.height - vh;
      var prog = span > 0 ? clamp(-r.top / span, 0, 1) : 0;
      p.style.setProperty('--p', prog.toFixed(4));
      var steps = +p.getAttribute('data-steps');
      if(steps){
        var s = Math.min(steps, Math.floor(prog * steps) + 1);
        if(p.getAttribute('data-step') !== String(s)){ p.setAttribute('data-step', s); }
        if(p.classList.contains('gap')){
          var inside = r.top < vh * 0.5 && r.bottom > vh * 0.5;
          d.body.classList.toggle('fault', inside && s === steps);
        }
      }
      if(p._travel !== undefined){
        var track = $('.track', p);
        track.style.transform = 'translate3d(' + (-prog * p._travel).toFixed(1) + 'px,0,0)';
        var cards = $$('.svc', p), n = cards.length;
        var idx = Math.round(prog * (n - 1));
        $$('.rack i', p).forEach(function(b, i){ b.classList.toggle('on', i <= idx); });
        cards.forEach(function(c, i){ var a = $('.art', c); if(a && i === idx){ a.classList.add('on'); } });
      }
    });
    scrubs.forEach(function(s){
      var r = s.getBoundingClientRect();
      var prog = clamp((vh * 0.3 - r.top) / Math.max(1, r.height - vh * 1.1), 0, 1);
      s.style.setProperty('--p', prog.toFixed(4));
    });
    sequences.forEach(function(s){
      var r = s.getBoundingClientRect();
      var prog = clamp((vh * 0.85 - r.top) / (vh * 0.55), 0, 1);
      s.style.setProperty('--p', prog.toFixed(3));
      var items = $$('li', s);
      items.forEach(function(li, i){ li.classList.toggle('lit', prog >= (i + 0.5) / items.length - 0.02 || prog >= 0.999); });
    });
  }

  /* ---------------- the busbar: one conductor drawn down the page by scrolling ---------------- */
  var bus = null;
  function buildBus(){
    var nodes = $$('.node').filter(function(n){ return n.offsetParent !== null || n.getClientRects().length; });
    if(nodes.length < 2){ if(bus){ bus.svg.remove(); bus = null; } return; }
    if(!bus){
      var svg = el('svg', { 'class':'busbar', 'aria-hidden':'true' });
      d.body.appendChild(svg);
      bus = { svg:svg };
      bus.track = el('path', { 'class':'track' }, svg);
      bus.live = el('path', { 'class':'live' }, svg);
      bus.syms = el('g', {}, svg);
      bus.pulses = [];
      if(!reduced){ for(var i = 0; i < 4; i++){ bus.pulses.push(el('circle', { 'class':'pz', r:3.6 }, svg)); } }
      bus.ring = el('circle', { 'class':'tipring', r:6 }, svg);
      bus.tip = el('circle', { 'class':'tip', r:6 }, svg);
      bus.drawn = 0;
    }
    bus.svg.setAttribute('width', 0); bus.svg.setAttribute('height', 0);
    var W = root.clientWidth, H = root.scrollHeight;
    var sx = w.scrollX, sy = w.scrollY;
    var pts = nodes.map(function(n){
      var r = n.getBoundingClientRect();
      return { x:Math.round(r.left + sx), y:Math.round(r.top + sy), kind:n.getAttribute('data-kind') || 'breaker', route:n.getAttribute('data-route') || 'vh' };
    });
    // orthogonal route through every node, in document order
    var segs = [], cum = 0, dstr = 'M' + pts[0].x + ' ' + pts[0].y;
    pts[0].len = 0;
    function seg(x1, y1, x2, y2){
      var len = Math.abs(x2 - x1) + Math.abs(y2 - y1);
      if(!len) return;
      segs.push({ x1:x1, y1:y1, x2:x2, y2:y2, len:len, at:cum });
      cum += len;
      dstr += ' L' + x2 + ' ' + y2;
    }
    for(var i = 1; i < pts.length; i++){
      var a = pts[i - 1], b = pts[i];
      if(b.route === 'hv'){ seg(a.x, a.y, b.x, a.y); seg(b.x, a.y, b.x, b.y); }
      else { seg(a.x, a.y, a.x, b.y); seg(a.x, b.y, b.x, b.y); }
      b.len = cum;
    }
    bus.segs = segs; bus.total = cum; bus.pts = pts;
    bus.svg.setAttribute('width', W); bus.svg.setAttribute('height', H);
    bus.svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
    bus.track.setAttribute('d', dstr);
    bus.live.setAttribute('d', dstr);
    bus.live.style.strokeDasharray = cum + ' ' + (cum + 10);
    // device symbols
    bus.syms.textContent = '';
    var small = W < 760 ? 0.75 : 1;
    pts.forEach(function(p){
      var g = el('g', { transform:'translate(' + p.x + ' ' + p.y + ') scale(' + small + ')' }, bus.syms);
      var s;
      if(p.kind === 'source'){
        s = el('circle', { 'class':'sym', r:12 }, g);
        el('path', { 'class':'symline', d:'M-6 0 q3 -6 6 0 t6 0' }, g);
      } else if(p.kind === 'transformer'){
        el('circle', { 'class':'sym', cy:-7, r:10 }, g);
        s = el('circle', { 'class':'sym', cy:7, r:10 }, g);
      } else if(p.kind === 'earth'){
        s = el('path', { 'class':'symline earth', d:'M-15 0 H15 M-9 7 H9 M-4 14 H4' }, g);
      } else {
        s = el('rect', { 'class':'sym', x:-9, y:-9, width:18, height:18 }, g);
      }
      p.sym = s; p.g = g;
    });
    if(reduced){ bus.drawn = cum; }
    paintBus(true);
  }

  function targetLength(){
    var y = w.scrollY + w.innerHeight * 0.62;
    var L = 0;
    for(var i = 0; i < bus.segs.length; i++){
      var s = bus.segs[i];
      var top = Math.min(s.y1, s.y2), bot = Math.max(s.y1, s.y2);
      if(s.y1 === s.y2){ if(y >= s.y1){ L = s.at + s.len; continue; } return L; }
      if(y >= bot){ L = s.at + s.len; continue; }
      if(y > top){ return s.at + (y - top); }
      return L;
    }
    return bus.total;
  }

  function pointAt(len){
    var s = bus.segs[0];
    for(var i = 0; i < bus.segs.length; i++){ s = bus.segs[i]; if(len <= s.at + s.len) break; }
    var t = s.len ? clamp((len - s.at) / s.len, 0, 1) : 0;
    return { x:s.x1 + (s.x2 - s.x1) * t, y:s.y1 + (s.y2 - s.y1) * t };
  }

  function paintBus(force){
    if(!bus || !bus.segs.length) return;
    var target = reduced ? bus.total : targetLength();
    var diff = target - bus.drawn;
    if(!force && Math.abs(diff) < 0.4 && !bus.pulses.length) return;
    bus.drawn += reduced || force ? diff : diff * 0.14;
    var L = bus.drawn;
    bus.live.style.strokeDashoffset = 0;
    bus.live.style.strokeDasharray = L.toFixed(1) + ' ' + (bus.total + 10);
    var tp = pointAt(L);
    bus.tip.setAttribute('cx', tp.x); bus.tip.setAttribute('cy', tp.y);
    bus.ring.setAttribute('cx', tp.x); bus.ring.setAttribute('cy', tp.y);
    var done = L >= bus.total - 1;
    bus.tip.style.opacity = bus.ring.style.opacity = done ? 0 : 1;
    bus.pts.forEach(function(p){
      var closed = L >= p.len - 2;
      if(closed !== !!p.closed){
        p.closed = closed;
        $$('.sym', p.g).forEach(function(s){
          s.classList.toggle('closed', closed);
          if(closed && !force){ s.classList.remove('pop'); void s.getBBox(); s.classList.add('pop'); }
        });
      }
    });
    // current pulses travel along the energised part
    var now = performance.now() / 1000;
    bus.pulses.forEach(function(c, i){
      if(L < 40){ c.style.opacity = 0; return; }
      var span = Math.min(L, 2600);
      var pos = L - span + ((now * 160 + i * span / bus.pulses.length) % span);
      var q = pointAt(pos);
      c.style.opacity = 1;
      c.setAttribute('cx', q.x.toFixed(1)); c.setAttribute('cy', q.y.toFixed(1));
    });
  }

  /* ---------------- Africa map: sectors light up their regions ---------------- */
  $$('[data-map]').forEach(function(fig){
    var map = $('.map', fig);
    var list = fig.parentElement && $('.sector-list', fig.parentElement);
    if(!map || !list) return;
    var links = $$('a[data-sector]', list), touched = false, i = 0, timer = null;
    function show(sector){
      if(sector){ map.setAttribute('data-active', sector); } else { map.removeAttribute('data-active'); }
      links.forEach(function(a){ a.classList.toggle('on', a.getAttribute('data-sector') === sector); });
    }
    links.forEach(function(a){
      function on(){ touched = true; clearInterval(timer); show(a.getAttribute('data-sector')); }
      a.addEventListener('mouseenter', on); a.addEventListener('focus', on);
    });
    list.addEventListener('mouseleave', function(){ show(null); });
    if(reduced || !('IntersectionObserver' in w)) return;
    new IntersectionObserver(function(es){
      es.forEach(function(e){
        clearInterval(timer);
        if(e.isIntersecting && !touched){
          timer = setInterval(function(){ if(touched){ return clearInterval(timer); } show(links[i % links.length].getAttribute('data-sector')); i++; }, 2200);
        }
      });
    }, { threshold:0.4 }).observe(fig);
  });

  /* ---------------- main loop ---------------- */
  var ticking = false;
  function frame(){
    var vh = w.innerHeight;
    if(!reduced){ updatePins(vh); }
    paintBus(false);
    if(bus && bus.pulses.length){ requestAnimationFrame(frame); } else { ticking = false; }
  }
  function kick(){ if(!ticking){ ticking = true; requestAnimationFrame(frame); } }
  w.addEventListener('scroll', function(){ headerOnScroll(w.scrollY); kick(); }, { passive:true });

  var layoutTimer;
  function relayout(){
    clearTimeout(layoutTimer);
    layoutTimer = setTimeout(function(){ sizePins(); if(!reduced){ updatePins(w.innerHeight); } buildBus(); kick(); }, 60);
  }
  w.addEventListener('resize', relayout);
  w.addEventListener('load', relayout);
  if(d.fonts && d.fonts.ready){ d.fonts.ready.then(relayout); }
  if('ResizeObserver' in w){
    var lastH = 0;
    new ResizeObserver(function(){ var h = d.body.offsetHeight; if(Math.abs(h - lastH) > 4){ lastH = h; relayout(); } }).observe(d.body);
  }
  $$('details').forEach(function(x){ x.addEventListener('toggle', relayout); });
  sizePins(); if(!reduced){ updatePins(w.innerHeight); }
  buildBus(); kick();

  /* spec sheets and other one-shot reveals */
  if(!reduced && 'IntersectionObserver' in w){
    var once = new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('on'); once.unobserve(e.target); } }); }, { threshold:0.25 });
    $$('.spec').forEach(function(s){ once.observe(s); });
  } else { $$('.spec').forEach(function(s){ s.classList.add('on'); }); }

  /* label table cells so the comparison tables can stack on phones */
  $$('.spec-table').forEach(function(t){
    var heads = $$('thead th', t).map(function(th){ return th.textContent.trim(); });
    $$('tbody tr', t).forEach(function(tr){ $$('td', tr).forEach(function(td){ td.setAttribute('data-label', heads[td.cellIndex] || ''); }); });
  });

  /* current year */
  $$('[data-year]').forEach(function(x){ x.textContent = new Date().getFullYear(); });

  /* ---------------- contact form ----------------
     Sends the enquiry to Netlify Forms, then shows the thank-you page.
     Submissions are stored in Netlify (Forms > briefing-request) and emailed to you
     via Site configuration > Notifications > Form submission notifications.
     If JavaScript is off, the form still posts to Netlify normally. */
  var form = $('form[data-netlify]');
  if(form){
    var status = $('.form-status', form);
    var submit = $('button[type="submit"]', form);
    var sending = false;
    form.addEventListener('submit', function(e){
      e.preventDefault();
      if(sending) return;
      if(!form.checkValidity()){ form.reportValidity(); return; }
      sending = true;
      if(submit){ submit.disabled = true; }
      if(status){ status.classList.remove('is-error'); status.textContent = 'Sending your request…'; }
      fetch('/', {
        method:'POST',
        headers:{ 'Content-Type':'application/x-www-form-urlencoded' },
        body:new URLSearchParams(new FormData(form)).toString()
      })
      .then(function(res){
        if(!res.ok){ throw new Error('HTTP ' + res.status); }
        w.location.href = form.getAttribute('action') || '/thank-you';
      })
      .catch(function(){
        sending = false;
        if(submit){ submit.disabled = false; }
        if(status){
          status.classList.add('is-error');
          status.innerHTML = 'Your request wasn’t sent. Try again, or email <a href="mailto:info@machina-logic.com">info@machina-logic.com</a>.';
        }
      });
    });
  }
})();
