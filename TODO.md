# TODO.md - OPB Sistema

> Quadro de tarefas atualizado em 2026-05-19

## ✅ Concluído

### 23/05/2026 — Concorrentes + Obsidian + Notion + Radagast
- [x] Perfil > Posicionamento: tabela de concorrentes carregada automaticamente do `quem-sou.md` (5 seções de concorrentes)
- [x] Análise detalhada de concorrentes visível ao expandir no perfil
- [x] Página Posicionamento pré-preenchida com nicho e concorrentes do perfil
- [x] Frase de Posicionamento adicionada ao formulário de perfil
- [x] Obsidian: UI integrada na tela de Config (botões para abrir cérebro, quem-sou, projetos, etc.)
- [x] Obsidian: endpoint `/api/obsidian/abrir` + `/api/obsidian/status`
- [x] Notion: utilitário `utils/notion_integration.py` com fallback local
- [x] Notion: UI na Config + endpoints `/api/notion/config` e `/api/notion/sync`
- [x] Radagast: ideias salvas em `acervo/ideias/radagast_*.md`

### Infraestrutura
- [x] Servidor Flask API (`api_server.py`) - 18 endpoints REST
- [x] Telegram Bot integrado (NegreirosBot @NegreirosBot)
- [x] Ollama com tinyllama configurado (modelo padrão)
- [x] Deploy no Vercel (frontend estático): https://opb-sistema.vercel.app

### PWA Mobile
- [x] manifest.json com icons, shortcuts, orientação portrait
- [x] Service Worker (`sw.js`) para offline
- [x] Meta tags para Apple/Android
- [x] Plataforma responsiva (mobile-first) com sidebar navegável

### Setup
- [x] setup.bat + iniciar.bat + requirements.txt + INSTALL.md
- [x] iniciar-dia.bat (inicia API + Telegram Bot em 6 passos)

### Agentes
- [x] Agente Carrossel - 4 tipos com fallback textual (sem LLM) + botão copiar
- [x] Agente Consumo - 5 tipos de análise
- [x] Agente Text Generator - Geração de posts
- [x] Agente Transcrição - YouTube via yt-dlp
- [x] Agente Capa Vídeo - Ideias de thumbnail
- [x] Agente Posicionamento - Pesquisa de mercado
- [x] Agente Narvi - Editor de vídeo (FFmpeg)
- [x] Agente Radagast - Curadoria (reescrito: yt-dlp + RSS, sem Apify/Claude)

### Frontend (plataforma.html)
- [x] Dashboard com cards agentes e quick actions
- [x] Páginas: Cérebro, Rotinas, Transcrição, Capa Vídeo, Carrossel, Consumo, Text Generator, Posicionamento, Narvi, Radagast
- [x] Transcrição formatada com visualização bonita + botão copiar
- [x] Botões copiar em todos outputs de IA (Carrossel, Capa Vídeo, Text Generator, Transcrição)
- [x] Navegador de Arquivos completo (listar diretórios + ler arquivos)
- [x] Template de Perfil (HABILIDADES, HISTORIAS, COSMOVISAO, PUBLICO-ALVO, POSICIONAMENTO, NARRATIVA)

### Perfil Unificado
- [x] `utils/profile_loader.py` - Leitor central de `quem-sou.md` para todos os agentes

### Correções e Estabilização
- [x] phi3:mini → tinyllama (phi3 estava corrompido, tinyllama é mais leve/estável)
- [x] Cache Python limpo diversas vezes
- [x] Bug `/api/arquivos` corrigido (pai crashava na raiz do projeto)
- [x] 303 itens coletados no Radagast --dry-run

## 🔄 Em Progresso

- [ ] Preencher perfil do empreendedor com conteúdo real (parcial: dados básicos + posicionamento ok)
- [ ] Pesquisar solução para acessar iniciar-dia.bat remotamente (SSH ou /api/start no Termux)
- [ ] Testar Radagast salvando ideias em disco
- [ ] Configurar Notion token para sincronia automática
- [ ] Adicionar `showResult()` nos demais agentes (Consumo, Narvi, Radagast)

## 🔧 Notas Técnicas
- Modelo padrão: **tinyllama** (~637MB, funciona com ~3.4GB RAM)
- phi3:mini (~2.2GB) não está mais em uso (corrompido/lento)
- Ollama timeout: 180s
- RAM disponível: ~3.4GB
- Scoop instalado: `scoop install ffmpeg` para Narvi

### Correções Realizadas (19/05/2026)
- api_server.py: corrigido bug no endpoint `/api/arquivos` (ValueError com `relative_to` para diretório raiz)
- plataforma.html: outputs de IA agora usam `<pre>` formatado
- plataforma.html: botões copiar unificados em `copyOutput(id)`
- plataforma.html: página de navegação de arquivos adicionada
- TODO.md + AGENTS.md + DOC-API.md atualizados

## 📋 Próximos Passos

1. **Pós-deploy:** Atualizar toda documentação (AGENTS.md, TODO.md, DOC-API.md) com estado atual
2. **Em outro computador:**
   ```bash
   git clone https://github.com/cleiton-negreiros/opb-sistema.git
   cd opb-sistema
   setup.bat
   iniciar-dia.bat
   ```
3. **Usar no celular:**
   - Acesse https://opb-sistema.vercel.app
   - iOS: Compartilhar > "Adicionar à Tela de Início"
   - Android: Menu > "Instalar App"

## 🚧 Blocked
- (none)

---

## 🔗 Links Úteis

- **Vercel:** https://opb-sistema.vercel.app
- **GitHub:** https://github.com/cleiton-negreiros/opb-sistema
- **API + Frontend Local:** http://localhost:5000 (rode `python api_server.py`)

## 🚀 Como Usar

```bash
# Único terminal (recomendado):
python api_server.py
# Acesse: http://localhost:5000
```

Ou use `iniciar-dia.bat` para iniciar tudo (API + Telegram Bot).