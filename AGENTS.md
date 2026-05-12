# AGENTS.md - OPB Sistema

> **INFORMAÇÕES PARA AGENTES** - Leia este arquivo antes de qualquer trabalho!

---

## 🆕 Guia Rápido para Novo Agente

1. **Leia TODO.md** - Veja as tarefas pendentes e progresso
2. **Leia context-brain/*.json** - Entenda o contexto do negócio
3. **Execute sua tarefa**
4. **Atualize TODO.md** - Marque como concluído
5. **Commite no Git**
6. **Deploy no Vercel**

---

## 📌 Informações do Projeto

### Identidade
- **Nome**: OPB Sistema
- **Tipo**: Sistema multi-agente AI para solopreneurs
- **Stack**: Python 3.8+, Ollama (Llama3), HTML/CSS/JS, Bootstrap 5

### Infraestrutura
| Serviço | URL |
|---------|-----|
| **GitHub** | https://github.com/cleiton-negreiros/ |
| **Vercel** | https://vercel.com/cleiton-negreiros-projects/ |

---

## 📁 Estrutura de Arquivos

```
opb-sistema/
├── agents/
│   ├── coordinator/main.py      # Agente coordenador (orquestrador)
│   └── text_generator/main.py  # Gerador de posts Instagram
├── context-brain/               # CONTEXTO DO NEGÓCIO (LEIA ESTES)
│   ├── business-core.json       # Missão, visão, valores, tom de voz
│   ├── personal-profile.json   # Perfil pessoal, habilidades, agenda
│   └── goals.json             # Objetivos, KRs, métricas
├── utils/
│   ├── context_loader.py       # Carregador de contexto
│   └── llm_provider.py        # Provedor LLM (Ollama)
├── output/text_posts/          # Posts gerados (não versionar)
├── hub.html                    # Hub produtividade (Pomodoro, Planner, Finanças, Ideias)
├── index.html                  # Configurador de perfil
├── server.py                   # Servidor local (porta 8088)
├── iniciar.bat                 # Atalho iniciar
├── vercel.json                # Config Vercel
├── .github/workflows/deploy.yml # CI/CD
├── AGENTS.md                  # ESTE ARQUIVO
├── TODO.md                    # Quadro de tarefas
└── README.md
```

---

## 🎯 Contexto do Negócio (Ler Obrigatório)

### business-core.json
```json
{
  "valores": ["autenticidade", "praticidade", "impacto", "crescimento consciente"],
  "tom_de_voz": "direto, inspirador, sem jargões, próximo como uma conversa de café",
  "publico_alvo": "empreendedores solitários e pequenos times que querem crescer sem burnout",
  "missao": "ajudar solopreneurs a automatizar o repetitivo para focar no que realmente importa",
  "visao": "ser o cérebro por trás de mil negócios unipessoais lucrativos e sustentáveis"
}
```

### personal-profile.json
- Nome, descrição, habilidades principais
- Limitações (o que prefere evitar)
- Horários produtivos (manhã/tarde/noite)
- Preferências de comunicação

### goals.json
- Trimestre atual
- Objetivos com Key Results
- Métricas de acompanhamento

---

## 🤖 Agentes Disponíveis

### Agente Coordenador
**Caminho**: `agents/coordinator/main.py`

**Uso**:
```bash
# Modo interativo
python agents/coordinator/main.py

# Listar tarefas
python agents/coordinator/main.py list

# Executar tarefa específica
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
# Iniciar tudo
python server.py

# Hub de produtividade
http://localhost:8088/hub.html

# Configurar perfil
http://localhost:8088/index.html

# Usar coordenador
python agents/coordinator/main.py
```

---

## ⚠️ Status do Projeto

### ✅ Implementado
- Hub de produtividade (Pomodoro, Planner, Finanças, Ideias)
- Página de configuração de perfil
- Agente coordenador
- Configuração Vercel e CI/CD
- Documentação completa

### 🔜 Próximo Passo (BLOQUEADO)
- **Deploy**: Aguardando autenticação do GH CLI

### 🔜 Backlog
- Agente Carrossel
- Agente Transcrição
- Agente Email
- Agente Analytics

---

## 📝 Notas da Sessão

### Problema: GH CLI não autenticado
O usuário tentou instalar o GitHub CLI (`winget install GitHub.cli`) mas não conseguiu fazer login com `gh auth login`.

**Soluções alternativas:**
1. Tentar novamente: `gh auth login` (escolher autenticação via browser)
2. Criar Personal Access Token manualmente
3. Usar Vercel CLI para deploy direto

### Como Continuar
1. `gh auth login` no terminal PowerShell
2. Continuar deploy (ver TODO.md)

---

_Last updated: 2026-05-08_
