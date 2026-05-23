# AGENTS.md - OPB Sistema

> **INFORMAÇÕES PARA AGENTES** - Leia este arquivo antes de qualquer trabalho!

---

## Regra de Trabalho

Você (agente) sempre executa os comandos e ações por mim. Eu tomo as decisões de negócio e você implementa. Se eu pedir algo, faça — não pergunte "quer que eu faça X?" ou "prefere Y?". Apenas execute.

---

## 🆕 Guia Rápido para Novo Agente

1. **Leia MAPA.md** - Estrutura do cérebro
2. **Leia negocio/governanca/** - Contexto do negócio
3. **Leia negocio/projetos/ativos.md** - Projetos em andamento
4. **Execute sua tarefa**
5. **Atualize o cérebro** se necessário (crie arquivos em negocio/governanca/regras/)
6. **Commite no Git**
7. **Deploy no Vercel**

---

## 📌 Informações do Projeto

### Identidade
- **Nome**: OPB Sistema
- **Tipo**: Sistema multi-agente AI para solopreneurs
- **Stack**: Python 3.8+, Ollama (Llama3), HTML/CSS/JS, Bootstrap 5

### Infraestrutura
| Serviço | URL |
|---------|-----|
| **GitHub** | https://github.com/cleiton-negreiros/opb-sistema |
| **Vercel** | https://opb-sistema.vercel.app |
| **API Local** | http://localhost:5000 (rode `api_server.py`) |
| **Frontend Local** | http://localhost:5000 (api_server serve frontend + API) |

---

## 📁 Estrutura de Arquivos

```
opb-sistema/
├── api_server.py             # Servidor Flask (porta 5000) — API + frontend
├── server.py                 # Servidor local alternativo (porta 8088)
├── utils/
│   ├── llm_provider.py       # Conexão com Ollama (tinyllama)
│   ├── profile_loader.py     # Leitor unificado do perfil (quem-sou.md)
│   └── ...
├── agents/                   # Agentes Python
│   ├── carrossel/            # Gera carrosséis (4 tipos)
│   ├── capa_video/           # Ideias de thumbnail YouTube
│   ├── consumo/              # Processa textos, PDFs, URLs
│   ├── text_generator/       # Geração de posts Instagram
│   ├── posicionamento/       # Pesquisa de mercado
│   ├── radagast/             # Curadoria (yt-dlp + RSS, sem APIs pagas)
│   ├── narvi/                # Editor de vídeo (FFmpeg)
│   ├── telegram_bot/         # Interface Telegram
│   ├── coordinator/          # Agente coordenador
│   └── designer/             # Diagramas, briefings, paletas
├── cerebro/perfil-empreendedor-solo/
│   ├── plataforma.html       # Dashboard PWA principal
│   ├── formulario.html       # Formulário de perfil (6 seções)
│   ├── manifest.json         # PWA manifest
│   └── sw.js                 # Service Worker
├── negocio/governanca/
│   ├── quem-sou.md           ← IDENTIDADE (lido por todos agentes)
│   └── regras/
│       ├── linguagem-escrita.md
│       └── cerebro-manutencao.md
├── acervo/                   # Conteúdo produzido
│   ├── transcricoes/         # Transcrições de vídeo (.md)
│   └── conhecimento/         # Conhecimento processado
├── iniciar-dia.bat           # Inicia tudo (API + Telegram Bot)
├── requirements.txt
├── vercel.json
└── DOC-API.md
```

---

## 🧠 Cérebro - Como Usar

O cérebro é a **fonte de verdade** para contexto. Todo agente deve ler:

### Leitura obrigatória (toda sessão)
1. `MAPA.md` - Estrutura geral
2. `negocio/governanca/regras/quem-sou.md` - Identidade e tom de voz
3. `negocio/projetos/ativos.md` - O que está em andamento

### Escrita (quando relevante)
- Novas regras → `negocio/governanca/regras/`
- Decisões → `negocio/governanca/decisoes/AAAA-MM.md`
- Lições aprendidas → `negocio/governanca/licoes/`
- Conteúdo gerado → `acervo/`

### Padrão de arquivo
```markdown
---
name: "Título"
description: "O que é"
tipo: referencia|decisao|licao|regra
updated_at: AAAA-MM-DD
---

# Título

> Descrição em uma linha

## Detalhes...
```

---

## 🤖 Agentes Disponíveis

### API Server (Flask — porta 5000)
**Arquivo**: `api_server.py`

Serve frontend + todos os endpoints REST. Iniciar:
```bash
python api_server.py
```

### Endpoints da API
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/health` | Health check |
| GET | `/api/stats` | Estatísticas do projeto |
| GET | `/api/agentes` | Lista agentes disponíveis |
| GET | `/api/ideias` | Lista ideias capturadas |
| GET | `/api/transcricoes` | Lista transcrições salvas |
| POST | `/api/transcricao` | Transcreve vídeo YouTube |
| POST | `/api/transcricao/ler` | Lê conteúdo de uma transcrição |
| POST | `/api/capa-video` | Gera ideias de capa |
| POST | `/api/carrossel` | Gera carrossel |
| POST | `/api/consumo` | Processa conteúdo |
| POST | `/api/text-generator` | Gera posts |
| POST | `/api/posicionamento` | Analisa posicionamento |
| POST | `/api/alimentar` | Alimenta o cérebro |
| POST | `/api/arquivos` | Lista arquivos do projeto (navegador) |
| POST | `/api/arquivo/ler` | Lê conteúdo de arquivo |
| POST | `/api/bot/start` | Inicia Telegram Bot |
| POST | `/api/start` | Inicia serviços remotamente |
| POST | `/api/save-profile` | Salva perfil do usuário |

### Agente Coordenador
**Caminho**: `agents/coordinator/main.py`

**Uso**:
```bash
python agents/coordinator/main.py
python agents/coordinator/main.py list
python agents/coordinator/main.py run 1
```

### Agente Text Generator
**Caminho**: `agents/text_generator/main.py`

**Uso**:
```bash
python agents/text_generator/main.py "<objetivo>" [tipo_post]
```

**Tipos de Post**: `educational`, `inspirational`, `promotional`, `engagement`

---

## 🔧 Comandos Úteis

```bash
# Iniciar servidor local
python server.py

# Hub de produtividade
http://localhost:8088/hub.html

# Usar coordenador
python agents/coordinator/main.py

# Deploy (já automatizado via CI/CD)
# A cada push no master, deploy automático no Vercel
```

---

## ⚠️ Status do Projeto

### ✅ Implementado
- Dashboard PWA mobile-first com navegação lateral (plataforma.html)
- Formulário de perfil (6 seções: Habilidades, Histórias, Cosmovisão, Público, Posicionamento, Narrativa)
- Agente Carrossel (4 tipos com fallback textual sem LLM + botão copiar)
- Agente Consumo (5 tipos de análise)
- Agente Capa Vídeo, Text Generator, Posicionamento
- Agente Transcrição (YouTube) com visualização formatada + botão copiar
- Agente Radagast (reescrito sem Apify/Claude — só yt-dlp + RSS, gratuito)
- Agente Narvi (editor de vídeo com FFmpeg)
- Telegram Bot integrado (@NegreirosBot)
- API Server Flask (18 endpoints REST)
- Navegador de Arquivos na plataforma (listar/ler arquivos do projeto)
- Perfil unificado (`utils/profile_loader.py` + `quem-sou.md`)
- Ollama com `tinyllama` (modelo padrão, ~637MB, roda com 3.4GB RAM)
- iniciar-dia.bat (inicia API + Telegram Bot em 6 passos)
- Suporte PWA (manifest.json, sw.js, mobile-first)
- Deploy Vercel + CI/CD

### 🔜 Backlog
- Preencher perfil do empreendedor com conteúdo real
- Gerar primeiros carrosséis e posts via plataforma
- Pesquisar solução para acessar iniciar-dia.bat remotamente (SSH ou /api/start)
- Agente Analytics
- Configurar domínio personalizado

---

## 📝 Mantendo o Cérebro Vivo

Após qualquer conversa importante, o agente deve perguntar:
> "Quer que eu atualize o cérebro com o que aprendemos?"

Ou executar:
> "Atualiza o cérebro com as decisões e lições desta sessão."

---

---

## 🗓️ Progresso — 22/05/2026 (Sexta)

### Feito hoje
- **Correções carregamento perfil**: identidade visual salva/recuperada, previews de cor ao vivo
- **Funções ausentes criadas**: `startRoutine()`, `quickIdeia()`, `showAlimentarModal()`, `saveNotes()` — zero ReferenceErrors
- **Modal carrossel morto removido**: 6 botões sem handler deletados
- **Snapshot estático**: `snapshot.html` (60KB, self-contained, dados reais) + `gerar_snapshot.py`
- **Deploy Vercel**: 3 commits no master, CI/CD deve publicar em `https://opb-sistema.vercel.app/snapshot`
- **Regra de trabalho**: AGENTE EXECUTA — USUÁRIO DECIDE (linha 10)

### Pendente para amanhã
- [ ] Verificar deploy da snapshot
- [ ] Aplicar `showResult()` nos demais agentes
- [ ] Salvar resultados no servidor via API
- [ ] Card Jornada IA de hoje

---

## 🗓️ Jornada IA — Alimentação Diária

**Instrução:** Toda nova funcionalidade implementada deve ser registrada na seção Jornada IA da plataforma (`plataforma.html → #page-jornada-ia`). Cada dia de vira um card na timeline (tema + realizações + tags). Manter os textos de compartilhamento (LinkedIn, Twitter, Instagram, Substack, Carrossel) atualizados com os novos marcos. Isso gera autoridade pública e documenta o progresso real.

---

---

## 🧠 Integração com o Cérebro

**Regra:** Todo agente que gera texto deve chamar `get_brain_context()` no início e incluir o resultado no prompt. Agentes técnicos (corta-silencio, transcrever-audio, etc.) podem pular. Os utilitários em `utils/` (`context_loader.py`, `profile_loader.py`) agora são profile-aware — aceitam `profile_id` opcional e nunca quebram se arquivos não existirem.

**Agentes integrados:** consultor-negocios, text_generator, carrossel, consumo, designer, capa_video ✅
**Agentes que não precisam:** corta-silencio, transcrever-audio, telegram_bot, coordinator, quadro-de-avisos, hashtags

---

_Last updated: 2026-05-22_