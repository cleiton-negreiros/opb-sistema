// ============================================
// NAVIGATION
// ============================================
const PAGES = { dashboard:'Dashboard', cerebro:'Cérebro', rotinas:'Rotinas', transcricao:'Transcrição', 'capa-video':'Capa Vídeo', carrossel:'Carrossel', pipeline:'Pipeline Diário', consumo:'Consumo', posicionamento:'Posicionamento', 'text-generator':'Text Generator',   narvi:'Narvi', radagast:'Radagast', 'consultor-negocios':'Consultor de Negócios', 'jornada-ia':'Jornada IA', perfil:'Meu Perfil', produtividade:'Produtividade',
  'quadro-avisos':'Quadro de Avisos', inspiracoes:'Inspirações', aprendizados:'Aprendizados', config:'Configurações', gimli:'Gimli', arquivos:'Arquivos', 'audio-transcriber':'Áudio' };

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
    const pageTitle = document.getElementById('pageTitle');
    const pageBreadcrumb = document.getElementById('pageBreadcrumb');
    if (info && pageTitle) pageTitle.textContent = info;
    if (info && pageBreadcrumb) pageBreadcrumb.textContent = 'OPB Studio / ' + info;
    closeMobileMenu();
    location.hash = page;
    loadPageData(page);
}

// Handle browser Back/Forward buttons
window.addEventListener('hashchange', function() {
    const page = location.hash.replace('#', '');
    if (page && PAGES[page]) {
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        const target = document.getElementById('page-' + page);
        if (target) target.classList.add('active');
        document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
        document.querySelectorAll('.nav-item').forEach(item => {
            if (item.getAttribute('onclick') === `navigateTo('${page}')`) item.classList.add('active');
        });
        document.querySelectorAll('.bottom-nav-item').forEach(item => item.classList.remove('active'));
        document.querySelectorAll('.bottom-nav-item').forEach(item => {
            if (item.getAttribute('onclick') === `navigateTo('${page}')`) item.classList.add('active');
        });
        const info = PAGES[page];
        const pageTitle = document.getElementById('pageTitle');
        const pageBreadcrumb = document.getElementById('pageBreadcrumb');
        if (info && pageTitle) pageTitle.textContent = info;
        if (info && pageBreadcrumb) pageBreadcrumb.textContent = 'OPB Studio / ' + info;
        loadPageData(page);
    }
});

function toggleSidebarCollapse() {
    const s = document.getElementById('sidebar');
    s.classList.toggle('collapsed');
    localStorage.setItem('sidebarCollapsed', s.classList.contains('collapsed'));
}
