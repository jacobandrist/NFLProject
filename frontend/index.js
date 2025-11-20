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


const BASE_URL = "http://167.172.117.166:8000";

// --- SIMPLE TEST FETCH ---
async function testConnection() {
    try {
        const res = await fetch(`${BASE_URL}/leaders?limit=1`);
        const data = await res.json();
        console.log("Backend Connected!", data);
        
        // Display on page:
        const h2 = document.createElement("h2");
        h2.style.color = "lime";
        h2.textContent = "Backend Connected ✔";
        document.body.prepend(h2);
    } catch (err) {
        console.log("Backend FAILED ❌", err);
    }
}

testConnection();
