// Toggle menu mobile
function toggleMenu() {
    document.getElementById('menuList').classList.toggle('active');
}

// Fechar menu ao clicar em link
document.querySelectorAll('.menu-list a').forEach(link => {
    link.addEventListener('click', () => {
        document.getElementById('menuList').classList.remove('active');
    });
});

// Formatar moeda
function formatarMoeda(valor) {
    return 'R$ ' + parseFloat(valor).toFixed(2).replace('.', ',');
}

// Formatar data BR
function formatarDataBR(dataISO) {
    const partes = dataISO.split('-');
    return partes[2] + '/' + partes[1] + '/' + partes[0];
}

// Auto-hide alerts
setTimeout(() => {
    document.querySelectorAll('.alert').forEach(alert => {
        alert.style.opacity = '0';
        alert.style.transition = 'opacity 0.5s';
        setTimeout(() => alert.remove(), 500);
    });
}, 3000);

// Scroll top button
const scrollTopBtn = document.querySelector('.scroll-top');
if (scrollTopBtn) {
    window.addEventListener('scroll', () => {
        if (window.scrollY > 300) {
            scrollTopBtn.classList.add('visible');
        } else {
            scrollTopBtn.classList.remove('visible');
        }
    });
}