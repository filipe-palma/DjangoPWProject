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

// Fechar menu móvel quando um item é clicado
document.addEventListener('DOMContentLoaded', function() {
    // Verificar se estamos em um dispositivo móvel (largura < 992px)
    const isMobile = () => window.innerWidth < 992;
    
    // Pegar todos os links do navbar
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    const navbarCollapse = document.getElementById('navbarNav');
    const bsCollapse = navbarCollapse ? new bootstrap.Collapse(navbarCollapse, {toggle: false}) : null;
    
    // Adicionar evento de clique para cada link
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            // Se estamos em dispositivo móvel e o menu está aberto, fechá-lo
            if (isMobile() && navbarCollapse && navbarCollapse.classList.contains('show')) {
                bsCollapse.hide();
            }
        });
    });
    
    // Evitar que o dropdown do usuário feche o menu inteiro em dispositivos móveis
    const dropdownMenus = document.querySelectorAll('.dropdown-menu');
    dropdownMenus.forEach(menu => {
        menu.addEventListener('click', (e) => {
            // Evitar propagação apenas em dispositivos móveis
            if (isMobile()) {
                e.stopPropagation();
            }
        });
    });
});

// Detectar e corrigir problemas de overflow horizontal
document.addEventListener('DOMContentLoaded', function() {
  const checkForOverflow = () => {
    const docWidth = document.documentElement.clientWidth;
    let hasHorizontalOverflow = false;
    
    // Verificar se há elementos que extrapolam a largura da viewport
    document.querySelectorAll('*').forEach(element => {
      const rect = element.getBoundingClientRect();
      if (rect.right > docWidth || rect.left < 0) {
        if (!(element instanceof SVGElement)) { // Ignorar elementos SVG
          hasHorizontalOverflow = true;
          
          // Se for um elemento do navbar, ajustar automaticamente
          if (element.closest('.navbar') || element.closest('.dropdown-menu')) {
            element.style.maxWidth = '100%';
            element.style.overflowX = 'hidden';
          }
        }
      }
    });
    
    // Se detectar overflow, aplicar correções específicas
    if (hasHorizontalOverflow) {
      document.body.style.overflowX = 'hidden';
      document.documentElement.style.overflowX = 'hidden';
      
      // Ajustar elementos do navbar que podem estar causando problemas
      const navbarElements = document.querySelectorAll('.navbar-nav, .dropdown-menu');
      navbarElements.forEach(el => {
        el.style.maxWidth = '100vw';
        el.style.width = 'auto';
      });
    }
  };
  
  // Executar ao carregar e ao redimensionar
  checkForOverflow();
  window.addEventListener('resize', checkForOverflow);
});
