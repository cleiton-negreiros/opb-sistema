# TODO.md - OPB Sistema

> Quadro de tarefas atualizado em 2026-05-13

## ✅ Concluído

- [x] Agente Carrossel (`agents/carrossel/`) — 4 tipos, integrado ao cérebro
- [x] Agente de Consumo (`agents/consumo/`) — 5 tipos de análise, fallbacks
- [x] 6 Templates de Perfil (`cerebro/perfil-empreendedor-solo/`)
- [x] Formulário Web (`formulario.html`) — SPA com tabs, localStorage, export
- [x] Integração Formulário ↔ API (`sendSectionToApi()`)
- [x] Plataforma Web (`plataforma.html`) — Dashboard completo
- [x] `saveConfig()` melhorado — persiste API URL + envia token do Telegram
- [x] Scripts de alimentação (`alimentar.py`, `alimentar_com_input.py`)
- [x] Scripts de inicialização do Telegram Bot (Windows + Termux)
- [x] API Server Flask (`api_server.py`) — 14+ endpoints REST
- [x] Endpoint `/api/bot/start` — inicia bot via POST
- [x] Rota catch-all corrigida — aceita apenas GET
- [x] Encoding corrigido — UTF-8 em todos os outputs
- [x] Favicon e manifest.json criados
- [x] `llm_provider.py` — modelo configurável via env var, fallback para tinyllama
- [x] `index.html` — redireciona para `/plataforma.html`
- [x] Pipeline completo testado (formulário → API → agente → cérebro → carrossel)
- [x] Modelo `tinyllama` baixado no Ollama
- [x] `OLLAMA_MODEL` configurado como variável de ambiente
- [x] `beautifulsoup4` instalado
- [x] Token do Telegram configurado (`setx TELEGRAM_BOT_TOKEN`)
- [x] **Bot do Telegram rodando e conectado** (@NegreirosBot)
- [x] **API Flask rodando na porta 5000**
- [x] **Todos os endpoints testados** (health, stats, consumo, agentes, cerebro/arvore)

## 🔄 Em Progresso

- [ ] Preencher formulário web / templates markdown com conteúdo real
- [ ] Testar fluxo completo: formulário → API → consumo → cérebro → carrossel
- [ ] Gerar primeiros carrosséis e posts via plataforma
- [ ] Configurar token real do Telegram via `setx TELEGRAM_BOT_TOKEN`
  - ✅ Feito: `8789174206:AAEFbU9kz0PQQLFlCw4vMVzIYiXSnmVRjxQ`
- [ ] Instalar modelo leve no Ollama
  - ✅ Feito: `tinyllama:latest` puxado
- [ ] Instalar `beautifulsoup4`
  - ✅ Feito: já estava instalado

## 📋 Pendente (Próximos)

1. Testar fluxo completo end-to-end com Ollama ativo
2. Preencher perfil do empreendedor (Habilidades, Histórias, etc.)
3. Alimentar cérebro com conteúdo real via plataforma
4. Gerar primeiros carrosséis e posts
5. Configurar domínio / deploy (Vercel ou similar)
6. Documentar decisões e lições no cérebro

## 🚧 Blocked
- (none)