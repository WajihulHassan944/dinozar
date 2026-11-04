(function(){
  var fine=matchMedia('(hover:hover) and (pointer:fine)').matches, calm=matchMedia('(prefers-reduced-motion: reduce)').matches;
  // scroll reveal
  var rv=[].slice.call(document.querySelectorAll('.reveal'));
  if(calm||!('IntersectionObserver' in window)){rv.forEach(function(e){e.classList.add('in')});}
  else{var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.15});rv.forEach(function(e){io.observe(e)});}
  if(calm) return;
  // tilt cards
  if(fine) [].forEach.call(document.querySelectorAll('[data-tilt]'),function(el){
    var max=parseFloat(el.dataset.tilt)||8, tgt=el.querySelector('.photo,.scene')||el;
    el.addEventListener('pointermove',function(ev){
      var r=el.getBoundingClientRect(), x=(ev.clientX-r.left)/r.width, y=(ev.clientY-r.top)/r.height;
      el.classList.add('live');
      el.style.transform='perspective(1000px) rotateY('+((x-.5)*2*max).toFixed(2)+'deg) rotateX('+((.5-y)*2*max).toFixed(2)+'deg)';
      tgt.style.setProperty('--gx',(x*100)+'%');tgt.style.setProperty('--gy',(y*100)+'%');tgt.style.setProperty('--go',1);
    });
    el.addEventListener('pointerleave',function(){el.classList.remove('live');el.style.transform='';tgt.style.setProperty('--go',0)});
  });
  // hero parallax
  var hero=document.querySelector('.hero');
  if(fine&&hero){
    hero.addEventListener('pointermove',function(ev){var r=hero.getBoundingClientRect();
      hero.style.setProperty('--mx',(((ev.clientX-r.left)/r.width-.5)*2).toFixed(3));
      hero.style.setProperty('--my',(((ev.clientY-r.top)/r.height-.5)*2).toFixed(3));});
    hero.addEventListener('pointerleave',function(){hero.style.setProperty('--mx',0);hero.style.setProperty('--my',0)});
  }
  // scroll parallax on photo bands
  var bands=[].slice.call(document.querySelectorAll('.quote,.connect,.ab-name')), tick=false;
  function par(){tick=false;var h=innerHeight;bands.forEach(function(b){var r=b.getBoundingClientRect();if(r.bottom<0||r.top>h)return;
    var p=((r.top+r.height/2)-h/2)/h;b.querySelector('img.m').style.setProperty('--py',(p*-40).toFixed(1)+'px');});}
  addEventListener('scroll',function(){if(!tick){tick=true;requestAnimationFrame(par)}},{passive:true});par();
})();
(function(){
  var root=document.documentElement, loader=document.getElementById('loader');
  var calm=matchMedia('(prefers-reduced-motion: reduce)').matches, lenis=null, started=false;
  function begin(){
    if(started) return; started=true;
    root.classList.add('ready'); root.classList.remove('loading');
    if(loader){loader.classList.add('done'); setTimeout(function(){loader.style.display='none'},1100);}
    if(lenis) lenis.start();
  }
  // smooth scrolling (Lenis from CDN; falls back to CSS smooth scroll)
  if(!calm){
    var sc=document.createElement('script');
    sc.src='https://cdn.jsdelivr.net/npm/lenis@1.1.20/dist/lenis.min.js';
    sc.onload=function(){
      if(!window.Lenis) return;
      lenis=new Lenis({duration:1.2,easing:function(t){return Math.min(1,1.001-Math.pow(2,-10*t))},smoothWheel:true,
        prevent:function(n){return n.id==='mo'||n.id==='lb'}});
      window.__lenis=lenis;
      if(!started||document.documentElement.classList.contains('menu-open')) lenis.stop();
      (function raf(t){lenis.raf(t);requestAnimationFrame(raf)})(performance.now());
      [].forEach.call(document.querySelectorAll('a[href^="#"]'),function(a){
        a.addEventListener('click',function(e){
          var id=a.getAttribute('href'), el=id.length>1&&document.querySelector(id);
          if(!el) return; e.preventDefault(); lenis.scrollTo(el,{offset:0,duration:1.6});
        });
      });
    };
    document.head.appendChild(sc);
  }
  if(calm||!loader){begin();return;}
  var minWait=new Promise(function(r){setTimeout(r,1900)});
  var loaded=new Promise(function(r){ if(document.readyState==='complete') r(); else addEventListener('load',r); });
  Promise.all([minWait,loaded]).then(begin);
  setTimeout(begin,4500); // failsafe
})();
(function(){
  // count-up animation for stat numbers (e.g. "5+", "50+", "100%")
  var els=[].slice.call(document.querySelectorAll('.stat b, .page-about .fact b'));
  if(!els.length||matchMedia('(prefers-reduced-motion: reduce)').matches||!('IntersectionObserver' in window)) return;
  var root=document.documentElement;
  els.forEach(function(el){
    var m=el.textContent.trim().match(/^(\D*)(\d+)(.*)$/); if(!m) return;
    el.dataset.pre=m[1]; el.dataset.to=m[2]; el.dataset.suf=m[3];
    el.style.fontVariantNumeric='tabular-nums lining-nums';
    el.textContent=m[1]+(+m[2]>1000?+m[2]-25:0)+m[3];
  });
  function run(el){
    var to=+el.dataset.to, from=to>1000?to-25:0, pre=el.dataset.pre, suf=el.dataset.suf, dur=1600+Math.min(to,100)*6, t0=null;
    (function step(t){
      if(!root.classList.contains('ready')&&document.getElementById('loader')){requestAnimationFrame(step);return;}
      if(t0===null) t0=t;
      var p=Math.min(1,(t-t0)/dur), e=1-Math.pow(1-p,4);
      el.textContent=pre+Math.round(from+(to-from)*e)+suf;
      if(p<1) requestAnimationFrame(step);
    })(performance.now());
  }
  var io=new IntersectionObserver(function(es){es.forEach(function(e){
    if(e.isIntersecting&&e.target.dataset.to){io.unobserve(e.target);setTimeout(function(){run(e.target)},350);}
  })},{threshold:.6});
  els.forEach(function(el){if(el.dataset.to) io.observe(el)});
})();
(function(){
  // manifesto: words light up as the paragraph scrolls through the viewport
  var mf=document.querySelector('[data-words]'); if(!mf) return;
  (function wrap(node){ [].slice.call(node.childNodes).forEach(function(n){
    if(n.nodeType===3){ var f=document.createDocumentFragment();
      n.textContent.split(/(\s+)/).forEach(function(w){ if(!w) return; if(/^\s+$/.test(w)){f.appendChild(document.createTextNode(w));return;}
        var s=document.createElement('span'); s.className='w'; s.textContent=w; f.appendChild(s); });
      n.parentNode.replaceChild(f,n); }
    else if(n.nodeType===1) wrap(n); }); })(mf);
  var ws=[].slice.call(mf.querySelectorAll('.w'));
  if(matchMedia('(prefers-reduced-motion: reduce)').matches){ ws.forEach(function(w){w.classList.add('on')}); return; }
  var tick=false;
  function upd(){ tick=false; var r=mf.getBoundingClientRect(), h=innerHeight;
    var p=Math.min(1,Math.max(0,(h*.85-r.top)/(r.height+h*.35))), n=Math.round(p*ws.length);
    ws.forEach(function(w,i){ w.classList.toggle('on', i<n); }); }
  addEventListener('scroll',function(){ if(!tick){tick=true;requestAnimationFrame(upd)} },{passive:true}); upd();
})();
(function(){
  // cursor spotlight on the "What drives me" cards
  if(!matchMedia('(hover:hover) and (pointer:fine)').matches) return;
  [].forEach.call(document.querySelectorAll('.drives .tech'),function(c){
    c.addEventListener('pointermove',function(e){var r=c.getBoundingClientRect();
      c.style.setProperty('--x',(e.clientX-r.left)+'px');c.style.setProperty('--y',(e.clientY-r.top)+'px');});
  });
})();
(function(){
  // journey card slider: crossfade photos, 01 / 04 counter, arrows + autoplay (pauses on hover)
  var jr=document.querySelector('.jr'); if(!jr) return;
  var imgs=[].slice.call(jr.querySelectorAll('.jr-img')), cur=0, n=imgs.length, b=jr.querySelector('.jr-count b'), tot=jr.querySelector('.jr-count span'), timer=null;
  if(tot) tot.textContent=(n<10?'0':'')+n;
  function go(i){ imgs[cur].classList.remove('on'); cur=(i+n)%n; imgs[cur].classList.add('on'); b.textContent=(cur<9?'0':'')+(cur+1); }
  function play(){ stop(); if(!matchMedia('(prefers-reduced-motion: reduce)').matches) timer=setInterval(function(){go(cur+1)},6000); }
  function stop(){ if(timer) clearInterval(timer); timer=null; }
  jr.querySelector('.jr-prev').addEventListener('click',function(){go(cur-1);play()});
  jr.querySelector('.jr-next').addEventListener('click',function(){go(cur+1);play()});
  jr.addEventListener('pointerenter',stop); jr.addEventListener('pointerleave',play);
  imgs.forEach(function(im){ if(im.loading==='lazy') im.loading='eager'; });
  play();
})();
(function(){
  // journey chapters: gentle photo parallax
  var ims=[].slice.call(document.querySelectorAll('.page-journey .ch-frame img')); if(!ims.length||matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var tick=false; function upd(){ tick=false; var h=innerHeight; ims.forEach(function(im){ var r=im.parentNode.getBoundingClientRect(); if(r.bottom<0||r.top>h) return;
    im.style.setProperty('--py', (((r.top+r.height/2)-h/2)/h*-30).toFixed(1)+'px'); }); }
  addEventListener('scroll',function(){ if(!tick){tick=true;requestAnimationFrame(upd)} },{passive:true}); upd();
})();
(function(){
  // about milestones rail: arrows, drag to scroll, progress bar
  var rail=document.querySelector('.ab-rail'); if(!rail) return;
  var bar=document.querySelector('.ab-rail-bar i'), sec=rail.closest('section');
  function step(){ var c=rail.querySelector('.ms'); return c ? c.getBoundingClientRect().width+20 : 300; }
  function upd(){ var max=rail.scrollWidth-rail.clientWidth, p=max>0?rail.scrollLeft/max:1, w=Math.max(.12, rail.clientWidth/rail.scrollWidth);
    if(bar){ bar.style.width=(w*100)+'%'; bar.style.transform='translateX('+(p*(1/w-1)*100)+'%)'; } }
  sec.querySelector('.rp').addEventListener('click',function(){ rail.scrollBy({left:-step(),behavior:'smooth'}); });
  sec.querySelector('.rn').addEventListener('click',function(){ rail.scrollBy({left:step(),behavior:'smooth'}); });
  rail.addEventListener('scroll',upd,{passive:true}); addEventListener('resize',upd); upd();
  rail.addEventListener('keydown',function(e){ if(e.key==='ArrowRight'){rail.scrollBy({left:step(),behavior:'smooth'});e.preventDefault();} if(e.key==='ArrowLeft'){rail.scrollBy({left:-step(),behavior:'smooth'});e.preventDefault();} });
  var down=false,sx=0,sl=0,moved=false;
  rail.addEventListener('pointerdown',function(e){ if(e.pointerType!=='mouse') return; down=true; moved=false; sx=e.clientX; sl=rail.scrollLeft; });
  addEventListener('pointermove',function(e){ if(!down) return; var dx=e.clientX-sx; if(Math.abs(dx)>4){ moved=true; rail.classList.add('drag'); } rail.scrollLeft=sl-dx; });
  addEventListener('pointerup',function(){ if(!down) return; down=false; rail.classList.toggle('drag',false);
    if(moved){ var s=step(); rail.scrollTo({left:Math.round(rail.scrollLeft/s)*s,behavior:'smooth'}); } });
  rail.addEventListener('click',function(e){ if(moved){ e.preventDefault(); moved=false; } },true);
})();
