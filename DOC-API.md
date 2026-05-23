# ==========================================
# 🚀 API Server — OPB Sistema
# Conecta a plataforma web aos agentes reais
# ==========================================

> **Como funciona:** Este servidor Flask expõe uma API REST que a plataforma HTML (frontend) consome. Cada botão da plataforma dispara uma requisição para o servidor, que executa o agente Python correspondente e retorna o resultado.

## Arquitetura

```
┌─────────────────┐     HTTP/REST      ┌──────────────────┐
│  plataforma.html │ ──────────────────►│  api_server.py    │
│  (Frontend)      │     (JSON)         │  (Flask API)      │
│  localhost:5000  │  ◄───────────────── │  localhost:5000   │
└─────────────────┘                     └────────┬─────────┘
                                                  │ subprocess
                                          ┌───────┴────────┐
                                          │  Agentes Python │
                                          │  • Transcrição  │
                                          │  • Capa Vídeo   │
                                          │  • Carrossel    │
                                          │  • Consumo      │
                                          │  • Text Gen     │
                                          │  • Posicionamento│
                                          └─────────────────┘
```

## Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/health` | Health check |
| GET | `/api/stats` | Estatísticas do projeto |
| GET | `/api/agentes` | Lista agentes disponíveis |
| GET | `/api/ideias` | Lista ideias capturadas |
| GET | `/api/transcricoes` | Lista transcrições salvas |
| POST | `/api/transcricao` | Transcreve vídeo YouTube |
| POST | `/api/transcricao/ler` | Lê conteúdo de uma transcrição específica |
| POST | `/api/capa-video` | Gera ideias de capa |
| POST | `/api/carrossel` | Gera carrossel |
| POST | `/api/consumo` | Processa conteúdo |
| POST | `/api/text-generator` | Gera posts Instagram |
| POST | `/api/posicionamento` | Analisa posicionamento |
| POST | `/api/alimentar` | Alimenta o cérebro |
| POST | `/api/arquivos` | Lista arquivos/diretórios do projeto (navegador) |
| POST | `/api/arquivo/ler` | Lê conteúdo de um arquivo do projeto |
| POST | `/api/bot/start` | Inicia o Telegram Bot |
| POST | `/api/start` | Inicia serviços remotamente |
| POST | `/api/save-profile` | Salva perfil do usuário |
| GET | `/api/load-profile` | Carrega perfil + concorrentes do `quem-sou.md` |
| POST | `/api/obsidian/abrir` | Abre arquivo no Obsidian |
| GET | `/api/obsidian/status` | Verifica se Obsidian está instalado |
| POST | `/api/notion/config` | Salva/configura token do Notion |
| GET | `/api/notion/config` | Lê configuração do Notion |
| POST | `/api/notion/sync` | Envia conteúdo para Notion (com fallback local) |

### Detalhes de Endpoints Específicos

#### POST `/api/arquivos`
**Body:** `{ "caminho": "." }` (relativo ao diretório do projeto)
**Resposta:** `{ "arquivos": [...], "caminho_atual": "...", "pai": "..." }`

#### POST `/api/arquivo/ler`
**Body:** `{ "caminho": "AGENTS.md" }`
**Resposta:** `{ "sucesso": true, "conteudo": "...", "nome": "AGENTS.md" }`

#### POST `/api/transcricao/ler`
**Body:** `{ "nome": "video_id_data.md" }`
**Resposta:** `{ "sucesso": true, "conteudo": "...", "arquivo": "..." }`

## Instalação

```bash
pip install flask flask-cors python-dotenv yt-dlp feedparser
```

## Iniciar

```bash
python api_server.py
```

Acesse: **http://localhost:5000**

O servidor serve tanto a API quanto o frontend (plataforma.html).

---

_Last updated: 2026-05-19_