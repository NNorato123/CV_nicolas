// ===================================
// ANIMACIONES AL SCROLL
// ===================================

// Intersection Observer para animar elementos cuando entran en viewport
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in-up');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Elementos a animar
document.addEventListener('DOMContentLoaded', () => {
    // Animar tarjetas de proyectos
    document.querySelectorAll('.project-card').forEach(card => {
        card.classList.add('animate-on-scroll');
        observer.observe(card);
    });

    // Animar tarjetas de habilidades
    document.querySelectorAll('.skill-category').forEach(skill => {
        skill.classList.add('animate-on-scroll');
        observer.observe(skill);
    });

    // Animar items de experiencia
    document.querySelectorAll('.timeline-item').forEach(item => {
        item.classList.add('animate-on-scroll');
        observer.observe(item);
    });

    // Animar tarjetas de educación
    document.querySelectorAll('.education-card').forEach(card => {
        card.classList.add('animate-on-scroll');
        observer.observe(card);
    });

    // Animar items de contacto
    document.querySelectorAll('.contact-item').forEach(item => {
        item.classList.add('animate-on-scroll');
        observer.observe(item);
    });

    // Animar iconos de tecnologías
    document.querySelectorAll('.tech-icon').forEach(icon => {
        icon.classList.add('animate-on-scroll');
        observer.observe(icon);
    });

    // Animar encabezados
    document.querySelectorAll('h2').forEach(h2 => {
        h2.classList.add('animate-on-scroll');
        observer.observe(h2);
    });

    // Smooth scroll para anclas
    smoothScrollLinks();
});

// Smooth scroll para enlaces con #
function smoothScrollLinks() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
}

// Animación de parallax sutil
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const parallaxElements = document.querySelectorAll('[data-parallax]');
    
    parallaxElements.forEach(el => {
        const parallaxValue = scrolled * 0.5;
        el.style.transform = `translateY(${parallaxValue}px)`;
    });
});

// Animación del navbar al scroll
let lastScrollTop = 0;
const navbar = document.querySelector('nav');

if (navbar) {
    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > 100) {
            navbar.style.background = 'rgba(15, 23, 42, 0.95)';
            navbar.style.backdropFilter = 'blur(10px)';
            navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.3)';
        } else {
            navbar.style.background = 'rgba(15, 23, 42, 0.9)';
            navbar.style.boxShadow = 'none';
        }
        
        lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
    });
}

// Botón "Volver arriba"
function createScrollToTop() {
    const button = document.createElement('button');
    button.id = 'scrollToTop';
    button.innerHTML = '⬆️';
    button.style.cssText = `
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        width: 50px;
        height: 50px;
        background: linear-gradient(90deg, #3b82f6, #60a5fa);
        color: white;
        border: none;
        border-radius: 50%;
        cursor: pointer;
        font-size: 1.5rem;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
        z-index: 999;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    `;
    
    document.body.appendChild(button);
    
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            button.style.opacity = '1';
            button.style.visibility = 'visible';
        } else {
            button.style.opacity = '0';
            button.style.visibility = 'hidden';
        }
    });
    
    button.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Crear botón scroll to top
document.addEventListener('DOMContentLoaded', createScrollToTop);
