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
| GET | `/api/cerebro/arvore` | Árvore de arquivos do cérebro |
| GET | `/api/cerebro/ler` | Lê conteúdo de um arquivo |
| GET | `/api/cerebro/mapas` | Lista todos os MAPAs |
| GET | `/api/ideias` | Lista ideias capturadas |
| POST | `/api/transcricao` | Transcreve vídeo YouTube |
| POST | `/api/capa-video` | Gera ideias de capa |
| POST | `/api/carrossel` | Gera carrossel |
| POST | `/api/consumo` | Processa conteúdo |
| POST | `/api/text-generator` | Gera posts Instagram |
| POST | `/api/posicionamento` | Analisa posicionamento |
| POST | `/api/alimentar` | Alimenta o cérebro |

## Instalação

```bash
pip install flask flask-cors
```

## Iniciar

```bash
python api_server.py
```

Acesse: **http://localhost:5000**

---

_Last updated: 2026-05-14_