document.addEventListener('DOMContentLoaded', () => {
    // 1. 스크롤 애니메이션 (Fade-in 효과)
    const observerOptions = {
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    document.querySelectorAll('.fade-in, .feature-card, .step').forEach(el => {
        el.classList.add('fade-in'); // 초기 클래스 할당
        observer.observe(el);
    });

    // 2. 헤더 스크롤 효과
    const header = document.getElementById('main-header');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.style.padding = '0.5rem 0';
            header.style.background = 'rgba(10, 10, 15, 0.95)';
        } else {
            header.style.padding = '1rem 0';
            header.style.background = 'rgba(10, 10, 15, 0.8)';
        }
    });

    // 3. 스무스 스크롤 (네비게이션 링크)
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});
