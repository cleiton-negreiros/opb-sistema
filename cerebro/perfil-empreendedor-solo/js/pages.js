// ============================================
// PAGES
// ============================================
async function loadPerfilData() {
    try {
        const data = await apiCall('/api/load-profile');
        if (!data || data.error) return;

        // Dados Básicos (PERFIL.md)
        if (data.basico) {
            const b = data.basico;
            if (b.nome) document.getElementById('perfil-nome').value = b.nome;
            if (b['nome publico'] || b['nome público']) document.getElementById('perfil-nome-publico').value = b['nome publico'] || b['nome público'];
            if (b.nicho) document.getElementById('perfil-nicho').value = b.nicho;
            if (b['publico alvo'] || b['público-alvo']) document.getElementById('perfil-publico').value = b['publico alvo'] || b['público-alvo'];
            if (b.problema) document.getElementById('perfil-problema').value = b.problema;
        }

        // Habilidades
        if (data.habilidades) {
            const h = data.habilidades;
            if (h.habilidades) document.getElementById('perfil-habilidades').value = h.habilidades;
            if (h.resumo) document.getElementById('perfil-habilidades-resumo').value = h.resumo;
        }

        // Histórias
        if (data.historias) {
            const h = data.historias;
            if (h['história profissional'] || h['historia profissional']) document.getElementById('perfil-historia').value = h['história profissional'] || h['historia profissional'];
            if (h.experiências || h.experiencias) document.getElementById('perfil-experiencias').value = h.experiências || h.experiencias;
        }

        // Cosmovisão
        if (data.cosmovisao) {
            const c = data.cosmovisao;
            if (c.valores) document.getElementById('perfil-valores').value = c.valores;
            if (c.crenças || c.crencas) document.getElementById('perfil-crencas').value = c.crenças || c.crencas;
        }

        // Público-Alvo
        if (data.publico) {
            const p = data.publico;
            if (p['cliente ideal'] || p.cliente) document.getElementById('perfil-cliente').value = p['cliente ideal'] || p.cliente;
            if (p.problemas) document.getElementById('perfil-problemas').value = p.problemas;
        }

        // Posicionamento
        if (data.posicionamento) {
            const p = data.posicionamento;
            if (p.diferencial) document.getElementById('perfil-diferencial').value = p.diferencial;
            if (p['proposta de valor'] || p.proposta) document.getElementById('perfil-proposta').value = p['proposta de valor'] || p.proposta;
        }

        // Narrativa
        if (data.narrativa) {
            const n = data.narrativa;
            if (n.missão || n.missao) document.getElementById('perfil-missao').value = n.missão || n.missao;
            if (n.origem) document.getElementById('perfil-origem').value = n.origem;
        }
    } catch (e) {
        console.error('Erro ao carregar perfil:', e);
    }
}

function loadPageData(page) {
    if (page === 'perfil') { loadPerfilData(); }
    else if (page === 'arquivos') { loadFileBrowser(); }
    else if (page === 'transcricao') { loadTranscricoes(); }
    else if (page === 'dashboard') {
        const stats = await apiCall('/api/stats');
        if (stats && !stats.error) {
            document.getElementById('kpi-ideas').textContent = stats.ideias_salvas || 0;
            document.getElementById('kpi-agents').textContent = stats.agentes_ativos || 0;
            document.getElementById('kpi-conhecimento').textContent = stats.conhecimento_salvo || 0;
            document.getElementById('kpi-arquivos').textContent = stats.agentes_total || 0;
        }
        const ideas = await apiCall('/api/ideias');
        const el = document.getElementById('recent-activity');
        if (ideas && ideas.ideias && ideas.ideias.length) {
            document.getElementById('kpi-ideas').textContent = ideas.ideias.length;
            el.innerHTML = ideas.ideias.slice(0,5).map(a => `
                <div style="display:flex;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid var(--border)">
                    <i class="fas fa-lightbulb" style="color:var(--warning);width:20px;text-align:center"></i>
                    <span style="flex:1;font-size:0.85rem">${escapeHtml(a.titulo)}</span>
                    <span style="font-size:0.75rem;color:var(--text-muted)">${a.data}</span>
                </div>`).join('');
        } else {
            el.innerHTML = '<div style="text-align:center;padding:20px;color:var(--text-muted)">Nenhuma atividade recente</div>';
        }
        // Check API status
        const health = await apiCall('/api/health');
        const si = document.getElementById('statusIndicator');
        const tag = document.getElementById('api-status-tag');
        if (health && health.status === 'online') {
            si.innerHTML = '<span class="status-dot"></span><span>API: Online</span>';
            si.className = 'status-indicator online';
            tag.className = 'tag tag-green';
            tag.textContent = 'API Online';
        } else {
            si.innerHTML = '<span class="status-dot"></span><span>API: Offline</span>';
            si.className = 'status-indicator offline';
            tag.className = 'tag tag-red';
            tag.textContent = 'API Offline';
        }
        // Update agent status
        await checkAgentsApi();
    }
    if (page === 'consumo') await loadKnowledge();
    if (page === 'cerebro') {
        loadCerebroTree();
        loadMapas();
    }
    if (page === 'inspiracoes') loadInspiracoes();
    if (page === 'carrossel') loadCarrosseis();
    if (page === 'quadro-avisos') loadQuadroAvisos();
}

async function checkAgentsApi() {
    const agents = await apiCall('/api/agentes');
    if (agents) {
        const st = { carrossel:'st-carrossel', consumo:'st-consumo', 'capa-video':'st-capavideo', transcricao:'st-transcricao', 'text-generator':'st-textgen', posicionamento:'st-posicionamento', narvi:'st-narvi', radagast:'st-radagast', 'quadro-avisos':'st-quadroavisos' };
        agents.forEach(a => {
            const el = document.getElementById(st[a.pasta]);
            if (el) {
                el.className = a.status === 'ativo' ? 'tag tag-green' : 'tag tag-amber';
                el.textContent = a.status === 'ativo' ? '✅ Ativo' : '🔧 Desenvolvimento';
            }
        });
    }
}


function loadCerebroTree() {
    const result = await apiCall('/api/cerebro/arvore');
    const el = document.getElementById('cerebro-tree');
    if (result && result.length) {
        document.getElementById('stat-arquivos-c').textContent = result.filter(f=>f.tipo==='arquivo').length;
        document.getElementById('stat-pastas-c').textContent = result.filter(f=>f.tipo==='pasta').length;
        el.innerHTML = result.map(f => {
            const icon = f.tipo === 'pasta' ? '📁' : '📄';
            const color = f.tipo === 'pasta' ? 'line-blue' : 'line-green';
            return `<span class="${color}">${icon} ${escapeHtml(f.caminho)}</span>`;
        }).join('<br>');
    }
}

async function loadMapas() {
    const result = await apiCall('/api/cerebro/mapas');
    const tbody = document.getElementById('mapas-tbody');
    if (result && result.length) {
        tbody.innerHTML = result.map(m => `
            <tr><td><i class="fas fa-map" style="color:var(--accent);margin-right:6px"></i> ${escapeHtml(m.caminho)}</td><td><span class="tag tag-purple">${escapeHtml(m.pasta)}</span></td><td><button class="btn btn-sm btn-outline" onclick="readMap('${escapeHtml(m.caminho)}')">Ler</button></td></tr>
        `).join('');
    } else {
        tbody.innerHTML = '<tr><td colspan="3" style="text-align:center;color:var(--text-muted)">Nenhum MAPA encontrado</td></tr>';
    }
}

async function checkIntegrity() {
    const result = await apiCall('/api/cerebro/arvore');
    if (result) {
        const files = result.filter(f=>f.tipo==='arquivo');
        const maps = files.filter(f=>f.nome==='MAPA.md');
        document.getElementById('stat-mapas').textContent = maps.length;
        showToast(`✅ Integridade OK: ${files.length} arquivos, ${maps.length} MAPAs`, 'success');
    }
}


function checkIntegrity() {
    const result = await apiCall('/api/cerebro/arvore');
    if (result) {
        const files = result.filter(f=>f.tipo==='arquivo');
        const maps = files.filter(f=>f.nome==='MAPA.md');
        document.getElementById('stat-mapas').textContent = maps.length;
        showToast(`✅ Integridade OK: ${files.length} arquivos, ${maps.length} MAPAs`, 'success');
    }
}


function loadMapas() {
    const result = await apiCall('/api/cerebro/mapas');
    const tbody = document.getElementById('mapas-tbody');
    if (result && result.length) {
        tbody.innerHTML = result.map(m => `
            <tr><td><i class="fas fa-map" style="color:var(--accent);margin-right:6px"></i> ${escapeHtml(m.caminho)}</td><td><span class="tag tag-purple">${escapeHtml(m.pasta)}</span></td><td><button class="btn btn-sm btn-outline" onclick="readMap('${escapeHtml(m.caminho)}')">Ler</button></td></tr>
        `).join('');
    } else {
        tbody.innerHTML = '<tr><td colspan="3" style="text-align:center;color:var(--text-muted)">Nenhum MAPA encontrado</td></tr>';
    }
}

async function checkIntegrity() {
    const result = await apiCall('/api/cerebro/arvore');
    if (result) {
        const files = result.filter(f=>f.tipo==='arquivo');
        const maps = files.filter(f=>f.nome==='MAPA.md');
        document.getElementById('stat-mapas').textContent = maps.length;
        showToast(`✅ Integridade OK: ${files.length} arquivos, ${maps.length} MAPAs`, 'success');
    }
}


function runTranscricao() {
    const url = document.getElementById('transcricao-url').value;
    if (!url) { showToast('Cole a URL do vídeo', 'error'); return; }
    const out = document.getElementById('transcricao-output');
    const copyBtn = document.getElementById('transcricao-copy-btn');
    out.style.display = 'block';
    copyBtn.style.display = 'none';
    out.innerHTML = `🔄 Transcrevendo...`;
    const r = await apiCall('/api/transcricao','POST',{url});
    if (r.sucesso) {
        out.innerHTML = `<pre style="white-space:pre-wrap;font-family:'JetBrains Mono',monospace;font-size:0.85rem;line-height:1.5">${escapeHtml(r.saida||'✅ Transcrição concluída!')}</pre>`;
        copyBtn.style.display = 'inline-flex';
    } else {
        out.innerHTML = `❌ ${escapeHtml(r.erro||r.mensagem||'Erro desconhecido')}`;
    }
    showToast(r.sucesso?'Transcrição concluída!':'Erro', r.sucesso?'success':'error');
    loadTranscricoes();
}

async function loadTranscricoes() {
    const r = await apiCall('/api/transcricoes','GET');
    const el = document.getElementById('transcricoes-lista');
    if (r && r.transcricoes && r.transcricoes.length) {
        el.innerHTML = r.transcricoes.map(t => `
            <div class="activity-item" onclick="viewTranscricao('${escapeHtml(t.arquivo)}')" style="cursor:pointer">
                <i class="fas fa-file-audio"></i>
                <div style="flex:1">
                    <strong>${escapeHtml(t.metadata?.video_id||t.nome)}</strong>
                    <div style="font-size:0.75rem;color:var(--text-muted)">${escapeHtml(t.metadata?.data||'')} ${escapeHtml(t.metadata?.duracao||'')}</div>
                </div>
            </div>`).join('');
    } else {
        el.innerHTML = '<div class="empty-state"><i class="fas fa-microphone-slash"></i><h3>Nenhuma transcrição</h3></div>';
    }
}

async function viewTranscricao(nome) {
    const r = await apiCall('/api/transcricao/ler','POST',{nome});
    if (r && r.sucesso) {
        const out = document.getElementById('transcricao-output');
        const copyBtn = document.getElementById('transcricao-copy-btn');
        out.style.display = 'block';
        out.innerHTML = `<pre style="white-space:pre-wrap;font-family:'JetBrains Mono',monospace;font-size:0.85rem;line-height:1.5">${escapeHtml(r.conteudo)}</pre>`;
        copyBtn.style.display = 'inline-flex';
        navigateTo('transcricao');
    } else {
        showToast('Erro ao carregar transcrição', 'error');
    }
}

async function loadFileBrowser(dir) {
    const path = dir || document.getElementById('filebrowser-path').value || '.';
    document.getElementById('filebrowser-path').value = path;
    const el = document.getElementById('filebrowser-lista');
    document.getElementById('filebrowser-card-preview').style.display = 'none';
    el.innerHTML = '<div class="empty-state"><i class="fas fa-spinner fa-spin"></i><h3>Carregando...</h3></div>';
    const r = await apiCall('/api/arquivos','POST',{caminho:path});
    if (r && !r.error && r.arquivos) {
        const items = r.arquivos;
        el.innerHTML = `<div style="padding:8px 0"><span style="color:var(--text-muted);font-size:0.8rem">${r.pai||path}</span></div>` +
            items.map(a => {
                const isDir = a.tipo === 'diretoria';
                const icon = isDir ? 'fa-folder' : 'fa-file-alt';
                const color = isDir ? 'var(--warning)' : 'var(--text-secondary)';
                return `<div class="activity-item" style="cursor:pointer" onclick="${isDir ? `loadFileBrowser('${escapeHtml(a.caminho_completo||a.nome)}')` : `viewFile('${escapeHtml(a.caminho_completo||a.nome)}')`}">
                    <i class="fas ${icon}" style="color:${color}"></i>
                    <div style="flex:1"><strong>${escapeHtml(a.nome)}</strong></div>
                    <span style="font-size:0.75rem;color:var(--text-muted)">${isDir?'📁':'📄'} ${escapeHtml(a.tamanho||'')}</span>
                </div>`;
            }).join('');
        if (r.pai) {
            el.innerHTML = `<div class="activity-item" style="cursor:pointer;opacity:0.7" onclick="loadFileBrowser('${escapeHtml(r.pai)}')">
                <i class="fas fa-level-up-alt"></i>
                <div style="flex:1"><em>Voltar</em></div>
            </div>` + el.innerHTML;
        }
    } else {
        el.innerHTML = '<div class="empty-state"><i class="fas fa-exclamation-triangle"></i><h3>Erro ao carregar</h3><p>'+escapeHtml(r.erro||'Caminho inválido')+'</p></div>';
    }
}

async function viewFile(caminho) {
    const r = await apiCall('/api/arquivo/ler','POST',{caminho});
    const previewEl = document.getElementById('filebrowser-preview');
    const cardPreview = document.getElementById('filebrowser-card-preview');
    document.getElementById('filebrowser-preview-name').textContent = caminho.split('\\').pop().split('/').pop();
    if (r && r.sucesso) {
        previewEl.innerHTML = `<pre style="white-space:pre-wrap;font-family:'JetBrains Mono',monospace;font-size:0.8rem;line-height:1.4;max-height:70vh;overflow-y:auto">${escapeHtml(r.conteudo)}</pre>`;
        cardPreview.style.display = 'block';
    } else {
        showToast('Erro ao ler arquivo', 'error');
    }
}

async function runCapaVideo() {
    const tema = document.getElementById('capa-tema').value;
    if (!tema) { showToast('Informe o tema', 'error'); return; }
    const out = document.getElementById('capa-output');
    const copyBtn = document.getElementById('capa-copy-btn');
    out.style.display = 'block';
    copyBtn.style.display = 'none';
    out.innerHTML = `🖼️ Gerando...`;
    const r = await apiCall('/api/capa-video','POST',{tema, quantidade:parseInt(document.getElementById('capa-qtd').value)});
    if (r.sucesso) {
        out.innerHTML = `<pre style="white-space:pre-wrap;font-family:'JetBrains Mono',monospace;font-size:0.85rem;line-height:1.5">${escapeHtml(r.saida||r.mensagem)}</pre>`;
        copyBtn.style.display = 'inline-flex';
    } else {
        out.innerHTML = `❌ ${escapeHtml(r.erro||r.mensagem)}`;
    }
    showToast(r.sucesso?'Capas geradas!':'Erro', r.sucesso?'success':'error');
}

let currentCarrosselFilename = '';
let currentCarrosselOriginal = '';


function runCapaVideo() {
    const tema = document.getElementById('capa-tema').value;
    if (!tema) { showToast('Informe o tema', 'error'); return; }
    const out = document.getElementById('capa-output');
    const copyBtn = document.getElementById('capa-copy-btn');
    out.style.display = 'block';
    copyBtn.style.display = 'none';
    out.innerHTML = `🖼️ Gerando...`;
    const r = await apiCall('/api/capa-video','POST',{tema, quantidade:parseInt(document.getElementById('capa-qtd').value)});
    if (r.sucesso) {
        out.innerHTML = `<pre style="white-space:pre-wrap;font-family:'JetBrains Mono',monospace;font-size:0.85rem;line-height:1.5">${escapeHtml(r.saida||r.mensagem)}</pre>`;
        copyBtn.style.display = 'inline-flex';
    } else {
        out.innerHTML = `❌ ${escapeHtml(r.erro||r.mensagem)}`;
    }
    showToast(r.sucesso?'Capas geradas!':'Erro', r.sucesso?'success':'error');
}

let currentCarrosselFilename = '';
let currentCarrosselOriginal = '';


function runConsumo() {
    const input = document.getElementById('consumo-input').value;
    if (!input.trim()) { showToast('Cole um texto ou URL', 'error'); return; }
    const out = document.getElementById('consumo-output');
    out.style.display = 'block';
    const titulo = document.getElementById('consumo-titulo').value || 'Conteúdo';
    out.innerHTML = `📖 Processando "${escapeHtml(titulo)}"...`;
    const r = await apiCall('/api/consumo','POST',{input:input.slice(0,3000), tipo:document.getElementById('consumo-tipo').value, titulo});
    if (r.sucesso) out.innerHTML = `📖 ${escapeHtml(r.mensagem)}\n\n${escapeHtml(r.saida||'')}`;
    else out.innerHTML = `❌ ${escapeHtml(r.erro||r.mensagem)}`;
    showToast(r.sucesso?'Conteúdo processado!':'Erro', r.sucesso?'success':'error');
}

async function runTextGenerator() {
    const obj = document.getElementById('text-gen-objetivo').value;
    if (!obj.trim()) { showToast('Informe o objetivo', 'error'); return; }
    const out = document.getElementById('text-gen-output');
    const copyBtn = document.getElementById('textgen-copy-btn');
    out.style.display = 'block';
    copyBtn.style.display = 'none';
    out.innerHTML = `✍️ Gerando...`;
    const r = await apiCall('/api/text-generator','POST',{objetivo:obj, tipo:document.getElementById('text-gen-tipo').value});
    if (r.sucesso) {
        out.innerHTML = `<pre style="white-space:pre-wrap;font-family:'JetBrains Mono',monospace;font-size:0.85rem;line-height:1.5">${escapeHtml(r.saida||r.mensagem)}</pre>`;
        copyBtn.style.display = 'inline-flex';
    } else {
        out.innerHTML = `❌ ${escapeHtml(r.erro||r.mensagem)}`;
    }
    showToast(r.sucesso?'Post gerado!':'Erro', r.sucesso?'success':'error');
}

async function runNarvi() {
    const videoInput = document.getElementById('narvi-video');
    if (!videoInput.files[0]) { showToast('Selecione um vídeo', 'error'); return; }
    const out = document.getElementById('narvi-output');
    out.style.display = 'block';
    const r = await apiCall('/api/narvi','POST',{video:videoInput.files[0].name, corte:document.getElementById('narvi-corte').value, ratio:document.getElementById('narvi-ratio').value});
    if (r && r.sucesso) {
        out.innerHTML = `<pre style="white-space:pre-wrap;font-family:'JetBrains Mono',monospace;font-size:0.85rem;line-height:1.5">${escapeHtml(r.instrucao||r.mensagem)}\n\nSaída: ${escapeHtml(r.saida||'~/Desktop/narvi-saida/')}</pre>`;
    } else {
        out.innerHTML = `❌ ${escapeHtml(r.erro||'Erro ao processar')}`;
    }
    showToast('Verifique o terminal para executar', 'info');
}

async function runRadagast() {
    const out = document.getElementById('radagast-history');
    out.innerHTML = `<div style="padding:20px;text-align:center"><i class="fas fa-spinner fa-spin" style="font-size:2rem;color:var(--warning)"></i><p style="margin-top:10px">Executando curadoria...</p></div>`;
    const r = await apiCall('/api/radagast','POST',{days_back:1});
    if (r && r.sucesso) {
        out.innerHTML = `<div style="padding:20px;background:var(--bg-input);border-radius:8px"><strong>${escapeHtml(r.mensagem||'Radagast')}</strong><p style="color:var(--text-muted);margin-top:8px">${escapeHtml(r.instrucao||'')}</p><p style="margin-top:12px">Execute no terminal:</p><code style="display:block;padding:10px;background:var(--bg-dark);border-radius:4px;margin-top:8px">${escapeHtml(r.execucao||'python agents/radagast/radagast.py')}</code></div>`;
    } else {
        out.innerHTML = `❌ ${escapeHtml(r.erro||'Erro')}`;
    }
    showToast('Radagast requer execução via terminal', 'info');
}

async function analyzeCompetitors() {
    const nicho = document.getElementById('posicionamento-nicho').value;
    const conc = document.getElementById('posicionamento-concorrentes').value;
    const out = document.getElementById('posicionamento-output');
    if (!nicho || !conc.trim()) { showToast('Preencha nicho e concorrentes', 'error'); return; }
    out.style.display = 'block';
    out.innerHTML = `📊 Analisando...`;
    const r = await apiCall('/api/posicionamento','POST',{nicho, concorrentes:conc.split('\n').filter(l=>l.trim()).join(' ')});
    out.innerHTML = escapeHtml((r&&r.analise)||(r&&r.mensagem)||conc.split('\n').filter(l=>l.trim()).map((c,i)=>`${i+1}. @${c.trim()}`).join('\n'));
    showToast('Análise concluída!', 'info');
}

async function savePosicionamento() {
    const v = document.getElementById('minha-verdade').value;
    const f = document.getElementById('frase-posicionamento').value;
    if (!v||!f) { showToast('Preencha os campos', 'error'); return; }
    showToast('Posicionamento salvo!', 'success');
}

async function runAlimentarFromModal() {
    const input = document.getElementById('alimentar-input').value;
    if (!input.trim()) { showToast('Cole o conteúdo', 'error'); return; }
    const out = document.getElementById('alimentar-output');
    out.style.display = 'block';
    out.innerHTML = `🧠 Processando...`;
    const r = await apiCall('/api/alimentar','POST',{input:input.slice(0,3000), tipo:document.getElementById('alimentar-tipo').value, titulo:'Perfil Empreendedor'});
    out.innerHTML = r.sucesso ? `✅ ${escapeHtml(r.mensagem)}\n\n${escapeHtml(r.saida||r.arquivo||'')}` : `❌ ${escapeHtml(r.erro||r.mensagem)}`;
    showToast(r.sucesso?'🧠 Cérebro alimentado!':'Erro', r.sucesso?'success':'error');
}


function runTextGenerator() {
    const obj = document.getElementById('text-gen-objetivo').value;
    if (!obj.trim()) { showToast('Informe o objetivo', 'error'); return; }
    const out = document.getElementById('text-gen-output');
    const copyBtn = document.getElementById('textgen-copy-btn');
    out.style.display = 'block';
    copyBtn.style.display = 'none';
    out.innerHTML = `✍️ Gerando...`;
    const r = await apiCall('/api/text-generator','POST',{objetivo:obj, tipo:document.getElementById('text-gen-tipo').value});
    if (r.sucesso) {
        out.innerHTML = `<pre style="white-space:pre-wrap;font-family:'JetBrains Mono',monospace;font-size:0.85rem;line-height:1.5">${escapeHtml(r.saida||r.mensagem)}</pre>`;
        copyBtn.style.display = 'inline-flex';
    } else {
        out.innerHTML = `❌ ${escapeHtml(r.erro||r.mensagem)}`;
    }
    showToast(r.sucesso?'Post gerado!':'Erro', r.sucesso?'success':'error');
}

async function runNarvi() {
    const videoInput = document.getElementById('narvi-video');
    if (!videoInput.files[0]) { showToast('Selecione um vídeo', 'error'); return; }
    const out = document.getElementById('narvi-output');
    out.style.display = 'block';
    const r = await apiCall('/api/narvi','POST',{video:videoInput.files[0].name, corte:document.getElementById('narvi-corte').value, ratio:document.getElementById('narvi-ratio').value});
    if (r && r.sucesso) {
        out.innerHTML = `<pre style="white-space:pre-wrap;font-family:'JetBrains Mono',monospace;font-size:0.85rem;line-height:1.5">${escapeHtml(r.instrucao||r.mensagem)}\n\nSaída: ${escapeHtml(r.saida||'~/Desktop/narvi-saida/')}</pre>`;
    } else {
        out.innerHTML = `❌ ${escapeHtml(r.erro||'Erro ao processar')}`;
    }
    showToast('Verifique o terminal para executar', 'info');
}

async function runRadagast() {
    const out = document.getElementById('radagast-history');
    out.innerHTML = `<div style="padding:20px;text-align:center"><i class="fas fa-spinner fa-spin" style="font-size:2rem;color:var(--warning)"></i><p style="margin-top:10px">Executando curadoria...</p></div>`;
    const r = await apiCall('/api/radagast','POST',{days_back:1});
    if (r && r.sucesso) {
        out.innerHTML = `<div style="padding:20px;background:var(--bg-input);border-radius:8px"><strong>${escapeHtml(r.mensagem||'Radagast')}</strong><p style="color:var(--text-muted);margin-top:8px">${escapeHtml(r.instrucao||'')}</p><p style="margin-top:12px">Execute no terminal:</p><code style="display:block;padding:10px;background:var(--bg-dark);border-radius:4px;margin-top:8px">${escapeHtml(r.execucao||'python agents/radagast/radagast.py')}</code></div>`;
    } else {
        out.innerHTML = `❌ ${escapeHtml(r.erro||'Erro')}`;
    }
    showToast('Radagast requer execução via terminal', 'info');
}

async function analyzeCompetitors() {
    const nicho = document.getElementById('posicionamento-nicho').value;
    const conc = document.getElementById('posicionamento-concorrentes').value;
    const out = document.getElementById('posicionamento-output');
    if (!nicho || !conc.trim()) { showToast('Preencha nicho e concorrentes', 'error'); return; }
    out.style.display = 'block';
    out.innerHTML = `📊 Analisando...`;
    const r = await apiCall('/api/posicionamento','POST',{nicho, concorrentes:conc.split('\n').filter(l=>l.trim()).join(' ')});
    out.innerHTML = escapeHtml((r&&r.analise)||(r&&r.mensagem)||conc.split('\n').filter(l=>l.trim()).map((c,i)=>`${i+1}. @${c.trim()}`).join('\n'));
    showToast('Análise concluída!', 'info');
}

async function savePosicionamento() {
    const v = document.getElementById('minha-verdade').value;
    const f = document.getElementById('frase-posicionamento').value;
    if (!v||!f) { showToast('Preencha os campos', 'error'); return; }
    showToast('Posicionamento salvo!', 'success');
}

async function runAlimentarFromModal() {
    const input = document.getElementById('alimentar-input').value;
    if (!input.trim()) { showToast('Cole o conteúdo', 'error'); return; }
    const out = document.getElementById('alimentar-output');
    out.style.display = 'block';
    out.innerHTML = `🧠 Processando...`;
    const r = await apiCall('/api/alimentar','POST',{input:input.slice(0,3000), tipo:document.getElementById('alimentar-tipo').value, titulo:'Perfil Empreendedor'});
    out.innerHTML = r.sucesso ? `✅ ${escapeHtml(r.mensagem)}\n\n${escapeHtml(r.saida||r.arquivo||'')}` : `❌ ${escapeHtml(r.erro||r.mensagem)}`;
    showToast(r.sucesso?'🧠 Cérebro alimentado!':'Erro', r.sucesso?'success':'error');
}


function runNarvi() {
    const videoInput = document.getElementById('narvi-video');
    if (!videoInput.files[0]) { showToast('Selecione um vídeo', 'error'); return; }
    const out = document.getElementById('narvi-output');
    out.style.display = 'block';
    const r = await apiCall('/api/narvi','POST',{video:videoInput.files[0].name, corte:document.getElementById('narvi-corte').value, ratio:document.getElementById('narvi-ratio').value});
    if (r && r.sucesso) {
        out.innerHTML = `<pre style="white-space:pre-wrap;font-family:'JetBrains Mono',monospace;font-size:0.85rem;line-height:1.5">${escapeHtml(r.instrucao||r.mensagem)}\n\nSaída: ${escapeHtml(r.saida||'~/Desktop/narvi-saida/')}</pre>`;
    } else {
        out.innerHTML = `❌ ${escapeHtml(r.erro||'Erro ao processar')}`;
    }
    showToast('Verifique o terminal para executar', 'info');
}

async function runRadagast() {
    const out = document.getElementById('radagast-history');
    out.innerHTML = `<div style="padding:20px;text-align:center"><i class="fas fa-spinner fa-spin" style="font-size:2rem;color:var(--warning)"></i><p style="margin-top:10px">Executando curadoria...</p></div>`;
    const r = await apiCall('/api/radagast','POST',{days_back:1});
    if (r && r.sucesso) {
        out.innerHTML = `<div style="padding:20px;background:var(--bg-input);border-radius:8px"><strong>${escapeHtml(r.mensagem||'Radagast')}</strong><p style="color:var(--text-muted);margin-top:8px">${escapeHtml(r.instrucao||'')}</p><p style="margin-top:12px">Execute no terminal:</p><code style="display:block;padding:10px;background:var(--bg-dark);border-radius:4px;margin-top:8px">${escapeHtml(r.execucao||'python agents/radagast/radagast.py')}</code></div>`;
    } else {
        out.innerHTML = `❌ ${escapeHtml(r.erro||'Erro')}`;
    }
    showToast('Radagast requer execução via terminal', 'info');
}

async function analyzeCompetitors() {
    const nicho = document.getElementById('posicionamento-nicho').value;
    const conc = document.getElementById('posicionamento-concorrentes').value;
    const out = document.getElementById('posicionamento-output');
    if (!nicho || !conc.trim()) { showToast('Preencha nicho e concorrentes', 'error'); return; }
    out.style.display = 'block';
    out.innerHTML = `📊 Analisando...`;
    const r = await apiCall('/api/posicionamento','POST',{nicho, concorrentes:conc.split('\n').filter(l=>l.trim()).join(' ')});
    out.innerHTML = escapeHtml((r&&r.analise)||(r&&r.mensagem)||conc.split('\n').filter(l=>l.trim()).map((c,i)=>`${i+1}. @${c.trim()}`).join('\n'));
    showToast('Análise concluída!', 'info');
}

async function savePosicionamento() {
    const v = document.getElementById('minha-verdade').value;
    const f = document.getElementById('frase-posicionamento').value;
    if (!v||!f) { showToast('Preencha os campos', 'error'); return; }
    showToast('Posicionamento salvo!', 'success');
}

async function runAlimentarFromModal() {
    const input = document.getElementById('alimentar-input').value;
    if (!input.trim()) { showToast('Cole o conteúdo', 'error'); return; }
    const out = document.getElementById('alimentar-output');
    out.style.display = 'block';
    out.innerHTML = `🧠 Processando...`;
    const r = await apiCall('/api/alimentar','POST',{input:input.slice(0,3000), tipo:document.getElementById('alimentar-tipo').value, titulo:'Perfil Empreendedor'});
    out.innerHTML = r.sucesso ? `✅ ${escapeHtml(r.mensagem)}\n\n${escapeHtml(r.saida||r.arquivo||'')}` : `❌ ${escapeHtml(r.erro||r.mensagem)}`;
    showToast(r.sucesso?'🧠 Cérebro alimentado!':'Erro', r.sucesso?'success':'error');
}


function runRadagast() {
    const out = document.getElementById('radagast-history');
    out.innerHTML = `<div style="padding:20px;text-align:center"><i class="fas fa-spinner fa-spin" style="font-size:2rem;color:var(--warning)"></i><p style="margin-top:10px">Executando curadoria...</p></div>`;
    const r = await apiCall('/api/radagast','POST',{days_back:1});
    if (r && r.sucesso) {
        out.innerHTML = `<div style="padding:20px;background:var(--bg-input);border-radius:8px"><strong>${escapeHtml(r.mensagem||'Radagast')}</strong><p style="color:var(--text-muted);margin-top:8px">${escapeHtml(r.instrucao||'')}</p><p style="margin-top:12px">Execute no terminal:</p><code style="display:block;padding:10px;background:var(--bg-dark);border-radius:4px;margin-top:8px">${escapeHtml(r.execucao||'python agents/radagast/radagast.py')}</code></div>`;
    } else {
        out.innerHTML = `❌ ${escapeHtml(r.erro||'Erro')}`;
    }
    showToast('Radagast requer execução via terminal', 'info');
}

async function analyzeCompetitors() {
    const nicho = document.getElementById('posicionamento-nicho').value;
    const conc = document.getElementById('posicionamento-concorrentes').value;
    const out = document.getElementById('posicionamento-output');
    if (!nicho || !conc.trim()) { showToast('Preencha nicho e concorrentes', 'error'); return; }
    out.style.display = 'block';
    out.innerHTML = `📊 Analisando...`;
    const r = await apiCall('/api/posicionamento','POST',{nicho, concorrentes:conc.split('\n').filter(l=>l.trim()).join(' ')});
    out.innerHTML = escapeHtml((r&&r.analise)||(r&&r.mensagem)||conc.split('\n').filter(l=>l.trim()).map((c,i)=>`${i+1}. @${c.trim()}`).join('\n'));
    showToast('Análise concluída!', 'info');
}

async function savePosicionamento() {
    const v = document.getElementById('minha-verdade').value;
    const f = document.getElementById('frase-posicionamento').value;
    if (!v||!f) { showToast('Preencha os campos', 'error'); return; }
    showToast('Posicionamento salvo!', 'success');
}

async function runAlimentarFromModal() {
    const input = document.getElementById('alimentar-input').value;
    if (!input.trim()) { showToast('Cole o conteúdo', 'error'); return; }
    const out = document.getElementById('alimentar-output');
    out.style.display = 'block';
    out.innerHTML = `🧠 Processando...`;
    const r = await apiCall('/api/alimentar','POST',{input:input.slice(0,3000), tipo:document.getElementById('alimentar-tipo').value, titulo:'Perfil Empreendedor'});
    out.innerHTML = r.sucesso ? `✅ ${escapeHtml(r.mensagem)}\n\n${escapeHtml(r.saida||r.arquivo||'')}` : `❌ ${escapeHtml(r.erro||r.mensagem)}`;
    showToast(r.sucesso?'🧠 Cérebro alimentado!':'Erro', r.sucesso?'success':'error');
}


function runAlimentarFromModal() {
    const input = document.getElementById('alimentar-input').value;
    if (!input.trim()) { showToast('Cole o conteúdo', 'error'); return; }
    const out = document.getElementById('alimentar-output');
    out.style.display = 'block';
    out.innerHTML = `🧠 Processando...`;
    const r = await apiCall('/api/alimentar','POST',{input:input.slice(0,3000), tipo:document.getElementById('alimentar-tipo').value, titulo:'Perfil Empreendedor'});
    out.innerHTML = r.sucesso ? `✅ ${escapeHtml(r.mensagem)}\n\n${escapeHtml(r.saida||r.arquivo||'')}` : `❌ ${escapeHtml(r.erro||r.mensagem)}`;
    showToast(r.sucesso?'🧠 Cérebro alimentado!':'Erro', r.sucesso?'success':'error');
}


async function savePerfil(){
    const n=document.getElementById('perfil-nome').value;
    if(!n){showToast('Preencha seu nome','error');return}
    const content='---\nname: "Basico"\nupdated_at: '+new Date().toISOString().split('T')[0]+'\n---\n\n## Nome\n\n'+n+'\n\n## Nome Publico\n\n'+document.getElementById('perfil-nome-publico').value+'\n\n## Nicho\n\n'+document.getElementById('perfil-nicho').value+'\n\n## Publico Alvo\n\n'+document.getElementById('perfil-publico').value+'\n\n## Problema\n\n'+document.getElementById('perfil-problema').value+'\n';
    try{
        const r=await apiCall('/api/save-profile','POST',{modulo:'basico',content,filename:'PERFIL.md'});
        if(r.success||r.sucesso)showToast('Perfil salvo!','success');
        else showToast('Erro: '+(r.error||r.erro||''),'error');
    }catch(e){showToast('Erro ao salvar: '+e.message,'error')}
}

async function savePerfilModulo(modulo) {
    let content = '';
    let filename = '';

    switch(modulo) {
        case 'habilidades':
            filename = 'HABILIDADES.md';
            content = '## Habilidades\n\n' + (document.getElementById('perfil-habilidades').value || '') + '\n\n## Resumo\n\n' + (document.getElementById('perfil-habilidades-resumo').value || '');
            break;
        case 'historias':
            filename = 'HISTORIAS.md';
            content = '## História Profissional\n\n' + (document.getElementById('perfil-historia').value || '') + '\n\n## Experiências\n\n' + (document.getElementById('perfil-experiencias').value || '');
            break;
        case 'cosmovisao':
            filename = 'COSMOVISAO.md';
            content = '## Valores\n\n' + (document.getElementById('perfil-valores').value || '') + '\n\n## Crenças\n\n' + (document.getElementById('perfil-crencas').value || '');
            break;
        case 'publico':
            filename = 'PUBLICO-ALVO.md';
            content = '## Cliente Ideal\n\n' + (document.getElementById('perfil-cliente').value || '') + '\n\n## Problemas\n\n' + (document.getElementById('perfil-problemas').value || '');
            break;
        case 'posicionamento':
            filename = 'POSICIONAMENTO.md';
            content = '## Diferencial\n\n' + (document.getElementById('perfil-diferencial').value || '') + '\n\n## Proposta de Valor\n\n' + (document.getElementById('perfil-proposta').value || '');
            break;
        case 'narrativa':
            filename = 'NARRATIVA.md';
            content = '## Missão\n\n' + (document.getElementById('perfil-missao').value || '') + '\n\n## Origem\n\n' + (document.getElementById('perfil-origem').value || '');
            break;
        default:
            showToast('Módulo desconhecido', 'error');
            return;
    }

    try {
        const r = await apiCall('/api/save-profile', 'POST', { modulo, content, filename });
        if (r.success || r.sucesso) showToast(`${modulo.charAt(0).toUpperCase() + modulo.slice(1)} salvo!`, 'success');
        else showToast('Erro: ' + (r.error || r.erro || ''), 'error');
    } catch(e) {
        showToast('Erro ao salvar: ' + e.message, 'error');
    }
}


function togglePomodoro() {
    pR1=!pR1;
    const b=document.getElementById('pomodoro-btn');
    if(pR1){b.innerHTML='<i class="fas fa-pause"></i> Pausar';b.className='btn btn-warning btn-lg';pI1=setInterval(()=>{pS1--;updateTimer('pomodoro-timer',pS1);if(pS1<=0){clearInterval(pI1);pS1=25*60;pR1=false;b.innerHTML='<i class="fas fa-play"></i> Iniciar';b.className='btn btn-success btn-lg';showToast('✅ Ciclo completo!','success')}},1000)}
    else{clearInterval(pI1);b.innerHTML='<i class="fas fa-play"></i> Iniciar';b.className='btn btn-success btn-lg'}
}

function togglePomodoro2() {
    pR2=!pR2;
    const b=document.getElementById('pomo-btn2');
    if(pR2){b.innerHTML='<i class="fas fa-pause"></i>';b.className='btn btn-warning btn-lg';pI2=setInterval(()=>{pS2--;updateTimer('pomodoro-timer2',pS2);if(pS2<=0){clearInterval(pI2);pS2=25*60;pR2=false;b.innerHTML='<i class="fas fa-play"></i>';b.className='btn btn-success btn-lg'}},1000)}
    else{clearInterval(pI2);b.innerHTML='<i class="fas fa-play"></i>';b.className='btn btn-success btn-lg'}
}

function resetPomodoro(){clearInterval(pI1);pR1=false;pS1=25*60;updateTimer('pomodoro-timer',pS1);document.getElementById('pomodoro-btn').innerHTML='<i class="fas fa-play"></i> Iniciar';document.getElementById('pomodoro-btn').className='btn btn-success btn-lg'}

function resetPomodoro2(){clearInterval(pI2);pR2=false;pS2=25*60;updateTimer('pomodoro-timer2',pS2);document.getElementById('pomo-btn2').innerHTML='<i class="fas fa-play"></i>';document.getElementById('pomo-btn2').className='btn btn-success btn-lg'}

function skipPomodoro(){pS2=1}


function updateTimer(id,s){const m=Math.floor(s/60),ss=s%60;document.getElementById(id).textContent=String(m).padStart(2,'0')+':'+String(ss).padStart(2,'0')}

function updateTaskCount(){const items=document.querySelectorAll('#tasks-list .todo-item'),checked=document.querySelectorAll('#tasks-list input[type="checkbox"]:checked');document.getElementById('tasks-today').textContent=items.length;document.getElementById('pomo-done').textContent=checked.length;document.getElementById('pomo-focus').textContent=checked.length*25}

function addTask(){const l=document.getElementById('tasks-list');if(l.querySelector('.empty-state'))l.innerHTML='';const d=document.createElement('div');d.className='todo-item';d.style.cssText='display:flex;align-items:center;gap:10px;padding:12px;border-radius:8px;margin-bottom:6px;background:var(--bg-input)';d.innerHTML='<input type="checkbox" onchange="updateTaskCount(this)" style="accent-color:var(--accent);width:18px;height:18px"><input type="text" placeholder="Nova tarefa..." style="background:transparent;border:none;color:var(--text-primary);flex:1;font-size:0.9rem" onkeypress="if(event.key===\'Enter\')this.blur()"><button onclick="this.closest(\'.todo-item\').remove();updateTaskCount()" style="background:none;border:none;color:var(--text-muted);cursor:pointer;padding:4px"><i class="fas fa-trash"></i></button>';l.appendChild(d);updateTaskCount()}

function loadFileBrowser(dir) {
    const path = dir || document.getElementById('filebrowser-path').value || '.';
    document.getElementById('filebrowser-path').value = path;
    const el = document.getElementById('filebrowser-lista');
    document.getElementById('filebrowser-card-preview').style.display = 'none';
    el.innerHTML = '<div class="empty-state"><i class="fas fa-spinner fa-spin"></i><h3>Carregando...</h3></div>';
    const r = await apiCall('/api/arquivos','POST',{caminho:path});
    if (r && !r.error && r.arquivos) {
        const items = r.arquivos;
        el.innerHTML = `<div style="padding:8px 0"><span style="color:var(--text-muted);font-size:0.8rem">${r.pai||path}</span></div>` +
            items.map(a => {
                const isDir = a.tipo === 'diretoria';
                const icon = isDir ? 'fa-folder' : 'fa-file-alt';
                const color = isDir ? 'var(--warning)' : 'var(--text-secondary)';
                return `<div class="activity-item" style="cursor:pointer" onclick="${isDir ? `loadFileBrowser('${escapeHtml(a.caminho_completo||a.nome)}')` : `viewFile('${escapeHtml(a.caminho_completo||a.nome)}')`}">
                    <i class="fas ${icon}" style="color:${color}"></i>
                    <div style="flex:1"><strong>${escapeHtml(a.nome)}</strong></div>
                    <span style="font-size:0.75rem;color:var(--text-muted)">${isDir?'📁':'📄'} ${escapeHtml(a.tamanho||'')}</span>
                </div>`;
            }).join('');
        if (r.pai) {
            el.innerHTML = `<div class="activity-item" style="cursor:pointer;opacity:0.7" onclick="loadFileBrowser('${escapeHtml(r.pai)}')">
                <i class="fas fa-level-up-alt"></i>
                <div style="flex:1"><em>Voltar</em></div>
            </div>` + el.innerHTML;
        }
    } else {
        el.innerHTML = '<div class="empty-state"><i class="fas fa-exclamation-triangle"></i><h3>Erro ao carregar</h3><p>'+escapeHtml(r.erro||'Caminho inválido')+'</p></div>';
    }
}

async function viewFile(caminho) {
    const r = await apiCall('/api/arquivo/ler','POST',{caminho});
    const previewEl = document.getElementById('filebrowser-preview');
    const cardPreview = document.getElementById('filebrowser-card-preview');
    document.getElementById('filebrowser-preview-name').textContent = caminho.split('\\').pop().split('/').pop();
    if (r && r.sucesso) {
        previewEl.innerHTML = `<pre style="white-space:pre-wrap;font-family:'JetBrains Mono',monospace;font-size:0.8rem;line-height:1.4;max-height:70vh;overflow-y:auto">${escapeHtml(r.conteudo)}</pre>`;
        cardPreview.style.display = 'block';
    } else {
        showToast('Erro ao ler arquivo', 'error');
    }
}

async function runCapaVideo() {
    const tema = document.getElementById('capa-tema').value;
    if (!tema) { showToast('Informe o tema', 'error'); return; }
    const out = document.getElementById('capa-output');
    const copyBtn = document.getElementById('capa-copy-btn');
    out.style.display = 'block';
    copyBtn.style.display = 'none';
    out.innerHTML = `🖼️ Gerando...`;
    const r = await apiCall('/api/capa-video','POST',{tema, quantidade:parseInt(document.getElementById('capa-qtd').value)});
    if (r.sucesso) {
        out.innerHTML = `<pre style="white-space:pre-wrap;font-family:'JetBrains Mono',monospace;font-size:0.85rem;line-height:1.5">${escapeHtml(r.saida||r.mensagem)}</pre>`;
        copyBtn.style.display = 'inline-flex';
    } else {
        out.innerHTML = `❌ ${escapeHtml(r.erro||r.mensagem)}`;
    }
    showToast(r.sucesso?'Capas geradas!':'Erro', r.sucesso?'success':'error');
}

let currentCarrosselFilename = '';
let currentCarrosselOriginal = '';


function loadInspiracoes() {
    const data = await apiCall('/api/inspiracoes');
    inspData = data.profiles || [];
    inspDocs = data.recursos || [];
    document.getElementById('insp-count').textContent = inspData.length;
    renderInspGrid(inspData);
    renderInspDocs(inspDocs);
}


function filterInspiracoes(nicho, btn) {
    document.querySelectorAll('#insp-filters .btn').forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');
    if (nicho === 'todos') return renderInspGrid(inspData);
    const filtered = inspData.filter(p => (p.nicho || '').toLowerCase().includes(nicho));
    renderInspGrid(filtered);
}
function showInspTab(tab, btn) {
    document.querySelectorAll('#page-inspiracoes .tab-inline').forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');
    document.getElementById('insp-perfis').style.display = tab === 'perfis' ? '' : 'none';
    document.getElementById('insp-documentos').style.display = tab === 'documentos' ? '' : 'none';
}


function saveConfig(){
     const apiUrl = document.getElementById('cfg-api-url')?.value;
     const token = document.getElementById('cfg-telegram-token')?.value;
     localStorage.setItem('opb-api-url', apiUrl || 'http://localhost:5000');
     if (token) {
         fetch(apiUrl + '/api/config/telegram', {
             method: 'POST',
             headers: { 'Content-Type': 'application/json' },
             body: JSON.stringify({ token })
         }).then(r => r.json()).then(d => {
             showToast(d.sucesso ? 'Token salvo!' : 'Erro: ' + (d.erro || 'desconhecido'));
         }).catch(e => showToast('Erro ao salvar token: ' + e.message));
     }
     showToast('Configuracoes salvas!','success');
 }
async function startBot(){
    showToast('Iniciando Telegram Bot...','info');
    const r=await apiCall('/api/bot/start','POST',{});
    if(r&&r.sucesso){showToast('🤖 Bot iniciado!','success');document.getElementById('botStatus').textContent='Bot: Online'}
    else{showToast('Erro: '+(r?.erro||''),'error');document.getElementById('botStatus').textContent='Bot: Offline'}
}

function startBot(){
    showToast('Iniciando Telegram Bot...','info');
    const r=await apiCall('/api/bot/start','POST',{});
    if(r&&r.sucesso){showToast('🤖 Bot iniciado!','success');document.getElementById('botStatus').textContent='Bot: Online'}
    else{showToast('Erro: '+(r?.erro||''),'error');document.getElementById('botStatus').textContent='Bot: Offline'}
}

function checkDeps(){showToast('Verificando dependências... (verifique no terminal)','info')}

function exportLog(){const c='OPB Sistema - Log Exportado\nData: '+new Date().toLocaleString('pt-BR')+'\nAgentes: '+document.getElementById('kpi-agents').textContent+'\nIdeias: '+document.getElementById('kpi-ideas').textContent+'\n';const blob=new Blob([c],{type:'text/plain'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='opb-log-'+new Date().toISOString().split('T')[0]+'.txt';a.click();showToast('Log exportado!','success')}


function copyOutput(id) {
    const out = document.getElementById(id);
    const text = out.textContent || out.innerText;
    navigator.clipboard.writeText(text).then(() => {
        showToast('Conteúdo copiado!', 'success');
    }).catch(() => {
        const ta = document.createElement('textarea');
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        ta.remove();
        showToast('Conteúdo copiado!', 'success');
    });
}

async function runConsumo() {
    const input = document.getElementById('consumo-input').value;
    if (!input.trim()) { showToast('Cole um texto ou URL', 'error'); return; }
    const out = document.getElementById('consumo-output');
    out.style.display = 'block';
    const titulo = document.getElementById('consumo-titulo').value || 'Conteúdo';
    out.innerHTML = `📖 Processando "${escapeHtml(titulo)}"...`;
    const r = await apiCall('/api/consumo','POST',{input:input.slice(0,3000), tipo:document.getElementById('consumo-tipo').value, titulo});
    if (r.sucesso) out.innerHTML = `📖 ${escapeHtml(r.mensagem)}\n\n${escapeHtml(r.saida||'')}`;
    else out.innerHTML = `❌ ${escapeHtml(r.erro||r.mensagem)}`;
    showToast(r.sucesso?'Conteúdo processado!':'Erro', r.sucesso?'success':'error');
}

async function runTextGenerator() {
    const obj = document.getElementById('text-gen-objetivo').value;
    if (!obj.trim()) { showToast('Informe o objetivo', 'error'); return; }
    const out = document.getElementById('text-gen-output');
    const copyBtn = document.getElementById('textgen-copy-btn');
    out.style.display = 'block';
    copyBtn.style.display = 'none';
    out.innerHTML = `✍️ Gerando...`;
    const r = await apiCall('/api/text-generator','POST',{objetivo:obj, tipo:document.getElementById('text-gen-tipo').value});
    if (r.sucesso) {
        out.innerHTML = `<pre style="white-space:pre-wrap;font-family:'JetBrains Mono',monospace;font-size:0.85rem;line-height:1.5">${escapeHtml(r.saida||r.mensagem)}</pre>`;
        copyBtn.style.display = 'inline-flex';
    } else {
        out.innerHTML = `❌ ${escapeHtml(r.erro||r.mensagem)}`;
    }
    showToast(r.sucesso?'Post gerado!':'Erro', r.sucesso?'success':'error');
}

async function runNarvi() {
    const videoInput = document.getElementById('narvi-video');
    if (!videoInput.files[0]) { showToast('Selecione um vídeo', 'error'); return; }
    const out = document.getElementById('narvi-output');
    out.style.display = 'block';
    const r = await apiCall('/api/narvi','POST',{video:videoInput.files[0].name, corte:document.getElementById('narvi-corte').value, ratio:document.getElementById('narvi-ratio').value});
    if (r && r.sucesso) {
        out.innerHTML = `<pre style="white-space:pre-wrap;font-family:'JetBrains Mono',monospace;font-size:0.85rem;line-height:1.5">${escapeHtml(r.instrucao||r.mensagem)}\n\nSaída: ${escapeHtml(r.saida||'~/Desktop/narvi-saida/')}</pre>`;
    } else {
        out.innerHTML = `❌ ${escapeHtml(r.erro||'Erro ao processar')}`;
    }
    showToast('Verifique o terminal para executar', 'info');
}

async function runRadagast() {
    const out = document.getElementById('radagast-history');
    out.innerHTML = `<div style="padding:20px;text-align:center"><i class="fas fa-spinner fa-spin" style="font-size:2rem;color:var(--warning)"></i><p style="margin-top:10px">Executando curadoria...</p></div>`;
    const r = await apiCall('/api/radagast','POST',{days_back:1});
    if (r && r.sucesso) {
        out.innerHTML = `<div style="padding:20px;background:var(--bg-input);border-radius:8px"><strong>${escapeHtml(r.mensagem||'Radagast')}</strong><p style="color:var(--text-muted);margin-top:8px">${escapeHtml(r.instrucao||'')}</p><p style="margin-top:12px">Execute no terminal:</p><code style="display:block;padding:10px;background:var(--bg-dark);border-radius:4px;margin-top:8px">${escapeHtml(r.execucao||'python agents/radagast/radagast.py')}</code></div>`;
    } else {
        out.innerHTML = `❌ ${escapeHtml(r.erro||'Erro')}`;
    }
    showToast('Radagast requer execução via terminal', 'info');
}

async function analyzeCompetitors() {
    const nicho = document.getElementById('posicionamento-nicho').value;
    const conc = document.getElementById('posicionamento-concorrentes').value;
    const out = document.getElementById('posicionamento-output');
    if (!nicho || !conc.trim()) { showToast('Preencha nicho e concorrentes', 'error'); return; }
    out.style.display = 'block';
    out.innerHTML = `📊 Analisando...`;
    const r = await apiCall('/api/posicionamento','POST',{nicho, concorrentes:conc.split('\n').filter(l=>l.trim()).join(' ')});
    out.innerHTML = escapeHtml((r&&r.analise)||(r&&r.mensagem)||conc.split('\n').filter(l=>l.trim()).map((c,i)=>`${i+1}. @${c.trim()}`).join('\n'));
    showToast('Análise concluída!', 'info');
}

async function savePosicionamento() {
    const v = document.getElementById('minha-verdade').value;
    const f = document.getElementById('frase-posicionamento').value;
    if (!v||!f) { showToast('Preencha os campos', 'error'); return; }
    showToast('Posicionamento salvo!', 'success');
}

async function runAlimentarFromModal() {
    const input = document.getElementById('alimentar-input').value;
    if (!input.trim()) { showToast('Cole o conteúdo', 'error'); return; }
    const out = document.getElementById('alimentar-output');
    out.style.display = 'block';
    out.innerHTML = `🧠 Processando...`;
    const r = await apiCall('/api/alimentar','POST',{input:input.slice(0,3000), tipo:document.getElementById('alimentar-tipo').value, titulo:'Perfil Empreendedor'});
    out.innerHTML = r.sucesso ? `✅ ${escapeHtml(r.mensagem)}\n\n${escapeHtml(r.saida||r.arquivo||'')}` : `❌ ${escapeHtml(r.erro||r.mensagem)}`;
    showToast(r.sucesso?'🧠 Cérebro alimentado!':'Erro', r.sucesso?'success':'error');
}


function closeAlimentarModal(e) { if (e && e.target !== e.currentTarget) return; document.getElementById('alimentarModal').classList.remove('active'); }


function loadQuadroAvisos() {
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


function updateGreeting() {
    const h = new Date().getHours();
    let g = 'Boa noite! 🌙';
    if (h >= 5 && h < 12) g = 'Bom dia! ☀️';
    else if (h >= 12 && h < 18) g = 'Boa tarde! 🌤️';
    const el = document.getElementById('dash-greeting');
    if (el) el.textContent = g;
    const d = document.getElementById('dash-date');
    if (d) {
        const now = new Date();
        const dias = ['Domingo','Segunda','Terça','Quarta','Quinta','Sexta','Sábado'];
        const meses = ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'];
        d.textContent = '📅 ' + dias[now.getDay()] + ', ' + now.getDate() + ' de ' + meses[now.getMonth()] + ' de ' + now.getFullYear();
    }
}


function renderHeatmap() {
    const container = document.getElementById('heatmap');
    if (!container) return;
    container.innerHTML = '';
    const today = new Date();
    for (let i = 89; i >= 0; i--) {
        const d = new Date(today);
        d.setDate(d.getDate() - i);
        const day = d.getDay();
        const isWeekend = day === 0 || day === 6;
        const level = isWeekend ? 0 : Math.floor(Math.random() * 5);
        const cell = document.createElement('div');
        cell.className = 'heatmap-cell' + (level > 0 ? ' l' + level : '');
        cell.title = d.toLocaleDateString('pt-BR');
        container.appendChild(cell);
    }
}


function renderStreak() {
    const bar = document.getElementById('streak-bar');
    if (!bar) return;
    bar.innerHTML = '';
    const dias = ['D','S','T','Q','Q','S','S'];
    const today = new Date().getDay();
    const activeDays = [1,2,3,4,5];
    for (let i = 0; i < 7; i++) {
        const d = document.createElement('div');
        d.className = 'streak-day';
        if (activeDays.includes(i)) d.classList.add('active');
        if (i === today) d.classList.add('today');
        d.textContent = dias[i];
        bar.appendChild(d);
    }
}

function togglePerfilModulos() {
    const modulos = document.getElementById('perfil-modulos');
    if (modulos.style.display === 'none' || !modulos.style.display) {
        modulos.style.display = 'block';
        document.querySelectorAll('#perfil-modulos .card').forEach(c => c.style.display = 'block');
    } else {
        modulos.style.display = 'none';
    }
}


