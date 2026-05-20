# API Documentation — OPB Sistema v2.3

> **Base URL:** `http://localhost:5000` (local) | `https://opb-sistema.vercel.app` (static)
> **Auth:** Bearer token via `Authorization` header or `opb_token` cookie
> **Format:** JSON request/response
> **Version:** 2.3

---

## Table of Contents
- [Authentication](#authentication)
- [Agents](#agents)
- [Carrossel](#carrossel)
- [Transcrição](#transcrição)
- [Cérebro](#cérebro)
- [Quadro de Avisos](#quadro-de-avisos)
- [Serviços](#serviços)
- [Stats & Analytics](#stats--analytics)
- [Arquivos](#arquivos)
- [Errors](#errors)

---

## Authentication

### POST `/api/auth/register`
Create a new user account.

**Rate Limit:** 5 requests / 5 minutes

**Body:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "min6chars",
  "full_name": "Optional Name"
}
```

**Response 201:**
```json
{
  "message": "User created successfully",
  "user_id": 1
}
```

**Response 400:**
```json
{
  "error": "Email já está em uso"
}
```

---

### POST `/api/auth/login`
Authenticate user and receive session token.

**Rate Limit:** 10 requests / minute

**Body:**
```json
{
  "email_or_username": "user@example.com",
  "password": "password123"
}
```

**Response 200:**
```json
{
  "message": "Login realizado com sucesso",
  "token": "abc123...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "username",
    "full_name": "User Name",
    "plan": "free",
    "onboarding_complete": false,
    "created_at": "2026-05-20T10:00:00"
  }
}
```

**Response 401:**
```json
{
  "error": "Senha incorreta"
}
```

---

### GET `/api/auth/validate`
Validate session token.

**Headers:** `Authorization: Bearer <token>`

**Response 200:**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "username",
    "plan": "free",
    "onboarding_complete": true
  }
}
```

**Response 401:**
```json
{
  "success": false,
  "message": "Token inválido ou expirado"
}
```

---

### POST `/api/auth/logout`
Invalidate session token.

**Headers:** `Authorization: Bearer <token>`

**Response 200:**
```json
{
  "success": true,
  "message": "Logout realizado com sucesso"
}
```

---

### POST `/api/auth/onboarding`
Complete user onboarding.

**Headers:** `Authorization: Bearer <token>`

**Body:**
```json
{
  "goal": "organizar",
  "income": "2k-5k",
  "interests": ["budget", "tithe", "debt"],
  "telegram_token": "optional",
  "api_url": "http://localhost:5000",
  "notifications": "enabled"
}
```

**Response 200:**
```json
{
  "success": true,
  "message": "Onboarding completo"
}
```

---

### GET `/api/auth/settings`
Get user settings.

**Headers:** `Authorization: Bearer <token>`

**Response 200:**
```json
{
  "id": 1,
  "user_id": 1,
  "theme": "dark",
  "language": "pt-BR",
  "notifications_enabled": 1,
  "telegram_connected": 0,
  "telegram_chat_id": null,
  "api_url": "http://localhost:5000"
}
```

---

### PUT `/api/auth/settings`
Update user settings.

**Headers:** `Authorization: Bearer <token>`

**Body:**
```json
{
  "theme": "light",
  "notifications_enabled": 0,
  "telegram_connected": 1,
  "telegram_chat_id": "123456"
}
```

**Response 200:**
```json
{
  "success": true,
  "message": "Settings updated"
}
```

---

### GET `/api/auth/analytics`
Get user usage analytics.

**Headers:** `Authorization: Bearer <token>`

**Query:** `?days=30`

**Response 200:**
```json
{
  "stats": [
    { "action": "login", "agent_name": null, "count": 15 },
    { "action": "carrossel_generate", "agent_name": "carrossel", "count": 8 }
  ],
  "days": 30
}
```

---

## Agents

### GET `/api/agentes`
List all available agents.

**Response 200:**
```json
[
  {
    "nome": "Transcrição",
    "pasta": "transcricao",
    "tipo": "Transcrição",
    "descricao": "Transcreve vídeos do YouTube",
    "status": "ativo",
    "icone": "fa-microphone-alt"
  }
]
```

---

### POST `/api/agentes/executar`
Execute a specific agent.

**Body:**
```json
{
  "agente": "carrossel",
  "args": ["tema", "tipo", "5"]
}
```

**Available agents:** `radagast`, `carrossel`, `text_generator`, `consumo`, `capa_video`

**Response 200:**
```json
{
  "sucesso": true,
  "stdout": "Agent output...",
  "stderr": "",
  "agente": "carrossel",
  "mensagem": "✅ carrossel executado com sucesso!"
}
```

---

## Carrossel

### POST `/api/carrossel`
Generate Instagram carousel.

**Body:**
```json
{
  "tema": "Como organizar finanças com fé",
  "tipo": "educational",
  "slides": 7
}
```

**Response 200:**
```json
{
  "sucesso": true,
  "saida": "Carousel generated...",
  "conteudo": "---\nname: \"Como organizar...\"\n---\n# Slide 1...",
  "filename": "como-organizar-financas-com-fe.md",
  "mensagem": "Carrossel gerado: Como organizar finanças com fé"
}
```

---

### GET `/api/carrossel/lista`
List all generated carousels.

**Response 200:**
```json
{
  "carrosseis": [
    {
      "filename": "como-organizar-financas.md",
      "titulo": "Como Organizar Finanças",
      "slides": 7,
      "data": "2026-05-20 14:30",
      "tamanho": 2048
    }
  ]
}
```

---

### GET `/api/carrossel/<filename>`
Get specific carousel content.

**Response 200:**
```json
{
  "filename": "como-organizar-financas.md",
  "conteudo": "---\nname: \"...\"\n---\n# Slide 1..."
}
```

---

### PUT `/api/carrossel/<filename>`
Update carousel content.

**Body:**
```json
{
  "conteudo": "---\nname: \"Updated\"\n---\n# Slide 1..."
}
```

**Response 200:**
```json
{
  "sucesso": true,
  "mensagem": "Carrossel atualizado"
}
```

---

### DELETE `/api/carrossel/<filename>`
Delete a carousel.

**Response 200:**
```json
{
  "sucesso": true,
  "mensagem": "Carrossel deletado"
}
```

---

## Transcrição

### POST `/api/transcricao`
Transcribe YouTube video.

**Body:**
```json
{
  "url": "https://youtube.com/watch?v=abc123"
}
```

**Response 200:**
```json
{
  "sucesso": true,
  "saida": "Transcription output...",
  "erro": "",
  "mensagem": "Transcrição iniciada!"
}
```

---

### GET `/api/transcricoes`
List saved transcriptions.

**Response 200:**
```json
{
  "transcricoes": [
    {
      "nome": "video-abc123",
      "arquivo": "video-abc123.md",
      "metadata": {
        "titulo": "Video Title",
        "video_id": "abc123",
        "data": "2026-05-20",
        "duracao": "15:30"
      }
    }
  ],
  "total": 1
}
```

---

### POST `/api/transcricao/ler`
Read specific transcription.

**Body:**
```json
{
  "nome": "video-abc123.md"
}
```

**Response 200:**
```json
{
  "sucesso": true,
  "conteudo": "Full transcription text...",
  "arquivo": "video-abc123.md"
}
```

---

## Cérebro

### GET `/api/cerebro/arvore`
Get file tree of `cerebro/` directory.

**Response 200:**
```json
[
  {
    "nome": "perfil-empreendedor-solo",
    "caminho": "cerebro/perfil-empreendedor-solo",
    "tipo": "pasta"
  },
  {
    "nome": "PERFIL.md",
    "caminho": "cerebro/perfil-empreendedor-solo/PERFIL.md",
    "tipo": "arquivo",
    "tamanho": 1024,
    "modificado": "2026-05-20T10:00:00"
  }
]
```

---

### GET `/api/cerebro/ler?caminho=cerebro/...`
Read specific file from cerebro.

**Query:** `?caminho=cerebro/perfil-empreendedor-solo/PERFIL.md`

**Response 200:**
```json
{
  "caminho": "cerebro/perfil-empreendedor-solo/PERFIL.md",
  "conteudo": "# Perfil\n\nContent here...",
  "nome": "PERFIL.md"
}
```

---

### GET `/api/cerebro/mapas`
List all MAPA.md files.

**Response 200:**
```json
[
  {
    "caminho": "cerebro/agentes/transcricao/MAPA.md",
    "pasta": "cerebro/agentes/transcricao",
    "descricao": "Mapa de conhecimento do agente"
  }
]
```

---

## Quadro de Avisos

### GET `/api/quadro-avisos`
List tasks.

**Query:** `?agente=geral` (optional)

**Response 200:**
```json
{
  "tarefas": [
    {
      "id": 1,
      "tarefa": "Gerar carrossel sobre finanças",
      "agente": "carrossel",
      "prioridade": "alta",
      "status": "pendente",
      "criado_em": "2026-05-20"
    }
  ],
  "pendentes": 1
}
```

---

### POST `/api/quadro-avisos`
Add new task.

**Body:**
```json
{
  "tarefa": "Gerar carrossel sobre finanças",
  "agente": "carrossel",
  "prioridade": "alta"
}
```

**Response 200:**
```json
{
  "sucesso": true,
  "tarefa": {
    "id": 1,
    "tarefa": "Gerar carrossel sobre finanças",
    "agente": "carrossel",
    "prioridade": "alta",
    "status": "pendente",
    "criado_em": "2026-05-20"
  }
}
```

---

### POST `/api/quadro-avisos/<id>/concluir`
Mark task as complete.

**Response 200:**
```json
{
  "sucesso": true,
  "tarefa": {
    "id": 1,
    "status": "concluido",
    "concluido_em": "2026-05-20"
  }
}
```

---

### DELETE `/api/quadro-avisos/<id>`
Delete a task.

**Response 200:**
```json
{
  "sucesso": true
}
```

---

## Serviços

### GET `/api/servicos/status`
Check service status.

**Response 200:**
```json
{
  "api": { "rodando": true, "porta": 5000 },
  "bot": { "rodando": true, "pid": "12345" },
  "projeto": "/path/to/opb-sistema",
  "timestamp": "2026-05-20T10:00:00"
}
```

---

### POST `/api/servicos/parar`
Stop services.

**Response 200:**
```json
{
  "sucesso": true,
  "parados": ["bot"],
  "mensagem": "Serviços parados!"
}
```

---

### POST `/api/servicos/reiniciar`
Restart services.

**Response 200:**
```json
{
  "sucesso": true,
  "mensagem": "🔄 Serviços reiniciados!",
  "bot_pid": 12345
}
```

---

### POST `/api/bot/start`
Start Telegram bot.

**Response 200:**
```json
{
  "sucesso": true,
  "mensagem": "🤖 Bot iniciado com sucesso!",
  "status": "started"
}
```

---

## Stats & Analytics

### GET `/api/stats`
Get project statistics.

**Response 200:**
```json
{
  "agentes_total": 9,
  "agentes_ativos": 7,
  "ideias_salvas": 15,
  "transcricoes": 8,
  "carrossel_gerados": 12,
  "conhecimento_salvo": 25,
  "capas_geradas": 5,
  "posts_gerados": 20,
  "timestamp": "2026-05-20T10:00:00"
}
```

---

### GET `/api/health`
Health check.

**Response 200:**
```json
{
  "status": "online",
  "project_path": "/path/to/opb-sistema",
  "timestamp": "2026-05-20T10:00:00",
  "auth_enabled": true
}
```

---

### GET `/api/ideias`
List saved ideas.

**Response 200:**
```json
{
  "ideias": [
    {
      "titulo": "Ideia sobre finanças católicas",
      "arquivo": "2026-05-20-ideia.md",
      "data": "2026-05-20"
    }
  ],
  "total": 1
}
```

---

### GET `/api/inspiracoes`
Get influencer profiles.

**Response 200:**
```json
{
  "profiles": [
    {
      "name": "Influencer Name",
      "nicho": "Católico",
      "descricao": "Description",
      "platforms": {
        "instagram": "https://instagram.com/...",
        "youtube": "https://youtube.com/..."
      }
    }
  ],
  "recursos": [
    {
      "titulo": "Documento",
      "tema": "Finanças",
      "descricao": "Description",
      "url": "https://..."
    }
  ]
}
```

---

## Arquivos

### POST `/api/arquivos`
List directory contents.

**Body:**
```json
{
  "caminho": "cerebro/perfil-empreendedor-solo"
}
```

**Response 200:**
```json
{
  "arquivos": [
    {
      "nome": "PERFIL.md",
      "tipo": "arquivo",
      "tamanho": 1024,
      "editavel": true
    }
  ],
  "caminho_atual": "cerebro/perfil-empreendedor-solo",
  "pai": "cerebro"
}
```

---

### POST `/api/arquivo/ler`
Read file content.

**Body:**
```json
{
  "caminho": "cerebro/perfil-empreendedor-solo/PERFIL.md"
}
```

**Response 200:**
```json
{
  "sucesso": true,
  "conteudo": "# Perfil\n\nContent...",
  "nome": "PERFIL.md"
}
```

---

## Other Endpoints

### POST `/api/capa-video`
Generate video cover ideas.

**Body:**
```json
{
  "tema": "Finanças católicas",
  "quantidade": 5
}
```

---

### POST `/api/consumo`
Process content via consumption agent.

**Body:**
```json
{
  "input": "Content to process...",
  "tipo": "completo",
  "titulo": "Content Title"
}
```

---

### POST `/api/text-generator`
Generate Instagram posts.

**Body:**
```json
{
  "objetivo": "Gerar post sobre dízimo",
  "tipo": "educational"
}
```

---

### POST `/api/posicionamento`
Positioning/competitor analysis.

**Body:**
```json
{
  "nicho": "Finanças católicas",
  "concorrentes": "competitor1\ncompetitor2"
}
```

---

### POST `/api/alimentar`
Feed content to the brain.

**Body:**
```json
{
  "input": "Content to feed...",
  "tipo": "completo",
  "titulo": "Content Title"
}
```

---

### POST `/api/narvi`
Video editing agent (placeholder).

**Body:**
```json
{
  "video": "path/to/video.mp4",
  "corte": "medio",
  "ratio": "both"
}
```

---

### POST `/api/radagast`
Content curation agent (placeholder).

**Body:**
```json
{
  "days_back": 1
}
```

---

### POST `/api/save-profile`
Save profile content to .md file.

**Body:**
```json
{
  "modulo": "basico",
  "content": "# Perfil\n\nContent...",
  "filename": "PERFIL.md"
}
```

---

### GET `/api/load-profile`
Load profile data from .md files.

**Response 200:**
```json
{
  "basico": { "nome": "...", "email": "..." },
  "habilidades": { "tech": "..." }
}
```

---

## Errors

### Standard Error Format
```json
{
  "error": "Error message",
  "code": "ERROR_CODE"
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `AUTH_REQUIRED` | 401 | Authentication required |
| `INVALID_TOKEN` | 401 | Token invalid or expired |
| `MISSING_FIELDS` | 400 | Required fields missing |
| `INVALID_JSON` | 400 | Invalid JSON body |
| `INVALID_FIELD` | 400 | Field validation failed |
| `MAX_LENGTH_EXCEEDED` | 400 | Field too long |
| `RATE_LIMITED` | 429 | Too many requests |
| `PERMISSION_DENIED` | 403 | Access denied |
| `NOT_FOUND` | 404 | Resource not found |
| `VALIDATION_ERROR` | 400 | Validation failed |
| `INTERNAL_ERROR` | 500 | Server error |

---

## Authentication Methods

### 1. Bearer Token (Header)
```
Authorization: Bearer your-token-here
```

### 2. Cookie
```
Cookie: opb_token=your-token-here
```

### 3. Query Parameter (PWA)
```
GET /api/stats?token=your-token-here
```

---

## Rate Limits

| Endpoint | Limit | Window |
|----------|-------|--------|
| `/api/auth/register` | 5 requests | 5 minutes |
| `/api/auth/login` | 10 requests | 1 minute |
| All other endpoints | 60 requests | 1 minute |

---

## Multi-Tenant

When authenticated, all data operations are scoped to the user:
- `data/users/{user_id}/acervo/` - User content
- `data/users/{user_id}/output/` - User generated posts
- `data/users/{user_id}/cerebro/` - User brain files

Without authentication, the system uses shared paths:
- `acervo/`
- `output/`
- `cerebro/`
