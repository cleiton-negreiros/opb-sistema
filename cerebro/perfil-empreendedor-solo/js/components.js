// ============================================
// COMPONENTS
// ============================================
function showPerfilTab(tab, el) {
    document.querySelectorAll('.tab-inline').forEach(t => t.classList.remove('active'));
    el.classList.add('active');
    const basico = document.getElementById('perfil-tab-basico');
    const modulos = document.getElementById('perfil-modulos');
    if (tab === 'basico') {
        basico.style.display = 'block';
        modulos.style.display = 'none';
    } else {
        basico.style.display = 'none';
        modulos.style.display = 'block';
        document.querySelectorAll('#perfil-modulos .card').forEach(c => c.style.display = 'none');
        const map = { habilidades:0, historias:1, cosmovisao:2, publico:3, posicionamento:4, narrativa:5 };
        const cards = document.querySelectorAll('#perfil-modulos .card');
        const idx = map[tab];
        if (idx !== undefined && cards[idx]) cards[idx].style.display = 'block';
    }
}

function toggleMobileMenu() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    if (sidebar && overlay) {
        sidebar.classList.toggle('mobile-open');
        overlay.classList.toggle('active');
    }
}

function closeMobileMenu() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    if (sidebar && overlay) {
        sidebar.classList.remove('mobile-open');
        overlay.classList.remove('active');
    }
}
