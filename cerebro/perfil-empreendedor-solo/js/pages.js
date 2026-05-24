// ============================================
// PAGES
// ============================================
async function loadPerfilData() {
    try {
        const data = await apiCall('/api/load-profile');
        if (!data || data.error) return;

        if (data.basico) {
            const b = data.basico;
            if (b.nome) document.getElementById('perfil-nome').value = b.nome;
            if (b['nome publico'] || b['nome público']) document.getElementById('perfil-nome-publico').value = b['nome publico'] || b['nome público'];
            if (b.nicho) document.getElementById('perfil-nicho').value = b.nicho;
            if (b['publico alvo'] || b['público-alvo'] || b.público) document.getElementById('perfil-publico').value = b['publico alvo'] || b['público-alvo'] || b.público;
            if (b.problema) document.getElementById('perfil-problema').value = b.problema;
            if (b.descrição || b.descricao) {
                if (!b.problema) document.getElementById('perfil-problema').value = b.descrição || b.descricao;
            }
        }

        if (data.habilidades) {
            const h = data.habilidades;
            if (h.habilidades) document.getElementById('perfil-habilidades').value = h.habilidades;
            if (h.resumo) document.getElementById('perfil-habilidades-resumo').value = h.resumo;
        }

        if (data.historias) {
            const h = data.historias;
            if (h['história profissional'] || h['historia profissional']) document.getElementById('perfil-historia').value = h['história profissional'] || h['historia profissional'];
            if (h.experiências || h.experiencias) document.getElementById('perfil-experiencias').value = h.experiências || h.experiencias;
        }

        if (data.cosmovisao) {
            const c = data.cosmovisao;
            if (c.valores) document.getElementById('perfil-valores').value = c.valores;
            if (c.crenças || c.crencas) document.getElementById('perfil-crencas').value = c.crenças || c.crencas;
        }

        if (data.publico) {
            const p = data.publico;
            if (p['cliente ideal'] || p.cliente) document.getElementById('perfil-cliente').value = p['cliente ideal'] || p.cliente;
            if (p.problemas) document.getElementById('perfil-problemas').value = p.problemas;
        }

        if (data.posicionamento) {
            const p = data.posicionamento;
            if (p.diferencial) document.getElementById('perfil-diferencial').value = p.diferencial;
            if (p['proposta de valor'] || p.proposta) document.getElementById('perfil-proposta').value = p['proposta de valor'] || p.proposta;
            if (p['frase de posicionamento'] || p['frase']) document.getElementById('perfil-frase-posicionamento').value = p['frase de posicionamento'] || p['frase'];
        }

        // Concorrentes
        if (data.concorrentes_secoes) {
            const concEl = document.getElementById('perfil-concorrentes-display');
            if (concEl) {
                let html = '';
                for (const [cat, nomes] of Object.entries(data.concorrentes_secoes)) {
                    const nomesLimpos = nomes.map(n => {
                        let nome = n.replace(/^- \*\*/g, '').replace(/\*\*/g, '');
                        nome = nome.replace(/\(@\S+\)/g, '').trim();
                        return nome;
                    });
                    html += `<div style="margin-bottom:8px"><strong style="font-size:0.8rem;color:var(--accent-light)">${cat}</strong><div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:4px">${nomesLimpos.map(n => `<span class="tag tag-blue" style="font-size:0.75rem">${n}</span>`).join('')}</div></div>`;
                }
                concEl.innerHTML = html;
            }
        } else if (data.concorrentes) {
            const concEl = document.getElementById('perfil-concorrentes-display');
            if (concEl) concEl.innerHTML = `<pre style="white-space:pre-wrap;font-size:0.8rem;margin:0">${escapeHtml(data.concorrentes)}</pre>`;
        }

        // Análise detalhada
        if (data.analise_concorrentes) {
            const analiseEl = document.getElementById('perfil-analise-concorrentes');
            if (analiseEl) analiseEl.innerHTML = `<pre style="white-space:pre-wrap;font-size:0.8rem;margin:0;font-family:'JetBrains Mono',monospace">${escapeHtml(data.analise_concorrentes)}</pre>`;
        }

        if (data.narrativa) {
            const n = data.narrativa;
            if (n.missão || n.missao) document.getElementById('perfil-missao').value = n.missão || n.missao;
            if (n.origem) document.getElementById('perfil-origem').value = n.origem;
        }
        // Carrega identidade visual do localStorage
        if (localStorage.getItem('opb_cor1')) document.getElementById('perfil-cor1').value = localStorage.getItem('opb_cor1');
        if (localStorage.getItem('opb_cor2')) document.getElementById('perfil-cor2').value = localStorage.getItem('opb_cor2');
        if (localStorage.getItem('opb_cor3')) document.getElementById('perfil-cor3').value = localStorage.getItem('opb_cor3');
        if (localStorage.getItem('opb_fonte')) document.getElementById('perfil-fonte-titulo').value = localStorage.getItem('opb_fonte');
        // Atualiza previews
        document.getElementById('preview-c1').style.background = document.getElementById('perfil-cor1').value;
        document.getElementById('preview-c2').style.background = document.getElementById('perfil-cor2').value;
        document.getElementById('preview-c3').style.background = document.getElementById('perfil-cor3').value;
    } catch (e) {
        console.error('Erro ao carregar perfil:', e);
    }
}

async function loadPageData(page) {
    if (page === 'perfil') { await loadPerfilData(); }
    if (page === 'posicionamento') { await loadPosicionamentoPage(); }
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
        await checkAgentsApi();
    }
    if (page === 'cerebro') {
        await loadCerebroTree();
        await loadMapas();
    }
    if (page === 'inspiracoes') loadInspiracoes();
    if (page === 'quadro-avisos') loadQuadroAvisos();
    if (page === 'config') { checkObsidian(); loadNotionConfig(); }
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

async function loadCerebroTree() {
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

// ============================================
// CARROSSEL
// ============================================
async function gerarCarrossel() {
    const tema = document.getElementById('carrossel-ideia').value;
    if (!tema.trim()) { showToast('Descreva sua ideia', 'error'); return; }
    const out = document.getElementById('carrossel-output');
    out.style.display = 'block';
    out.innerHTML = `<i class="fas fa-spinner fa-spin"></i> Gerando carrossel...`;
    const slides = document.getElementById('carrossel-slides').value;
    const tipo = document.getElementById('carrossel-tipo').value;
    const r = await apiCall('/api/carrossel','POST',{tema, tipo, slides:parseInt(slides)});
    if (r.sucesso) {
        const texto = r.saida || r.mensagem || r.stdout || '';
        showResult('carrossel-output', 'carrossel-copy-btn', texto, 'carrossel');
        const saved = JSON.parse(localStorage.getItem('opb_resultados') || '[]');
        saved.unshift({id:Date.now(), texto, tag:'carrossel', data:new Date().toLocaleString('pt-BR')});
        localStorage.setItem('opb_resultados', JSON.stringify(saved.slice(0,50)));
        renderSavedResults();
    } else {
        out.innerHTML = `<div class="empty-state"><i class="fas fa-exclamation-triangle"></i><h3>Erro</h3><p>${escapeHtml(r.erro||r.mensagem||'Tente novamente')}</p></div>`;
    }
    showToast(r.sucesso ? 'Carrossel gerado!' : 'Erro', r.sucesso ? 'success' : 'error');
}

async function runTranscricao() {
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
    out.innerHTML = `<i class="fas fa-spinner fa-spin"></i> Gerando...`;
    const r = await apiCall('/api/capa-video','POST',{tema, quantidade:parseInt(document.getElementById('capa-qtd').value)});
    if (r.sucesso) {
        const texto = r.saida || r.mensagem || '';
        showResult('capa-output', 'capa-copy-btn', texto, 'capa-video');
    } else {
        out.innerHTML = `<div class="empty-state"><i class="fas fa-exclamation-triangle"></i><h3>Erro</h3><p>${escapeHtml(r.erro||r.mensagem||'Tente novamente')}</p></div>`;
    }
    showToast(r.sucesso?'Capas geradas!':'Erro', r.sucesso?'success':'error');
}

async function runConsumo() {
    const input = document.getElementById('consumo-input').value;
    if (!input.trim()) { showToast('Cole um texto ou URL', 'error'); return; }
    const out = document.getElementById('consumo-output');
    out.style.display = 'block';
    const titulo = document.getElementById('consumo-titulo').value || 'Conteúdo';
    out.innerHTML = `<i class="fas fa-spinner fa-spin"></i> Processando...`;
    const r = await apiCall('/api/consumo','POST',{input:input.slice(0,3000), tipo:document.getElementById('consumo-tipo').value, titulo});
    if (r.sucesso) {
        const texto = `${r.mensagem}\n\n${r.saida||''}`;
        showResult('consumo-output', null, texto, 'consumo');
    } else {
        out.innerHTML = `<div class="empty-state"><i class="fas fa-exclamation-triangle"></i><h3>Erro</h3><p>${escapeHtml(r.erro||r.mensagem||'Tente novamente')}</p></div>`;
    }
    showToast(r.sucesso?'Conteúdo processado!':'Erro', r.sucesso?'success':'error');
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

async function loadPosicionamentoPage() {
    try {
        const data = await apiCall('/api/load-profile');
        if (!data || data.error) return;
        // Preenche nicho do perfil
        if (data.basico && data.basico.nicho) {
            document.getElementById('posicionamento-nicho').value = data.basico.nicho;
        }
        // Preenche concorrentes do quem-sou
        if (data.concorrentes_secoes) {
            const concs = [];
            for (const [cat, nomes] of Object.entries(data.concorrentes_secoes)) {
                nomes.forEach(n => {
                    const match = n.match(/@(\S+)/);
                    if (match) concs.push('@' + match[1]);
                });
            }
            if (concs.length) {
                document.getElementById('posicionamento-concorrentes').value = concs.slice(0, 10).join('\n');
            }
        }
        // Preenche frase de posicionamento
        if (data.posicionamento) {
            const p = data.posicionamento;
            if (p['frase de posicionamento'] || p['frase']) {
                document.getElementById('frase-posicionamento').value = p['frase de posicionamento'] || p['frase'];
            }
        }
    } catch (e) {
        console.error('Erro ao carregar dados na página de posicionamento:', e);
    }
}

async function analyzeCompetitors() {
    const nicho = document.getElementById('posicionamento-nicho').value;
    const conc = document.getElementById('posicionamento-concorrentes').value;
    const out = document.getElementById('posicionamento-output');
    if (!nicho || !conc.trim()) { showToast('Preencha nicho e concorrentes', 'error'); return; }
    out.style.display = 'block';
    out.innerHTML = `<i class="fas fa-spinner fa-spin"></i> Analisando...`;
    const r = await apiCall('/api/posicionamento','POST',{nicho, concorrentes:conc.split('\n').filter(l=>l.trim()).join(' ')});
    if (r && r.analise) {
        showResult('posicionamento-output', null, r.analise, 'posicionamento');
    } else {
        out.innerHTML = `<div class="empty-state"><i class="fas fa-exclamation-triangle"></i><h3>Erro</h3><p>${escapeHtml(r.erro||r.mensagem||'Tente novamente')}</p></div>`;
    }
    showToast('Análise concluída!', 'info');
}

async function savePosicionamento() {
    const v = document.getElementById('minha-verdade').value;
    const f = document.getElementById('frase-posicionamento').value;
    if (!v||!f) { showToast('Preencha os campos', 'error'); return; }
    try {
        const content = '## Minha Verdade\n\n' + v + '\n\n## Frase de Posicionamento\n\n' + f;
        const r = await apiCall('/api/save-profile', 'POST', { modulo: 'posicionamento', content, filename: 'POSICIONAMENTO.md' });
        showToast(r.sucesso ? '✅ Posicionamento salvo!' : 'Erro: ' + (r.error || ''), r.sucesso ? 'success' : 'error');
    } catch (e) {
        showToast('Erro: ' + e.message, 'error');
    }
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

async function savePerfil(){
    const n=document.getElementById('perfil-nome').value;
    if(!n){showToast('Preencha seu nome','error');return}
    const cor1 = document.getElementById('perfil-cor1').value;
    const cor2 = document.getElementById('perfil-cor2').value;
    const cor3 = document.getElementById('perfil-cor3').value;
    const fonte = document.getElementById('perfil-fonte-titulo').value;
    localStorage.setItem('opb_cor1', cor1);
    localStorage.setItem('opb_cor2', cor2);
    localStorage.setItem('opb_cor3', cor3);
    localStorage.setItem('opb_fonte', fonte);
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
            content = '## Diferencial\n\n' + (document.getElementById('perfil-diferencial').value || '') + '\n\n## Proposta de Valor\n\n' + (document.getElementById('perfil-proposta').value || '') + '\n\n## Frase de Posicionamento\n\n' + (document.getElementById('perfil-frase-posicionamento').value || '');
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

let pR1 = false, pI1 = null, pS1 = 25 * 60;

function togglePomodoro() {
    pR1 = !pR1;
    const b=document.getElementById('pomodoro-btn');
    if(pR1){b.innerHTML='<i class="fas fa-pause"></i> Pausar';b.className='btn btn-warning btn-lg';pI1=setInterval(()=>{pS1--;updateTimer('pomodoro-timer',pS1);if(pS1<=0){clearInterval(pI1);pS1=25*60;pR1=false;b.innerHTML='<i class="fas fa-play"></i> Iniciar';b.className='btn btn-success btn-lg';showToast('✅ Ciclo completo!','success')}},1000)}
    else{clearInterval(pI1);b.innerHTML='<i class="fas fa-play"></i> Iniciar';b.className='btn btn-success btn-lg'}
}

function resetPomodoro(){clearInterval(pI1);pR1=false;pS1=25*60;updateTimer('pomodoro-timer',pS1);document.getElementById('pomodoro-btn').innerHTML='<i class="fas fa-play"></i> Iniciar';document.getElementById('pomodoro-btn').className='btn btn-success btn-lg'}

function updateTimer(id,s){const m=Math.floor(s/60),ss=s%60;document.getElementById(id).textContent=String(m).padStart(2,'0')+':'+String(ss).padStart(2,'0')}

function updateTaskCount(){const items=document.querySelectorAll('#tasks-list .todo-item'),checked=document.querySelectorAll('#tasks-list input[type="checkbox"]:checked');document.getElementById('tasks-today').textContent=items.length;document.getElementById('pomo-done').textContent=checked.length;document.getElementById('pomo-focus').textContent=checked.length*25}

function addTask(){const l=document.getElementById('tasks-list');if(l.querySelector('.empty-state'))l.innerHTML='';const d=document.createElement('div');d.className='todo-item';d.style.cssText='display:flex;align-items:center;gap:10px;padding:12px;border-radius:8px;margin-bottom:6px;background:var(--bg-input)';d.innerHTML='<input type="checkbox" onchange="updateTaskCount(this)" style="accent-color:var(--accent);width:18px;height:18px"><input type="text" placeholder="Nova tarefa..." style="background:transparent;border:none;color:var(--text-primary);flex:1;font-size:0.9rem" onkeypress="if(event.key===\'Enter\')this.blur()"><button onclick="this.closest(\'.todo-item\').remove();updateTaskCount()" style="background:none;border:none;color:var(--text-muted);cursor:pointer;padding:4px"><i class="fas fa-trash"></i></button>';l.appendChild(d);updateTaskCount()}

// inspData/inspDocs declared in app.js

async function loadInspiracoes() {
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

function closeAlimentarModal(e) { if (e && e.target !== e.currentTarget) return; document.getElementById('alimentarModal').classList.remove('active'); }

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

function buildContextoJson(tipo, input) {
    if (tipo === 'analise_swot') return JSON.stringify({business_name: input});
    if (tipo === 'planejamento_conteudo') return JSON.stringify({timeframe: 'próximo mês', objectives: input});
    if (tipo === 'otimizacao_tempo') return JSON.stringify({challenges: input});
    if (tipo === 'consulta_geral') return JSON.stringify({question: input});
    return JSON.stringify({contexto: input});
}

async function runConsultorNegocios() {
    const tipo = document.getElementById('consultor-tipo').value;
    const input = document.getElementById('consultor-input').value;
    if (!input.trim()) { showToast('Descreva sua situação ou desafio', 'error'); return; }
    const out = document.getElementById('consultor-output');
    out.style.display = 'block';
    out.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Consultando...';
    const r = await apiCall('/api/agentes/executar','POST',{agente:'consultor-negocios',args:[tipo,buildContextoJson(tipo,input)]});
    if (r.sucesso) {
        const texto = r.stdout||r.mensagem||'';
        showResult('consultor-output', 'consultor-copy-btn', texto, 'consultor-negocios');
        const saved = JSON.parse(localStorage.getItem('opb_resultados') || '[]');
        saved.unshift({id:Date.now(), texto, tag:`consulta-${tipo}`, data:new Date().toLocaleString('pt-BR')});
        localStorage.setItem('opb_resultados', JSON.stringify(saved.slice(0,50)));
        renderSavedResults();
    } else {
        out.innerHTML = `<div class="empty-state"><i class="fas fa-exclamation-triangle"></i><h3>Erro na Consulta</h3><p>${escapeHtml(r.erro||r.mensagem||'Tente novamente')}</p></div>`;
    }
    showToast(r.sucesso?'Consultoria concluída!':'Erro na consulta', r.sucesso?'success':'error');
}

function quickConsultoria(tipo, contexto) {
    document.getElementById('consultor-tipo').value = tipo;
    document.getElementById('consultor-input').value = contexto;
    runConsultorNegocios();
}

// ============================================
// JORNADA IA — COMPARTILHAR
// ============================================
function openShareEditor(platform) {
    const titles = {
        linkedin: '📢 LinkedIn',
        twitter: '🐦 Twitter / X',
        instagram: '📸 Instagram / Reels',
        substack: '📧 Substack',
        carrossel: '🎠 Carrossel 5 Slides'
    };
    document.getElementById('shareModalTitle').innerHTML = `<i class="fas fa-pen" style="color:var(--primary);margin-right:8px"></i> Editar — ${titles[platform] || platform}`;

    const texts = {
        linkedin: `🚀 10 dias. 1 pessoa. 15 agentes de IA. 3 negócios. R$ 0 em assinaturas.

Construí um sistema operacional de negócios movido a inteligência artificial — DO ZERO — sozinho, num notebook Acer de 2012 com 8GB de RAM.

E não, não é milagre. É estratégia.

Aqui está o que eu construí em 10 dias:

📌 Dia 1-2: Instalei Python + Ollama (IA local). Criei 3 agentes que transcrevem vídeos, geram carrosséis do Instagram e descrevem designs. Cada resposta levava 3 minutos — mas funcionava.

📌 Dia 3-5: Construí uma plataforma web completa (SPA) onde todos os agentes vivem. Cada um com sua página, seu formulário, seu propósito. Adicionei o Radagast — um curador automático que varre YouTube, Twitter e web todo dia pra me trazer ideias de conteúdo.

📌 Dia 6: Mapeei o mercado. 40+ influenciadores de finanças no Brasil analisados. Descobri o gap: finanças pessoais com perspectiva cristã, sem teologia da prosperidade. Isso virou meu posicionamento.

📌 Dia 7: Implementei multi-perfil — 3 negócios (Paz na Conta, Toque de Paz, Caminho Vida) compartilham a mesma plataforma, cada um com seu cérebro e seus agentes. Adicionei sincronia PC-celular via GitHub.

📌 Dia 8-9: Criei o Consultor de Negócios (análise SWOT, planejamento estratégico), Agente Hashtags, Reels Script, e integração total com Telegram Bot — o sistema inteiro no bolso.

📌 Dia 10: Rodei tudo no celular via Termux. Debug de permissão, line endings, tokens. Cada erro virou lição documentada.

O resultado?
✅ 15+ agentes de IA trabalhando 24h
✅ 3 negócios na mesma plataforma
✅ R$ 0 gasto em assinaturas
✅ PC fraco + celular antigo = suficiente

Essa história prova que você NÃO precisa de:
❌ Grana pra investir em tecnologia cara
❌ Equipe de desenvolvedores
❌ PC poderoso
❌ Conhecimento avançado

Você precisa de:
✅ Um problema real pra resolver
✅ Vontade de aprender
✅ 10 dias de foco

O hardware que você tem é suficiente. O conhecimento se constrói no caminho.

Se eu consegui, você consegue também.

#IA #EmpreendedorismoSolo #OPBStudio #Inovação #FinançasCatólicas #Produtividade`,

        twitter: `🧵 Construí um sistema de agentes de IA do zero em 10 dias — sozinho, num PC de 2012, gastando R$ 0 em assinaturas.

1/10 🚀 O sonho: ter uma equipe de especialistas 24h. A realidade: um notebook Acer 2012 com 8GB RAM.

Dia 1: Instalei Python + Ollama (IA local). Criei 3 agentes que transcrevem, geram carrosséis e descrevem designs. Lentos, mas funcionais. 🐢

2/10 Dia 2: Construí a plataforma web. Cada agente ganhou página própria com formulário e resultado. Adicionei PWA mobile e alimentação automática do cérebro.

3/10 Dias 3-5: Layout profissional com gradientes + modo escuro + Landing Page. Nasceu o Radagast — curador que varre YouTube/Twitter/web todo dia e gera ideias de Reels com IA.

4/10 Dia 6: Mapeei o mercado. 40+ influenciadores. Descobri o gap: finanças com fé, sem teologia da prosperidade.

5/10 Dia 7: Multi-perfil — 3 negócios na mesma plataforma. Dashboard PWA. Sincronia PC-celular. Autenticação. Agentes corta-silêncio e transcrever-áudio.

6/10 Dias 8-9: Consultor de Negócios (SWOT, estratégia). Hashtags IA. Reels Script. Telegram Bot comandando tudo.

7/10 Dia 10: TUDO RODANDO NO CELULAR via Termux. Debug de permissão, CRLF, tokens. Cada erro documentado como lição.

8/10 Resultado: 15+ agentes, 3 negócios, R$ 0, PC de 2012 + celular antigo.

9/10 Lição: Hardware não é desculpa. Conhecimento se constrói no caminho. O problema real + foco > qualquer recurso.

10/10 Se eu consegui, você consegue. Comece hoje.

#IA #Empreendedorismo #Inovação #OPBStudio #TinyLLM`,

        instagram: `🚀 10 DIAS. 1 PESSOA. 15 AGENTES DE IA.

Construí um SISTEMA OPERACIONAL DE NEGÓCIOS inteiro movido a inteligência artificial.

Sozinho.
Num notebook de 2012.
Gastando R$ 0 em assinaturas.

O que esse sistema faz:
📹 Transcreve vídeos automaticamente
🎠 Gera carrosséis para Instagram
✍️ Cria roteiros para Reels
📡 Curadoria diária de conteúdo
🏛️ Consultoria estratégica (SWOT, KPIs)
🔍 Análise de concorrência
📊 Planejamento de conteúdo
🎬 Roteiro para vídeos
🤖 E muito mais...

Tudo roda LOCALMENTE — sem enviar seus dados pra ninguém.

E o melhor: você controla TUDO pelo Telegram no celular.

O hardware que você tem é SUFICIENTE.
O conhecimento se constrói no caminho.
O melhor momento pra começar foi ontem. O segundo melhor é AGORA.

#IA #EmpreendedorismoSolo #OPBStudio #Inovação #Produtividade #FinançasCatólicas`,

        substack: `# Como construí um sistema de agentes de IA do zero em 10 dias (sozinho, num PC de 2012, gastando R$ 0)

---

**TL;DR:** Instalei Python, baixei um modelo de IA gratuito (Ollama + tinyllama), e em 10 dias construí um sistema com 15+ agentes que gerenciam 3 negócios — tudo rodando local, sem assinatura, num notebook Acer de 2012.

---

## Por que isso importa?

Vivemos a era do "empreendedor solo aumentado". Pela primeira vez na história, uma única pessoa pode ter uma equipe inteira de especialistas trabalhando 24h por dia, 7 dias por semana, por centavos de energia elétrica.

Eu resolvi testar esse limite na prática.

## O experimento

**Setup:** Notebook Acer Aspire E1-571, Intel Core i5-2400, 8GB RAM, Intel HD Graphics 3000. Sem GPU. Sem internet dedicada. Hardware que qualquer pessoa tem guardado numa gaveta.

**Modelo de IA:** Tinyllama (637MB) via Ollama — IA local, gratuita, que roda sem internet. Vazão: ~2 tokens/segundo. É lento, mas funciona.

**O que foi construído em 10 dias:**

| Dia | O que aconteceu |
|-----|----------------|
| 1 | Primeiros agentes (transcrição, carrossel, designer) + Ollama local |
| 2 | Plataforma web SPA com PWA mobile + Agentes Consumo e Capa Vídeo |
| 3-5 | Layout profissional, modo escuro, Landing Page, Radagast (curador diário) |
| 6 | Pesquisa de mercado (40+ concorrentes), definição de nicho e posicionamento |
| 7 | Multi-perfil (3 negócios), sincronia PC-celular, autenticação, dashboard PWA |
| 8-9 | Consultor de Negócios, Hashtags IA, Reels Script, integração Telegram total |
| 10 | Deploy no celular via Termux, debug de Android, lições documentadas |

## O resultado

✅ **15+ agentes de IA** trabalhando em paralelo
✅ **3 negócios** na mesma plataforma (cada um com seu cérebro)
✅ **R$ 0** gasto em assinaturas de SaaS
✅ **PC fraco + celular antigo** = infraestrutura suficiente
✅ **89 commits** no GitHub em 10 dias

## A lição mais importante

O hardware que você tem é suficiente. O conhecimento se constrói no caminho. O que realmente importa é:

1. **Um problema real** — sem isso, nenhuma tecnologia resolve nada
2. **Vontade de aprender** — você vai errar muito. Anote cada erro.
3. **Foco** — 10 dias dedicados valem mais que 6 meses de "vou fazer quando der"

Se eu consegui com um notebook de 2012, você consegue também.

—

*Este artigo faz parte da série "Jornada IA" — documentando em tempo real a construção de um sistema operacional de negócios movido a inteligência artificial.*

[Assine a newsletter](#) para receber as atualizações semanais.`,

        carrossel: `Slide 1 — CAPA
🚀 10 DIAS. 1 PESSOA. 15 AGENTES DE IA.
Construí um sistema operacional de negócios movido a IA — do zero, num PC de 2012, gastando R$ 0.
(Imagem: você no centro, ícones de IA girando ao redor)

Slide 2 — O PROBLEMA
😰 Ser empreendedor solo é fazer tudo sozinho:
📹 Conteúdo
✍️ Roteiros
📊 Estratégia
📡 Curadoria
📈 Análises
🤝 Gestão
E se você pudesse ter uma equipe de especialistas trabalhando 24h por dia?
(Imagem: pessoa sobrecarregada vs pessoa com robôs ajudando)

Slide 3 — A SOLUÇÃO
🤖 Conheça os agentes OPB:
📹 Transcrição de vídeos → automático
🎠 Carrossel Instagram → 1 clique
📡 Radagast → curadoria diária
🏛️ Consultor → análise SWOT + estratégia
✍️ Text Generator → posts prontos
🔍 Consumo → livros resumidos por IA
📊 Posicionamento → diferencial competitivo
(Imagem: grid de ícones com cada agente)

Slide 4 — O DIFERENCIAL
💡 Tudo roda LOCALMENTE:
✅ Sem internet necessária
✅ Sem enviar seus dados
✅ Sem assinatura mensal
✅ PC fraco serve (8GB RAM)
✅ Celular também roda
Hardware não é desculpa. Conhecimento se constrói no caminho.
(Imagem: notebook + celular com check verde)

Slide 5 — CTA
👇 Pronto pra começar sua jornada IA?
O melhor momento foi ontem.
O segundo melhor é AGORA.
Comente "EU VOU" ou compartilhe com quem precisa ler isso.
🚀 #IA #EmpreendedorismoSolo #OPBStudio #Inovação #Produtividade
(Imagem: fundo inspirador com texto "COMECE HOJE")
`
    };

    const editor = document.getElementById('shareEditor');
    editor.value = texts[platform] || '';
    updateCharCount();
    document.getElementById('shareModal').classList.add('active');
}

function closeShareModal(e) {
    if (e && e.target !== e.currentTarget) return;
    document.getElementById('shareModal').classList.remove('active');
}

function copyShareText() {
    const text = document.getElementById('shareEditor').value;
    navigator.clipboard.writeText(text);
    showToast('✅ Texto copiado!', 'success');
}

document.addEventListener('input', function(e) {
    if (e.target && e.target.id === 'shareEditor') updateCharCount();
});

function updateCharCount() {
    const text = document.getElementById('shareEditor').value;
    const count = text.length;
    document.getElementById('shareCharCount').textContent = `${count} caracteres`;
}

// ============================================
// COMPONENTE: Resultado + Compartilhar
// ============================================
function showResult(outputId, copyBtnId, text, extraShareText) {
    const out = document.getElementById(outputId);
    const copyBtn = document.getElementById(copyBtnId);
    out.style.display = 'block';
    if (copyBtn) copyBtn.style.display = 'inline-flex';
    const safe = escapeHtml(text);
    out.innerHTML = `
<textarea class="result-editor" id="${outputId}-editor" rows="8" style="width:100%;padding:12px;border:2px solid var(--border);border-radius:8px;font-family:'Inter',sans-serif;font-size:0.9rem;line-height:1.6;resize:vertical;background:var(--bg-card);color:var(--text)">${safe}</textarea>
<div class="result-actions" style="display:flex;gap:8px;flex-wrap:wrap;margin-top:10px">
    <button class="btn btn-sm" style="background:var(--primary);color:white;border:none" onclick="copyResult('${outputId}-editor')"><i class="fas fa-copy"></i> Copiar</button>
    <button class="btn btn-sm" style="background:#0A66C2;color:white;border:none" onclick="shareResult('${outputId}-editor','linkedin','${escapeHtml(extraShareText||'')}')"><i class="fab fa-linkedin"></i> LinkedIn</button>
    <button class="btn btn-sm" style="background:#1DA1F2;color:white;border:none" onclick="shareResult('${outputId}-editor','twitter','${escapeHtml(extraShareText||'')}')"><i class="fab fa-x-twitter"></i> Twitter/X</button>
    <button class="btn btn-sm" style="background:linear-gradient(135deg,#F58529,#DD2A7B);color:white;border:none" onclick="shareResult('${outputId}-editor','instagram','${escapeHtml(extraShareText||'')}')"><i class="fab fa-instagram"></i> Instagram</button>
    <button class="btn btn-sm btn-outline" onclick="saveResult('${outputId}-editor','${escapeHtml(extraShareText||'')}')"><i class="fas fa-save"></i> Salvar</button>
</div>`;
}

function copyResult(editorId) {
    const text = document.getElementById(editorId).value;
    navigator.clipboard.writeText(text);
    showToast('Texto copiado!', 'success');
}

function shareResult(editorId, platform, extra) {
    const text = document.getElementById(editorId).value;
    const encoded = encodeURIComponent(text.substring(0,280) + (text.length>280?'...':''));
    const urls = {
        linkedin: `https://www.linkedin.com/sharing/share-offsite/?url=&text=${encoded}`,
        twitter: `https://twitter.com/intent/tweet?text=${encoded}`,
        instagram: null
    };
    if (platform === 'instagram') {
        navigator.clipboard.writeText(text);
        showToast('Texto copiado! Cole no Instagram.', 'info');
    } else if (urls[platform]) {
        window.open(urls[platform], '_blank', 'width=600,height=400');
    }
}

function saveResult(editorId, tag) {
    const text = document.getElementById(editorId).value;
    if (!text.trim()) { showToast('Nada pra salvar', 'error'); return; }
    const saved = JSON.parse(localStorage.getItem('opb_resultados') || '[]');
    saved.unshift({
        id: Date.now(),
        texto: text,
        tag: tag || 'geral',
        data: new Date().toLocaleString('pt-BR')
    });
    localStorage.setItem('opb_resultados', JSON.stringify(saved.slice(0,50)));
    showToast('Salvo! Consulte em "Meus Resultados"', 'success');
    renderSavedResults();
}

function renderSavedResults() {
    const containers = document.querySelectorAll('.saved-results');
    const container = Array.from(containers).find(el => el.closest('.page')?.style.display !== 'none') || containers[0];
    if (!container) return;
    const saved = JSON.parse(localStorage.getItem('opb_resultados') || '[]');
    if (saved.length === 0) {
        container.innerHTML = '<div class="empty-state"><i class="fas fa-inbox"></i><h3>Nenhum resultado salvo</h3></div>';
        return;
    }
    container.innerHTML = saved.map((r,i) => `
<div class="saved-item" style="padding:12px;background:var(--bg-overlay);border-radius:8px;margin-bottom:8px;border-left:3px solid var(--primary)">
    <div style="font-size:0.75rem;color:var(--text-muted);margin-bottom:4px">${r.data} ${r.tag ? '— '+r.tag : ''}</div>
    <div style="font-size:0.85rem;white-space:pre-wrap;max-height:80px;overflow:hidden;cursor:pointer" onclick="expandSaved(this,${i})">${escapeHtml(r.texto.substring(0,200))}${r.texto.length>200?'...':''}</div>
    <div style="display:flex;gap:6px;margin-top:6px">
        <button class="btn btn-sm btn-outline" onclick="copySaved(${i})" style="font-size:0.75rem"><i class="fas fa-copy"></i></button>
        <button class="btn btn-sm btn-outline" onclick="deleteSaved(${i})" style="font-size:0.75rem;color:var(--danger)"><i class="fas fa-trash"></i></button>
    </div>
</div>`).join('');
}

function expandSaved(el) {
    const full = JSON.parse(localStorage.getItem('opb_resultados') || '[]');
    const idx = parseInt(el.getAttribute('onclick').match(/\d+/)[0]);
    if (el.style.maxHeight === 'none') {
        el.style.maxHeight = '80px';
    } else {
        el.style.maxHeight = 'none';
        el.textContent = full[idx].texto;
    }
}

function copySaved(idx) {
    const saved = JSON.parse(localStorage.getItem('opb_resultados') || '[]');
    navigator.clipboard.writeText(saved[idx].texto);
    showToast('Copiado!', 'success');
}

function deleteSaved(idx) {
    const saved = JSON.parse(localStorage.getItem('opb_resultados') || '[]');
    saved.splice(idx, 1);
    localStorage.setItem('opb_resultados', JSON.stringify(saved));
    renderSavedResults();
    showToast('Removido', 'info');
}

function startRoutine(tipo) {
    const prefix = tipo === 'morning' ? 'mr' : 'nr';
    const items = [];
    for (let i = 1; i <= 5; i++) {
        const cb = document.getElementById(prefix + i);
        if (cb) items.push(cb);
    }
    if (!items.length) { showToast('Rotina não encontrada', 'error'); return; }
    let idx = 0;
    const checkNext = () => {
        if (idx >= items.length) {
            showToast('Rotina concluída! 🎉', 'success');
            return;
        }
        items[idx].checked = true;
        showToast(`Passo ${idx+1}/${items.length} concluído`, 'info');
        idx++;
        if (idx < items.length) {
            setTimeout(checkNext, 2000);
        } else {
            setTimeout(() => showToast('Rotina concluída! 🎉', 'success'), 500);
        }
    };
    checkNext();
}

function quickIdeia(texto) {
    document.getElementById('carrossel-ideia').value = texto;
    gerarCarrossel();
}

function quickPost(obj, tipo) {
    document.getElementById('text-gen-objetivo').value = obj;
    document.getElementById('text-gen-tipo').value = tipo;
    runTextGenerator();
}

function showAlimentarModal() {
    const modal = document.getElementById('alimentarModal');
    if (modal) modal.classList.add('active');
}

function loadCarrosseis() {
    const container = document.getElementById('carrossel-lista');
    if (!container) return;
    apiCall('/api/carrossel/lista').then(r => {
        if (!r || !r.carrosseis || !r.carrosseis.length) {
            container.innerHTML = '<div class="empty-state"><i class="fas fa-layer-group"></i><h3>Nenhum carrossel gerado</h3></div>';
            return;
        }
        container.innerHTML = r.carrosseis.map(c => `
        <div style="padding:12px;background:var(--bg-overlay);border-radius:8px;margin-bottom:8px;border-left:3px solid var(--primary)">
            <div style="font-size:0.85rem;white-space:pre-wrap;max-height:80px;overflow:hidden">${escapeHtml(c.tema)}</div>
            <div style="font-size:0.75rem;color:var(--text-muted);margin-top:4px">${c.data || ''}</div>
        </div>`).join('');
        const count = document.getElementById('carrossel-count');
        if (count) count.textContent = r.carrosseis.length;
    }).catch(() => {});
}

function loadKnowledge() {
    const container = document.getElementById('conhecimento-lista');
    if (!container) return;
    apiCall('/api/conhecimento').then(r => {
        if (!r || !r.conhecimentos || !r.conhecimentos.length) {
            container.innerHTML = '<div class="empty-state"><i class="fas fa-book-open"></i><h3>Nenhum conhecimento salvo</h3></div>';
            return;
        }
        container.innerHTML = r.conhecimentos.map(c => `
        <div style="padding:10px;background:var(--bg-overlay);border-radius:8px;margin-bottom:6px;border-left:3px solid var(--success)">
            <div style="font-size:0.85rem">${escapeHtml(c.titulo || c.nome || '')}</div>
            <div style="font-size:0.75rem;color:var(--text-muted)">${c.data || ''}</div>
        </div>`).join('');
    }).catch(() => {});
}

function saveNotes() {
    const text = document.getElementById('daily-notes').value;
    if (!text.trim()) { showToast('Nada para salvar', 'error'); return; }
    localStorage.setItem('opb_daily_notes', text);
    showToast('Notas salvas!', 'success');
}

function loadNotes() {
    const el = document.getElementById('daily-notes');
    if (!el) return;
    const saved = localStorage.getItem('opb_daily_notes');
    if (saved) el.value = saved;
}

// ============================================
// OBSIDIAN
// ============================================
async function checkObsidian() {
    const el = document.getElementById('obsidian-status');
    if (!el) return;
    try {
        const r = await apiCall('/api/obsidian/status');
        if (r.instalado) {
            el.innerHTML = '<span class="status-dot" style="background:var(--success)"></span><span style="color:var(--success)">Obsidian instalado</span>';
        } else {
            el.innerHTML = '<span class="status-dot" style="background:gray"></span><span>Obsidian não encontrado</span>';
        }
    } catch {
        el.innerHTML = '<span class="status-dot" style="background:gray"></span><span>Servidor offline</span>';
    }
}

async function openObsidian(comando) {
    showToast('Abrindo no Obsidian...', 'info');
    try {
        const r = await apiCall('/api/obsidian/abrir', 'POST', { comando });
        showToast(r.sucesso ? '✅ Aberto no Obsidian!' : '❌ Obsidian não encontrado', r.sucesso ? 'success' : 'error');
    } catch (e) {
        showToast('Erro: ' + e.message, 'error');
    }
}

// ============================================
// NOTION
// ============================================
async function saveNotionConfig() {
    const token = document.getElementById('notion-token').value;
    const db = document.getElementById('notion-database-id').value;
    if (!token.trim()) { showToast('Informe o token do Notion', 'error'); return; }
    try {
        const r = await apiCall('/api/notion/config', 'POST', { token, database_id: db });
        showToast(r.sucesso ? '✅ Configuração salva!' : 'Erro', r.sucesso ? 'success' : 'error');
        document.getElementById('notion-status').textContent = r.sucesso ? '✅ Configurado' : '';
    } catch (e) {
        showToast('Erro: ' + e.message, 'error');
    }
}

async function loadNotionConfig() {
    try {
        const r = await apiCall('/api/notion/config');
        if (r.token) {
            document.getElementById('notion-token').value = r.token;
            document.getElementById('notion-database-id').value = r.database_id || '';
            document.getElementById('notion-status').textContent = '✅ Configurado';
        }
    } catch {}
}

async function syncToNotion(tipo) {
    const titulo = prompt('Título para o Notion:', tipo === 'ideia' ? 'Nova Ideia' : 'Resultado OPB');
    if (!titulo) return;
    const conteudo = prompt('Conteúdo para enviar ao Notion:');
    if (!conteudo) return;
    try {
        const r = await apiCall('/api/notion/sync', 'POST', { titulo, conteudo, tipo });
        if (r.sucesso) {
            showToast('✅ ' + r.mensagem, 'success');
        } else {
            showToast('❌ ' + (r.error || 'Erro'), 'error');
        }
    } catch (e) {
        showToast('Erro: ' + e.message, 'error');
    }
}

// ============================================
// INICIALIZAÇÃO
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    renderSavedResults();
    loadNotes();
    checkObsidian();
    loadNotionConfig();
});

// ============================================
// APRENDIZADOS VIBE CODING
// ============================================
async function loadAprendizadosDoc() {
    const out = document.getElementById('aprendizados-doc');
    if (!out) return;
    out.style.display = 'block';
    out.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Carregando documento...';
    const r = await apiCall('/api/arquivo/ler', 'POST', { caminho: 'acervo/conhecimento/aprendizados-vibe-coding.md' });
    if (r && r.sucesso) {
        out.innerHTML = '<pre style="white-space:pre-wrap;font-size:0.82rem;line-height:1.6;margin:0">' + escapeHtml(r.conteudo) + '</pre>';
        showToast('Documento carregado!', 'success');
    } else {
        out.innerHTML = '<div class="empty-state"><i class="fas fa-exclamation-triangle"></i><h3>Arquivo nao encontrado</h3><p>Execute a geracao do documento primeiro ou acesse pelo navegador de arquivos.</p></div>';
    }
}

// ============================================
// TEXT GENERATOR
// ============================================
async function runTextGenerator() {
    const obj = document.getElementById('text-gen-objetivo').value;
    if (!obj.trim()) { showToast('Informe o objetivo', 'error'); return; }
    const out = document.getElementById('text-gen-output');
    const copyBtn = document.getElementById('textgen-copy-btn');
    out.style.display = 'block';
    copyBtn.style.display = 'none';
    out.innerHTML = `<i class="fas fa-spinner fa-spin"></i> Gerando...`;
    const tipo = document.getElementById('text-gen-tipo').value;
    const r = await apiCall('/api/text-generator','POST',{objetivo:obj, tipo});
    if (r.sucesso) {
        const texto = r.saida || r.mensagem || r.stdout || '';
        showResult('text-gen-output', 'textgen-copy-btn', texto, 'text-generator');
        // Salva auto
        const saved = JSON.parse(localStorage.getItem('opb_resultados') || '[]');
        saved.unshift({id:Date.now(), texto, tag:`texto-${tipo}`, data:new Date().toLocaleString('pt-BR')});
        localStorage.setItem('opb_resultados', JSON.stringify(saved.slice(0,50)));
        renderSavedResults();
    } else {
        out.innerHTML = `<div class="empty-state"><i class="fas fa-exclamation-triangle"></i><h3>Erro</h3><p>${escapeHtml(r.erro||r.mensagem||'Tente novamente')}</p></div>`;
    }
    showToast(r.sucesso ? 'Post gerado!' : 'Erro', r.sucesso ? 'success' : 'error');
}

// ============================================
// POST TEMPLATES para compartilhar
// ============================================
const POST_TEMPLATES = {
    linkedin: `Construi 20+ agentes de IA do zero em 10 dias.

Sozinho.
Num notebook de 2012 com 8GB de RAM.
Gastando R$ 0 em assinaturas.

Nao, isso nao e curso. E o que o "vibe coding" torna possivel.

O que eu construi:
- Um sistema que transcreve videos automaticamente
- Agentes que geram posts, carrosseis, roteiros
- Curadoria diaria de conteudo (sem APIs pagas)
- Consultoria estrategica com IA
- Tudo controlavel pelo Telegram no celular
- Tudo rodando local, sem enviar dados pra ninguem

A stack: Python + Ollama (tinyllama) + Flask + PWA + GitHub
O hardware: Notebook Acer 2012, 8GB RAM, sem placa de video
O custo: R$ 0 de assinatura mensal

Vivemos a era do "empreendedor solo aumentado". Pela primeira vez na historia, uma pessoa so pode ter uma equipe de especialistas trabalhando 24h por centavos de energia eletrica.

O hardware que voce tem e suficiente. O conhecimento se constroi no caminho.

Se eu consegui com um PC de 2012, voce consegue tambem.

#VibeCoding #IA #EmpreendedorismoSolo #Inovacao #IALocal #Solopreneur`,

    instagram: `🚀 10 DIAS. 1 PESSOA. 20+ AGENTES DE IA.

Construi um SISTEMA OPERACIONAL DE NEGOCIOS inteiro movido a inteligencia artificial.

Sozinho.
Num notebook de 2012.
Gastando R$ 0 em assinaturas.

O que esse sistema faz:
- Transcreve videos
- Gera carrosseis para Instagram
- Cria roteiros para Reels
- Curadoria diaria de conteudo
- Consultoria estrategica
- Analise de concorrencia
- Tudo pelo Telegram no celular

Tudo roda LOCALMENTE sem enviar seus dados.
Tudo de GRACA sem assinatura mensal.
Tudo num PC VELHO 8GB de RAM bastam.

O hardware que voce tem e SUFICIENTE.
O conhecimento se constroi no caminho.

Comenta "EU VOU" se voce quer entender como.

#IA #EmpreendedorismoSolo #VibeCoding #Inovacao #Tecnologia`,

    twitter: `Construi 20+ agentes de IA num PC de 2012 com 8GB RAM gastando R$ 0.

Nao precisa de GPU. Ollama + tinyllama (637MB) rodam em CPU.

Stack: Python + Flask + Ollama + HTML/CSS/JS puro. Zero assinaturas.

20+ agentes: transcricao, carrossel, posts, curadoria, consultoria, video, audio.

PWA instalavel no celular. Telegram Bot como controle.

O "vibe coding" e a maior superpotencia do empreendedor solo hoje.

PC fraco e suficiente. O conhecimento se constroi no caminho.

Se eu consegui com um notebook de 2012, voce consegue tambem.

#VibeCoding #IA #Solopreneur #Python #LLM`,

    substack: `# Como construi 20+ agentes de IA do zero em 10 dias (sozinho, num PC de 2012, gastando R$ 0)

## A historia de como o "vibe coding" transformou um notebook velho num sistema operacional de negocios movido a IA.

Faz dez dias, eu tinha uma duvida: "Sera que eu consigo fazer um robo que me ajuda a criar conteudo?"

Hoje, eu tenho 20+ agentes de IA trabalhando 24h por dia.

Tudo rodando num notebook Acer de 2012 com 8GB de RAM.
Tudo de graca, sem assinatura mensal.
Tudo controlavel pelo Telegram no celular.

## A stack (tudo gratuito)
- IA Local: Ollama + Tinyllama (637MB, roda em CPU)
- Backend: Python + Flask (20+ endpoints)
- Frontend: HTML/CSS/JS puro + PWA
- Interface movel: Telegram Bot
- Infra: PC local + GitHub + Vercel (gratis)

## O hardware
Notebook Acer Aspire E1-571 (2012): Intel Core i5, 8GB RAM, sem placa de video, SSD 240GB.

## Quanto custa
R$ 0 de assinatura mensal.

Economia total vs ferramentas pagas: ~R$ 4.000/mes.

## 10 licoes
1. IA local funciona — 8GB RAM + modelo 637MB dao conta
2. Agentes sao como funcionarios — cada um com sua especialidade
3. Mobile-first nao e opcional — 70% usam so celular
4. Documente tudo — cada erro vira regra
5. Nicho e tudo — IA sem nicho e brinquedo
6. Comece pelo problema — tecnologia e meio
7. Vibe coding e superpotencia — 3 meses viram 3 dias
8. PC fraco e suficiente — hardware nunca foi desculpa
9. Contexto e rei — mais dados = melhores respostas
10. Gratuito e viavel — voce nao precisa de dinheiro, precisa de foco

O melhor momento para comecar foi ontem. O segundo melhor e AGORA.`,

    carrossel: `Slide 1 - CAPA
10 DIAS. 1 PESSOA. 20+ AGENTES DE IA.
Construi um sistema operacional de negocios movido a IA - do zero, num PC de 2012, gastando R$ 0.

Slide 2 - O PROBLEMA
Ser empreendedor solo e fazer tudo sozinho: conteudo, roteiros, estrategia, curadoria, analises, gestao.
E se voce pudesse ter uma equipe de especialistas trabalhando 24h por dia?

Slide 3 - A SOLUCAO (STACK)
A stack que roda tudo:
- Ollama + Tinyllama (IA local, 637MB, CPU)
- Python + Flask (20+ endpoints API)
- HTML/CSS/JS puro + PWA (instalavel no celular)
- Telegram Bot (controle pelo celular)
Tudo rodando localmente, sem internet, sem assinatura.

Slide 4 - O DIFERENCIAL
Tudo isso num NOTEBOOK ACER 2012:
- Intel Core i5, 8GB RAM, sem placa de video
- R$ 0 em assinaturas de SaaS
- 20+ agentes trabalhando 24h
- 3 negocios na mesma plataforma
Hardware nao e desculpa. Conhecimento se constroi no caminho.

Slide 5 - CTA
Pronto para comecar sua jornada?
O melhor momento foi ontem. O segundo melhor e AGORA.
Comente "VIBE" ou compartilhe com quem precisa ler isso.`
};

function loadPostTemplate(platform) {
    const text = POST_TEMPLATES[platform];
    if (!text) { showToast('Template nao encontrado', 'error'); return; }
    const editor = document.getElementById('shareEditor');
    if (editor) {
        editor.value = text;
        updateCharCount();
        document.getElementById('shareModal').classList.add('active');
        document.getElementById('shareModalTitle').innerHTML = '<i class="fas fa-pen" style="color:var(--primary);margin-right:8px"></i> Editar - ' + platform.charAt(0).toUpperCase() + platform.slice(1);
    } else {
        navigator.clipboard.writeText(text);
        showToast('Texto copiado!', 'success');
    }
}
