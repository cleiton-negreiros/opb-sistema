// ============================================
// NAVIGATION
// ============================================
const PAGES = { dashboard:'Dashboard', cerebro:'Cérebro', rotinas:'Rotinas', transcricao:'Transcrição', 'capa-video':'Capa Vídeo', carrossel:'Carrossel', consumo:'Consumo', posicionamento:'Posicionamento', 'text-generator':'Text Generator',   narvi:'Narvi', radagast:'Radagast', perfil:'Meu Perfil', produtividade:'Produtividade',
  'quadro-avisos':'Quadro de Avisos', inspiracoes:'Inspirações', config:'Configurações' };

function navigateTo(page) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    const target = document.getElementById('page-' + page);
    if (target) {
        target.classList.add('active');
        target.scrollIntoView({behavior:'smooth',block:'start'});
    }
    document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
    document.querySelectorAll('.nav-item').forEach(item => {
        if (item.getAttribute('onclick') === `navigateTo('${page}')`) item.classList.add('active');
    });
    // Sync bottom nav
    document.querySelectorAll('.bottom-nav-item').forEach(item => item.classList.remove('active'));
    document.querySelectorAll('.bottom-nav-item').forEach(item => {
        if (item.getAttribute('onclick') === `navigateTo('${page}')`) item.classList.add('active');
    });
    const info = PAGES[page];
    if (info) { document.getElementById('pageTitle').textContent = info; document.getElementById('pageBreadcrumb').textContent = 'OPB Studio / ' + info; }
    closeMobileMenu();
    location.hash = page;
    loadPageData(page);
}

function toggleSidebarCollapse() {
    const s = document.getElementById('sidebar');
    s.classList.toggle('collapsed');
    localStorage.setItem('sidebarCollapsed', s.classList.contains('collapsed'));
}
