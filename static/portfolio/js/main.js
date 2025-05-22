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

// Gerenciamento de responsividade para navegação em dispositivos móveis
document.addEventListener('DOMContentLoaded', function() {
    // Fechar o menu mobile quando um item for clicado
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        document.querySelectorAll('.navbar-nav .nav-link').forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth < 992 && navbarCollapse.classList.contains('show')) {
                    navbarToggler.click();
                }
            });
        });
    }
    
    // Manipular o comportamento de touch em dispositivos móveis para cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        // Detector de dispositivos touch
        if ('ontouchstart' in window || navigator.maxTouchPoints) {
            card.addEventListener('touchstart', function() {
                this.classList.add('card-touch');
            }, {passive: true});
            
            card.addEventListener('touchend', function() {
                this.classList.remove('card-touch');
            }, {passive: true});
        }
    });
    
    // Ajustar altura de elementos conforme necessário em telas pequenas
    function adjustHeights() {
        // Redefinir alturas antes de ajustar
        const itemsToReset = document.querySelectorAll('.card-body');
        itemsToReset.forEach(item => item.style.height = 'auto');
        
        // Em telas maiores, igualar altura dos cards na mesma linha
        if (window.innerWidth >= 768) {
            const rows = {};
            document.querySelectorAll('.card').forEach(card => {
                const top = card.getBoundingClientRect().top;
                if (!rows[top]) rows[top] = [];
                rows[top].push(card.querySelector('.card-body'));
            });
            
            // Aplicar a mesma altura a todos os cards na mesma "linha"
            Object.values(rows).forEach(row => {
                const maxHeight = Math.max(...row.map(el => el.offsetHeight));
                row.forEach(el => el.style.height = maxHeight + 'px');
            });
        }
    }
    
    // Executar ajuste de altura ao carregar e ao redimensionar
    window.addEventListener('load', adjustHeights);
    window.addEventListener('resize', adjustHeights);
});

// Função para verificar e ajustar conforme necessário a responsividade
function checkResponsiveness() {
  // Ajustar tamanho dos itens em telas pequenas
  const isMobile = window.innerWidth < 768;
  
  // Ajustar botões em dispositivos móveis
  document.querySelectorAll('.btn').forEach(btn => {
    if (isMobile && !btn.classList.contains('btn-sm') && !btn.classList.contains('btn-lg')) {
      btn.classList.add('w-100', 'mb-2');
    } else if (!isMobile) {
      btn.classList.remove('w-100', 'mb-2');
    }
  });
  
  // Garantir que imagens sejam responsivas
  document.querySelectorAll('img:not(.tech-logo):not(.card-img-top)').forEach(img => {
    if (!img.classList.contains('img-fluid')) {
      img.classList.add('img-fluid');
    }
  });
  
  // Ajustar vídeos incorporados para serem responsivos
  document.querySelectorAll('iframe').forEach(iframe => {
    const parent = iframe.parentElement;
    if (!parent.classList.contains('video-container') && !parent.classList.contains('responsive-embed')) {
      const wrapper = document.createElement('div');
      wrapper.className = 'responsive-embed';
      parent.insertBefore(wrapper, iframe);
      wrapper.appendChild(iframe);
    }
  });
}

// Executar verificação de responsividade ao carregar e redimensionar
window.addEventListener('load', checkResponsiveness);
window.addEventListener('resize', checkResponsiveness);

// Para cards de projetos, garantir que as ações fiquem bem organizadas em telas pequenas
document.querySelectorAll('.projeto-actions').forEach(actionsContainer => {
  if (window.innerWidth < 768) {
    actionsContainer.querySelectorAll('.btn-action').forEach(btn => {
      btn.classList.add('w-100', 'justify-content-center');
    });
  }
});

// Ajuste para menu responsivo
const navbarCollapse = document.querySelector('.navbar-collapse');
if (navbarCollapse) {
  document.querySelectorAll('.navbar-nav .nav-link').forEach(link => {
    link.addEventListener('click', () => {
      if (window.innerWidth < 992 && navbarCollapse.classList.contains('show')) {
        document.querySelector('.navbar-toggler').click();
      }
    });
  });
}
