(function(){
  var d = document;
  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* header shadow on scroll */
  var header = d.querySelector('.site-header');
  function onScroll(){ if(header){ header.classList.toggle('scrolled', window.scrollY > 8); } }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive:true });

  /* mobile navigation */
  var btn = d.querySelector('.menu-btn');
  var panel = d.getElementById('mobile-nav');
  function setMenu(open){
    if(!btn || !panel) return;
    btn.setAttribute('aria-expanded', String(open));
    btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    panel.hidden = !open;
    d.body.classList.toggle('nav-open', open);
  }
  if(btn && panel){
    btn.addEventListener('click', function(){ setMenu(btn.getAttribute('aria-expanded') !== 'true'); });
    panel.querySelectorAll('a').forEach(function(a){ a.addEventListener('click', function(){ setMenu(false); }); });
    d.addEventListener('keydown', function(e){ if(e.key === 'Escape'){ setMenu(false); } });
    window.addEventListener('resize', function(){ if(window.innerWidth > 920){ setMenu(false); } });
  }

  /* reveal on scroll, staggered within a group */
  var els = d.querySelectorAll('.reveal');
  if(!('IntersectionObserver' in window) || reduced){
    els.forEach(function(el){ el.classList.add('is-in'); });
  } else {
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(entry){
        if(!entry.isIntersecting) return;
        var el = entry.target;
        var group = el.parentElement;
        var sibs = group ? Array.prototype.filter.call(group.children, function(c){ return c.classList.contains('reveal'); }) : [el];
        var idx = Math.max(0, sibs.indexOf(el));
        el.style.transitionDelay = (Math.min(idx, 6) * 70) + 'ms';
        el.classList.add('is-in');
        io.unobserve(el);
      });
    }, { threshold:0.12, rootMargin:'0px 0px -40px 0px' });
    els.forEach(function(el){ io.observe(el); });
  }

  /* illustrative monitoring log in the hero console */
  var log = d.querySelector('[data-log]');
  if(log){
    var lines = [
      ['ok',   'OK  ', 'L1 PLC-01  Modbus/TCP polling matches baseline'],
      ['info', 'INFO', 'L3 HIST   Telemetry batch archived (4,812 tags)'],
      ['ok',   'OK  ', 'L2 SCADA  DNP3 integrity poll nominal'],
      ['warn', 'WARN', 'L1 PLC-02  Unscheduled logic write from ENG-WS'],
      ['act',  'ACT ', 'SOC       Analyst engaged · session captured'],
      ['ok',   'OK  ', 'L3.5 DMZ  No new inbound paths detected'],
      ['info', 'INFO', 'L2 HMI-01  Operator login (shift change)'],
      ['ok',   'OK  ', 'L1 RTU-07  IEC 104 link stable']
    ];
    var i = 0;
    function pad(n){ return (n < 10 ? '0' : '') + n; }
    function stamp(){ var t = new Date(); return pad(t.getHours()) + ':' + pad(t.getMinutes()) + ':' + pad(t.getSeconds()); }
    function push(){
      var L = lines[i % lines.length]; i++;
      var row = d.createElement('div');
      row.className = 'log-line ' + L[0];
      row.innerHTML = '<span class="t">[' + stamp() + ']</span> <span class="lv">' + L[1] + '</span> <span class="msg"></span>';
      row.querySelector('.msg').textContent = L[2];
      log.appendChild(row);
      while(log.children.length > 4){ log.removeChild(log.firstChild); }
    }
    log.innerHTML = '';
    for(var k = 0; k < 4; k++){ push(); }
    if(!reduced){ setInterval(push, 2600); }
  }

  /* current year */
  d.querySelectorAll('[data-year]').forEach(function(el){ el.textContent = new Date().getFullYear(); });

  /* contact form: sends the enquiry to Netlify Forms, then shows the thank-you page.
     Submissions are stored in Netlify (Forms > briefing-request) and emailed to you
     via Site configuration > Notifications > Form submission notifications.
     If JavaScript is off, the form still posts to Netlify normally. */
  var form = d.querySelector('form[data-netlify]');
  if(form){
    var status = form.querySelector('.form-status');
    var submit = form.querySelector('button[type="submit"]');
    var sending = false;
    form.addEventListener('submit', function(e){
      e.preventDefault();
      if(sending) return;
      if(!form.checkValidity()){ form.reportValidity(); return; }

      sending = true;
      if(submit){ submit.disabled = true; }
      if(status){ status.classList.remove('is-error'); status.textContent = 'Sending your request…'; }

      var body = new URLSearchParams(new FormData(form)).toString();
      fetch('/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: body
      })
      .then(function(res){
        if(!res.ok){ throw new Error('HTTP ' + res.status); }
        window.location.href = form.getAttribute('action') || '/thank-you';
      })
      .catch(function(){
        sending = false;
        if(submit){ submit.disabled = false; }
        if(status){
          status.classList.add('is-error');
          status.innerHTML = 'Sorry, your request could not be sent. Please try again, or email us at <a href="mailto:info@machina-logic.com">info@machina-logic.com</a>.';
        }
      });
    });
  }
})();
