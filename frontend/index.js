const counters = document.querySelectorAll('.stat-number');
    const speed = 100;

    const animateCounters = () => {
      counters.forEach(counter => {
        const update = () => {
          const target = +counter.getAttribute('data-target');
          const count = +counter.innerText;
          const increment = target / speed;

          if (count < target) {
            counter.innerText = Math.ceil(count + increment);
            requestAnimationFrame(update);
          } else {
            counter.innerText = target;
          }
        };
        update();
      });
    };

    const observer = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting) animateCounters();
    }, { threshold: 0.3 });

    observer.observe(document.querySelector('#leaders'));