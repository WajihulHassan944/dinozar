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
  var bands=[].slice.call(document.querySelectorAll('.quote,.connect')), tick=false;
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
      lenis=new Lenis({duration:1.2,easing:function(t){return Math.min(1,1.001-Math.pow(2,-10*t))},smoothWheel:true});
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
