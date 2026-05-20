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
    
    // Desativa Service Worker (causava erros de cache)
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/sw.js').catch(()=>{});
    }
});

// ============================================
// QUADRO DE AVISOS
// ============================================
async function loadQuadroAvisos() {
    const data = await apiCall('/api/quadro-avisos');
    const el = document.getElementById('qa-lista');
    const concluidas = document.getElementById('qa-concluidas');
    const count = document.getElementById('qa-count');
    const badge = document.getElementById('qa-badge');
    if (!data || data.error) {
        el.innerHTML = '<div class="empty-state"><i class="fas fa-clipboard-list"></i><h3>Erro ao carregar</h3></div>';
        return;
    }
    const pendentes = data.tarefas.filter(t => t.status === 'pendente');
    const feitas = data.tarefas.filter(t => t.status === 'concluido');
    count.textContent = pendentes.length;
    if (badge) badge.textContent = pendentes.length;
    if (!pendentes.length) {
        el.innerHTML = '<div class="empty-state"><i class="fas fa-clipboard-list"></i><h3>Nenhuma tarefa pendente</h3><p>Adicione tarefas para os agentes</p></div>';
    } else {
        el.innerHTML = pendentes.map(t => renderTarefa(t)).join('');
    }
    if (!feitas.length) {
        concluidas.innerHTML = '<div class="empty-state"><i class="fas fa-check"></i><h3>Nenhuma concluída</h3></div>';
    } else {
        concluidas.innerHTML = feitas.slice(0, 10).map(t => renderTarefa(t, true)).join('');
    }
}

function renderTarefa(t, isConcluida = false) {
    const pIcon = { alta: '🔴', media: '🟡', baixa: '🟢' };
    const cores = { alta: 'var(--danger)', media: 'var(--warning)', baixa: 'var(--success)' };
    return `<div class="carrossel-slide-card" style="${isConcluida ? 'opacity:0.6' : ''}">
        <div class="slide-header">
            <div style="display:flex;align-items:center;gap:8px">
                <span style="font-size:1rem">${pIcon[t.prioridade] || '🟡'}</span>
                <span class="slide-titulo">${escapeHtml(t.tarefa)}</span>
            </div>
            <span class="tag" style="${isConcluida ? 'background:var(--success-glow);color:var(--success)' : 'background:' + cores[t.prioridade] + '20;color:' + cores[t.prioridade]}">${t.agente}</span>
        </div>
        <div style="display:flex;justify-content:space-between;align-items:center;margin-top:6px">
            <span style="font-size:0.7rem;color:var(--text-muted)">#${t.id} — ${t.criado_em}${t.concluido_em ? ' | ✅ ' + t.concluido_em : ''}</span>
            <div style="display:flex;gap:6px">
                ${!isConcluida ? `<button class="btn btn-sm btn-success" onclick="concluirTarefa(${t.id})"><i class="fas fa-check"></i></button>` : ''}
                <button class="btn btn-sm btn-danger" onclick="excluirTarefa(${t.id})"><i class="fas fa-trash"></i></button>
            </div>
        </div>
    </div>`;
}

async function adicionarTarefa() {
    const descricao = document.getElementById('qa-descricao').value.trim();
    if (!descricao) { showToast('Descreva a tarefa', 'error'); return; }
    const r = await apiCall('/api/quadro-avisos', 'POST', {
        tarefa: descricao,
        agente: document.getElementById('qa-agente').value,
        prioridade: document.getElementById('qa-prioridade').value
    });
    if (r && r.sucesso) {
        document.getElementById('qa-descricao').value = '';
        showToast('Tarefa adicionada!', 'success');
        await loadQuadroAvisos();
    } else {
        showToast('Erro: ' + (r?.error || ''), 'error');
    }
}

async function concluirTarefa(id) {
    const r = await apiCall(`/api/quadro-avisos/${id}/concluir`, 'POST');
    if (r && r.sucesso) {
        showToast('Tarefa concluída!', 'success');
        await loadQuadroAvisos();
    } else {
        showToast('Erro ao concluir', 'error');
    }
}

async function excluirTarefa(id) {
    if (!confirm('Excluir tarefa #' + id + '?')) return;
    const r = await apiCall(`/api/quadro-avisos/${id}`, 'DELETE');
    if (r && r.sucesso) {
        showToast('Tarefa excluída!', 'success');
        await loadQuadroAvisos();
    } else {
        showToast('Erro ao excluir', 'error');
    }
}

// ============================================
// INSPIRAÇÕES
// ============================================
let inspData = [];
let inspDocs = [];

async function loadInspiracoes() {
    const data = await apiCall('/api/inspiracoes');
    inspData = data.profiles || [];
    inspDocs = data.recursos || [];
    document.getElementById('insp-count').textContent = inspData.length;
    renderInspGrid(inspData);
    renderInspDocs(inspDocs);
}

function showInspTab(tab, btn) {
    document.querySelectorAll('#page-inspiracoes .tab-inline').forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');
    document.getElementById('insp-perfis').style.display = tab === 'perfis' ? '' : 'none';
    document.getElementById('insp-documentos').style.display = tab === 'documentos' ? '' : 'none';
}

function renderInspGrid(items) {
    const el = document.getElementById('insp-grid');
    if (!items.length) {
        el.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:40px;color:var(--text-muted)">Nenhum perfil encontrado</div>';
        return;
    }
    el.innerHTML = items.map(p => {
        const plat = p.platforms || {};
        const links = Object.entries(plat).map(([k, v]) => {
            const icons = { twitter:'fa-x-twitter', instagram:'fa-instagram', youtube:'fa-youtube', linkedin:'fa-linkedin', website:'fa-globe', podcast:'fa-podcast' };
            return `<a href="${v}" target="_blank" class="btn btn-sm btn-outline" style="padding:4px 10px;font-size:0.75rem"><i class="fab ${icons[k] || 'fa-link'}"></i> ${k}</a>`;
        }).join(' ');
        const tagColor = (p.nicho || '').toLowerCase().includes('cristao') || (p.nicho || '').toLowerCase().includes('catolico') ? 'green' : 'blue';
        return `<div class="card insp-card" data-nicho="${(p.nicho || '').toLowerCase()}">
            <div class="card-header">
                <div class="card-title"><i class="fas fa-user" style="color:var(--accent-light)"></i> ${p.name}</div>
                ${p.nicho ? `<span class="tag tag-${tagColor}" style="font-size:0.7rem">${p.nicho}</span>` : ''}
            </div>
            <div style="padding:12px 16px">
                ${p.descricao ? `<div style="font-size:0.8rem;color:var(--text-muted);margin-bottom:10px">${p.descricao}</div>` : ''}
                <div style="display:flex;flex-wrap:wrap;gap:6px">${links || '<span style="color:var(--text-muted);font-size:0.8rem">Sem plataformas</span>'}</div>
            </div>
        </div>`;
    }).join('');
}

function renderInspDocs(docs) {
    const el = document.getElementById('insp-docs-grid');
    if (!docs.length) {
        el.innerHTML = '<div style="text-align:center;padding:40px;color:var(--text-muted)">Nenhum documento encontrado</div>';
        return;
    }
    el.innerHTML = docs.map(d => {
        const temas = { 'financas etica':'Finanças', 'investimentos etica':'Investimentos', 'doutrina social':'DSI' };
        return `<div class="card">
            <div class="card-header">
                <div class="card-title"><i class="fas fa-file-alt" style="color:var(--warning)"></i> ${d.titulo}</div>
                <span class="tag tag-amber" style="font-size:0.7rem">${temas[d.tema] || d.tema}</span>
            </div>
            <div style="padding:12px 16px">
                <div style="font-size:0.82rem;color:var(--text-muted);margin-bottom:12px;line-height:1.5">${d.descricao}</div>
                <a href="${d.url}" target="_blank" class="btn btn-sm btn-primary"><i class="fas fa-external-link-alt"></i> Acessar</a>
            </div>
        </div>`;
    }).join('');
}

function filterInspiracoes(nicho, btn) {
    document.querySelectorAll('#insp-filters .btn').forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');
    if (nicho === 'todos') return renderInspGrid(inspData);
    const filtered = inspData.filter(p => (p.nicho || '').toLowerCase().includes(nicho));
    renderInspGrid(filtered);
}
