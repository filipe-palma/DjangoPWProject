// Portfolio - JavaScript Interativo

// Alternar entre tema claro e escuro
document.addEventListener('DOMContentLoaded', function() {
    // Verificar se há preferência salva
    const currentTheme = localStorage.getItem('theme') ? localStorage.getItem('theme') : null;
    
    // Se houver, aplicar tema
    if (currentTheme) {
        document.documentElement.setAttribute('data-theme', currentTheme);
        
        if (currentTheme === 'dark') {
            document.getElementById('theme-toggle-icon').classList.remove('fa-moon');
            document.getElementById('theme-toggle-icon').classList.add('fa-sun');
        }
    }
    
    // Configurar botão de alternar tema
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            let theme = 'light';
            const icon = document.getElementById('theme-toggle-icon');
            
            if (document.documentElement.getAttribute('data-theme') !== 'dark') {
                document.documentElement.setAttribute('data-theme', 'dark');
                theme = 'dark';
                icon.classList.remove('fa-moon');
                icon.classList.add('fa-sun');
            } else {
                document.documentElement.setAttribute('data-theme', 'light');
                icon.classList.remove('fa-sun');
                icon.classList.add('fa-moon');
            }
            
            localStorage.setItem('theme', theme);
        });
    }
    
    // Adicionar classe active ao link de navegação atual
    const currentLocation = location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentLocation) {
            link.classList.add('active');
        }
    });
    
    // Animações ao scroll
    const animateElements = document.querySelectorAll('.animate-on-scroll');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
            }
        });
    }, { threshold: 0.1 });
    
    animateElements.forEach(element => {
        observer.observe(element);
    });
});

// Efeito de digitação para títulos (usado na página inicial)
function typeEffect(element, text, speed = 100) {
    let i = 0;
    
    function typing() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(typing, speed);
        }
    }
    
    typing();
}

// Iniciar efeito de digitação quando o elemento estiver visível
document.addEventListener('DOMContentLoaded', function() {
    const typingElement = document.getElementById('typing-effect');
    
    if (typingElement) {
        const text = typingElement.getAttribute('data-text');
        typingElement.innerHTML = '';
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    typeEffect(typingElement, text);
                    observer.unobserve(typingElement);
                }
            });
        });
        
        observer.observe(typingElement);
    }
});
