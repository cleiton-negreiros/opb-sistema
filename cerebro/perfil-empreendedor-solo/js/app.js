// ============================================
// THEME TOGGLE
// ============================================
function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('opb-theme', next);
    updateThemeIcon(next);
}

function updateThemeIcon(theme) {
    const btn = document.getElementById('themeToggle');
    if (!btn) return;
    const icon = btn.querySelector('i');
    if (theme === 'light') {
        icon.className = 'fas fa-sun';
    } else {
        icon.className = 'fas fa-moon';
    }
}

function initTheme() {
    const saved = localStorage.getItem('opb-theme');
    if (saved) {
        document.documentElement.setAttribute('data-theme', saved);
        updateThemeIcon(saved);
    } else {
        // Check system preference
        const prefersLight = window.matchMedia('(prefers-color-scheme: light)').matches;
        const theme = prefersLight ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', theme);
        updateThemeIcon(theme);
    }
}

// ============================================
// APP INIT
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    // Auth disabled for now - bypass check
    /*
    const token = localStorage.getItem('opb_token');
    if (!token) {
        window.location.href = 'auth.html';
        return;
    }

    const API_URL = localStorage.getItem('opb_api_url') || '';
    fetch(`${API_URL}/api/auth/validate`, {
        headers: { 'Authorization': `Bearer ${token}` }
    })
    .then(r => r.json())
    .then(data => {
        if (!data.success) {
            localStorage.removeItem('opb_token');
            localStorage.removeItem('opb_user');
            window.location.href = 'auth.html';
        }
    })
    .catch(() => {});
    */

    initTheme();
    updateGreeting();
    renderHeatmap();
    renderStreak();
    const hash = location.hash.replace('#','');
    // Restaurar estado do sidebar (recolhido/expandido)
    if (localStorage.getItem('sidebarCollapsed') === 'true') {
        document.getElementById('sidebar').classList.add('collapsed');
    }
    
    const startPage = (hash && document.getElementById('page-' + hash)) ? hash : 'dashboard';
    navigateTo(startPage);
    
    // Registra Service Worker para PWA offline
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/sw.js').catch((err) => {
            console.warn('SW registration failed:', err);
        });
    }
});

// ============================================
// AUTH / LOGOUT
// ============================================
function loadUserInfo() {
    const user = JSON.parse(localStorage.getItem('opb_user') || '{}');
    const emailEl = document.getElementById('cfg-user-email');
    const planEl = document.getElementById('cfg-user-plan');
    if (emailEl) emailEl.textContent = user.email || user.username || 'Usuário';
    if (planEl) planEl.textContent = `Plano: ${(user.plan || 'free').charAt(0).toUpperCase() + (user.plan || 'free').slice(1)}`;
}

async function logout() {
    if (!confirm('Deseja realmente sair?')) return;

    const token = localStorage.getItem('opb_token');
    const API_URL = localStorage.getItem('opb_api_url') || '';

    try {
        await fetch(`${API_URL}/api/auth/logout`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` }
        });
    } catch (e) {}

    localStorage.removeItem('opb_token');
    localStorage.removeItem('opb_user');
    window.location.href = 'auth.html';
}

// Load user info when config page is shown
const origNavigateTo = window.navigateTo;
if (origNavigateTo) {
    window.navigateTo = function(page) {
        origNavigateTo(page);
        if (page === 'config') {
            setTimeout(loadUserInfo, 100);
        }
    };
}

// ============================================
// PROFILE SWITCHER
// ============================================
async function loadProfiles() {
    const select = document.getElementById('profileSwitcher');
    if (!select) return;

    try {
        const res = await fetch('/api/perfis');
        const data = await res.json();

        select.innerHTML = data.perfis.map(p =>
            `<option value="${p.id}" ${p.id === data.ativo ? 'selected' : ''}>${p.icone} ${p.nome}</option>`
        ).join('');
    } catch (e) {}
}

async function switchProfile(profileId) {
    try {
        const res = await fetch('/api/perfis/ativo', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ perfil_id: profileId })
        });
        const data = await res.json();

        if (data.success) {
            localStorage.setItem('opb_profile', profileId);
            showToast(`Perfil trocado: ${data.config.nome}`, 'success');

            // Reload page data for new profile
            setTimeout(() => {
                loadPageData('dashboard');
                loadPageData('cerebro');
                loadPageData('perfil');
            }, 500);
        } else {
            showToast('Erro ao trocar perfil', 'error');
            loadProfiles(); // Reset select
        }
    } catch (e) {
        showToast('Erro ao trocar perfil', 'error');
        loadProfiles();
    }
}

// Load profiles on init
if (document.getElementById('profileSwitcher')) {
    loadProfiles();
}
