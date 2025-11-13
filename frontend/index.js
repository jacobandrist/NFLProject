
  (function(){
    const hero = document.querySelector('.hero');
    const heroInner = document.querySelector('.hero-inner');
    const masonryItems = Array.from(document.querySelectorAll('.masonry-item'));
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = lightbox.querySelector('img');
    const closeBtn = lightbox.querySelector('.close-btn');

    let lastScroll = 0;
    window.addEventListener('scroll', () => {
      const y = window.scrollY || window.pageYOffset;
      const threshold = hero.offsetHeight * 0.2;
      if (y > threshold) hero.classList.add('shrunk'); else hero.classList.remove('shrunk');

      const depth = Math.min(50, Math.max(0, y / 12)); // clamp
      hero.style.transform = `translateY(${ -depth * 0.12 }px)`;

      lastScroll = y;
    }, {passive:true});

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting){
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, {rootMargin: '0px 0px -80px 0px', threshold: 0.08});

    masonryItems.forEach((el,i)=>{
      el.style.transitionDelay = `${(i % 6) * 0.06}s`;
      observer.observe(el);
    });

    document.getElementById('masonry').addEventListener('click', (ev) => {
      const target = ev.target;
      if (target && target.tagName === 'IMG'){
        openLightbox(target);
      }
    });

    function openLightbox(imgEl){
      lightboxImg.src = imgEl.src.replace(/\/\d+\/\d+$/, function(match){
        return match;
      });
      lightboxImg.alt = imgEl.alt || '';
      lightbox.classList.add('open');
      lightbox.setAttribute('aria-hidden','false');
      document.body.style.overflow = 'hidden';
    }
    function closeLightbox(){
      lightbox.classList.remove('open');
      lightbox.setAttribute('aria-hidden','true');
      document.body.style.overflow = '';
      setTimeout(()=> lightboxImg.src = '', 300);
    }

    closeBtn.addEventListener('click', closeLightbox);
    lightbox.addEventListener('click', (e) => {
      if (e.target === lightbox) closeLightbox();
    });

    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && lightbox.classList.contains('open')) closeLightbox();
    });

    document.querySelectorAll('nav.navbar a[href^="#"]').forEach(a=>{
      a.addEventListener('click', (ev)=>{
        ev.preventDefault();
        const id = a.getAttribute('href').slice(1);
        const el = document.getElementById(id);
        if (!el) return;
        const rect = el.getBoundingClientRect();
        const offset = window.pageYOffset + rect.top - (parseInt(getComputedStyle(document.documentElement).getPropertyValue('--nav-height')) || 68) - 12;
        window.scrollTo({top: offset, behavior:'smooth'});
      });
    });

    if ((window.scrollY || window.pageYOffset) > (hero.offsetHeight * 0.2)) {
      hero.classList.add('shrunk');
    }
  })();