# AGENTS.md - OPB Sistema

> **INFORMAÇÕES PARA AGENTES** - Leia este arquivo antes de qualquer trabalho!

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

---

## 📁 Estrutura de Arquivos

```
opb-sistema/
├── MAPA.md                    # Mapa raiz do cérebro
├── agents/                    # Agentes Python (código executável)
│   ├── capa_video/            # Gera ideias de thumbnail YouTube
│   ├── carrossel/             # Gera estruturas de carrossel Instagram
│   ├── coordinator/          # Agente coordenador
│   ├── designer/             # Gera diagramas, briefings, paletas
│   ├── posicionamento/       # Pesquisa de mercado
│   ├── telegram_bot/         # Interface Telegram
│   └── text_generator/      # Geração de posts Instagram
├── cerebro/                  # CÉREBRO - contexto vivo (MARKDOWN)
│   ├── MAPA.md              # Índice raiz
│   ├── negocio/             # Tudo do trabalho
│   │   ├── governanca/      # Regras, decisões, lições, referências
│   │   │   ├── regras/      # Regras de operação
│   │   │   │   ├── quem-sou.md        ← IDENTIDADE
│   │   │   │   ├── linguagem-escrita.md
│   │   │   │   └── cerebro-manutencao.md
│   │   │   ├── decisoes/
│   │   │   └── licoes/
│   │   ├── areas/           # Marketing, conteúdo, suporte...
│   │   ├── produtos/        # Catálogo de produtos
│   │   ├── infra/           # Sistemas internos
│   │   └── projetos/        # Iniciativas
│   │       └── ativos.md   ← METAS ATUAIS
│   ├── pessoal/             # Vida pessoal (ACL)
│   ├── agentes/             # Config de agentes IA
│   ├── playbooks/           # Manuais executáveis
│   ├── acervo/              # Conteúdo produzido
│   └── seguranca/           # Permissões
├── hub.html                  # Hub produtividade
├── index.html               # Configurador de perfil
├── server.py                # Servidor local
└── vercel.json              # Config Vercel
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
- Hub de produtividade (Pomodoro, Planner, Finanças, Ideias)
- Página de configuração de perfil
- Agente coordenador
- Configuração Vercel e CI/CD
- Cérebro (template OPB School integrado)
- Deploy automático

### 🔜 Backlog
- Agente Carrossel
- Agente Transcrição
- Agente Email
- Agente Analytics

---

## 📝 Mantendo o Cérebro Vivo

Após qualquer conversa importante, o agente deve perguntar:
> "Quer que eu atualize o cérebro com o que aprendemos?"

Ou executar:
> "Atualiza o cérebro com as decisões e lições desta sessão."

---

_Last updated: 2026-05-12_