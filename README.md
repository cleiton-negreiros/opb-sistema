# OPB Sistema - One Person Business AI Agent System

🤖 Sistema multi-agente de IA para solopreneurs automatizarem tarefas repetitivas.

## 🚀 Quick Start

```bash
# Iniciar servidor local
python server.py

# Acessar:
# - Hub de Produtividade: http://localhost:8088/hub.html
# - Configurar Perfil: http://localhost:8088/index.html
```

## 📦 Deploy no Vercel

### 1. Criar repositório no GitHub
```bash
git init
git remote add origin https://github.com/cleiton-negreiros/opb-sistema.git
git add .
git commit -m "feat: setup inicial"
git push -u origin main
```

### 2. Deploy no Vercel
1. Acesse [vercel.com/cleiton-negreiros-projects](https://vercel.com/cleiton-negreiros-projects)
2. Clique "New Project"
3. Importe o repositório do GitHub
4. Deploy!

## 📁 Estrutura do Projeto

```
opb-sistema/
├── agents/              # Agentes especializados
│   ├── coordinator/    # Agente coordenador
│   └── text_generator/ # Gerador de posts
├── context-brain/      # Contexto do negócio
├── utils/              # Utilitários
├── hub.html            # Hub de produtividade
├── index.html          # Configurador de perfil
└── server.py           # Servidor local
```

## 🧠 Contextos

Edite os arquivos em `context-brain/` para personalizar:
- `business-core.json` - Missão, visão, valores
- `personal-profile.json` - Seu perfil
- `goals.json` - Objetivos e métricas

## 🤖 Agentes

| Agente | Status | Descrição |
|--------|--------|-----------|
| Coordenador | ✅ | Orquestra os demais agentes |
| Text Generator | ✅ | Gera posts para Instagram |
| Carrossel | 🔜 | Transforma texto em carrossel |
| Transcrição | 🔜 | Transcreve áudios/vídeos |
| Email | 🔜 | Gera e envia emails |
| Analytics | 🔜 | Dashboard de métricas |

## 🛠️ Tecnologias

- Python 3.8+
- Ollama (Llama3) para LLM local
- HTML/CSS/JavaScript
- Bootstrap 5
- Vercel (deploy)

## 📊 Métricas

- Posts gerados: `context-brain/goals.json` → `posts_gerados`
- Tempo economizado: `context-brain/goals.json` → `tempo_economizado_semanal`

---

Made with ❤️ for solopreneurs
