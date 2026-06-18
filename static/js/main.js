document.addEventListener('DOMContentLoaded', () => {
  (function() {
    if (sessionStorage.getItem('preloaderSeen')) {
      document.getElementById('preloader').style.display = 'none';
      return;
    }
    const TAU=Math.PI*2, cx=200, cy=170, r=98, SEG=154;
    function pt(a){ return {x:cx+r*Math.cos(a-Math.PI/2), y:cy+r*Math.sin(a-Math.PI/2)}; }
    function ease(t){ return t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2; }
    const arcs=[0,1,2,3].map(i=>document.getElementById('plArc'+i));
    const brush=document.getElementById('plBrush');
    const logo=document.getElementById('plLogo');
    const pre=document.getElementById('preloader');
    const dur=2200; let start=null;
    function tick(ts){
      if(!start) start=ts;
      const raw=Math.min((ts-start)/dur,1), prog=ease(raw);
      const angle=prog*TAU, p=pt(angle);
      const holdAngle=(angle*180/Math.PI)+90-38;
      brush.style.opacity='1';
      brush.setAttribute('transform',`translate(${p.x},${p.y}) rotate(${holdAngle})`);
      const seg=Math.min(Math.floor(prog*4),3), segProg=(prog*4)%1;
      for(let i=0;i<4;i++){
        if(i<seg) arcs[i].style.strokeDashoffset='0';
        else if(i===seg) arcs[i].style.strokeDashoffset=SEG*(1-segProg);
        else arcs[i].style.strokeDashoffset=SEG;
      }
      if(raw<1){ requestAnimationFrame(tick); }
      else {
        arcs.forEach(a=>a.style.strokeDashoffset='0');
        brush.style.transition='opacity 0.5s ease';
        brush.style.opacity='0';
        setTimeout(()=>logo.style.opacity='1', 400);
        setTimeout(()=>{
          pre.style.transition='opacity 0.7s ease';
          pre.style.opacity='0';
          setTimeout(()=>{ pre.style.display='none'; sessionStorage.setItem('preloaderSeen','1'); }, 700);
        }, 2000);
      }
    }
    setTimeout(()=>requestAnimationFrame(tick), 300);
  })();

  const navbar = document.getElementById('navbar');
  if (navbar) {
    const onScroll = () => {
      if (window.scrollY > 20) {
        navbar.classList.add('navbar-scrolled');
      } else {
        navbar.classList.remove('navbar-scrolled');
      }
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', (e) => {
      const targetId = anchor.getAttribute('href');
      if (!targetId || targetId === '#') return;
      const target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // Scroll reveal — triggers .reveal elements as they enter the viewport
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });

  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
});
