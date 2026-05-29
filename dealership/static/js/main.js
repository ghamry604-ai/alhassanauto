document.addEventListener('DOMContentLoaded', () => {

  // ===== NAVBAR: add shadow on scroll (Minimalist & Dynamic) =====
  const navbar = document.querySelector('.ae-navbar');
  if (navbar) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 50) {
        // يسحب الظل الديناميكي الناعم المخصص للـ Light أو Dark تلقائياً
        navbar.style.boxShadow = 'var(--shadow-lg)';
      } else {
        navbar.style.boxShadow = 'none';
      }
    });
  }

  // ===== CARD ENTRANCE ANIMATIONS =====
  const cards = document.querySelectorAll('.ae-car-card');
  if ('IntersectionObserver' in window && cards.length) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry, i) => {
        if (entry.isIntersecting) {
          setTimeout(() => {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
          }, i * 60);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });

    cards.forEach(card => {
      card.style.opacity = '0';
      card.style.transform = 'translateY(20px)';
      card.style.transition = 'opacity 0.4s ease, transform 0.4s ease, border-color 0.2s ease, box-shadow 0.2s ease';
      observer.observe(card);
    });
  }

  // ===== HERO STATS COUNTER ANIMATION =====
  const statNumbers = document.querySelectorAll('.stat-number');
  if (statNumbers.length) {
    statNumbers.forEach(el => {
      const rawText = el.textContent.trim();
      const num = parseInt(rawText.replace(/\D/g, ''), 10);
      const suffix = rawText.replace(/[\d]/g, '');
      if (!isNaN(num)) {
        let current = 0;
        const step = Math.ceil(num / 40);
        const timer = setInterval(() => {
          current = Math.min(current + step, num);
          el.textContent = current.toLocaleString() + suffix;
          if (current >= num) clearInterval(timer);
        }, 30);
      }
    });
  }

  // ===== SMOOTH FILTER FORM AUTO-SUBMIT FEEDBACK =====
  const filterForm = document.getElementById('filterForm');
  if (filterForm) {
    filterForm.addEventListener('change', (e) => {
      if (e.target.tagName === 'SELECT') {
        filterForm.submit();
      }
    });
  }

  // ===== BACK TO TOP BUTTON (Minimalist & Adaptive Style) =====
  const bttBtn = document.createElement('button');
  bttBtn.innerHTML = '<i class="bi bi-arrow-up"></i>';
  bttBtn.className = 'btt-btn';
  bttBtn.setAttribute('aria-label', 'Back to top');
  
  // تعديل الألوان لتصبح متغيرة (تتحول تلقائياً في الـ Light والـ Dark)
  bttBtn.style.cssText = `
    position: fixed; bottom: 2rem; right: 2rem;
    width: 40px; height: 40px;
    background: var(--text-primary); color: var(--bg-main);
    border: 1px solid var(--border); border-radius: 50%;
    font-size: 1rem; cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    box-shadow: var(--shadow);
    opacity: 0; transform: translateY(10px);
    transition: opacity 0.3s, transform 0.3s, background 0.2s;
    z-index: 9999;
  `;
  document.body.appendChild(bttBtn);

  window.addEventListener('scroll', () => {
    if (window.scrollY > 400) {
      bttBtn.style.opacity = '1';
      bttBtn.style.transform = 'translateY(0)';
    } else {
      bttBtn.style.opacity = '0';
      bttBtn.style.transform = 'translateY(10px)';
    }
  });

  bttBtn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

});