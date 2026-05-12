# Obsidian Integration Guide

> Como usar o OPB Sistema com Obsidian

## 🚀 Quick Start

1. **Abrir o projeto como Vault no Obsidian**
   - Abra o Obsidian
   - "Open folder as vault"
   - Selecione a pasta `opb-sistema`

2. **Pronto!** Todos os arquivos do cérebro são compatíveis.

---

## ⌨️ Comandos Rápidos (No PC)

### Integração Python
```bash
# Abrir Obsidian com todo o projeto
python utils/obsidian_integration.py

# Abrir arquivo específico
python utils/obsidian_integration.py open quem-sou
python utils/obsidian_integration.py open projetos
python utils/obsidian_integration.py open brain
```

### Comandos Disponíveis
| Comando | Arquivo |
|---------|---------|
| `python obsidian.py open brain` | MAPA.md |
| `python obsidian.py open quem-sou` | quem-sou.md |
| `python obsidian.py open projetos` | ativos.md |
| `python obsidian.py open regras` | linguagem-escrita.md |
| `python obsidian.py open agentes` | AGENTS.md |
| `python obsidian.py open ideas` | Ideas do acervo |
| `python obsidian.py open transcricoes` | Transcrições |

---

## 🎯 Fluxo de Trabalho

### Manhã
1. Abra o Obsidian → `python utils/obsidian_integration.py`
2. Veja o MAPA.md para contexto
3. Check quem-sou.md para identidade

### Durante o Dia
- Capture ideias via Telegram Bot
- Execute agentes pelo terminal
- Continue trabalhando no Obsidian

### noite
- Revise transcrições no Obsidian
- Atualize o cérebro com novas regras

---

## 📱 Via Telegram

Envie `/obsidian` ao bot para ver instruções:

```
🔗 *Obsidian Integration*

O cerebro do OPB Sistema usa arquivos markdown 
compatíveis com Obsidian!

*No seu PC:*
python utils/obsidian_integration.py open quem-sou
python utils/obsidian_integration.py open projetos
python utils/obsidian_integration.py
```

---

## 💡 Dicas Obsidian

- **Ctrl+O** - Quick switcher (pular entre arquivos)
- **Ctrl+Shift+F** - Buscar em todos os arquivos
- **Ctrl+Shift+K** - Linked mentions
- **Ctrl+E** - Toggle edit/preview

---

## 🔗 Pastas Principais no Obsidian

```
opb-sistema/
├── MAPA.md                    ← Comece aqui!
├── negocio/
│   └── governanca/
│       └── regras/
│           └── quem-sou.md    ← Sua identidade
├── agentes/                   ← Docs dos agentes
├── acervo/
│   ├── ideias/               ← Suas ideias
│   ├── transcricoes/         ← Videos transcritos
│   └── pesquisas/            ← Pesquisas de mercado
└── hub.html                  ← Hub produtividade
```

---

_Last updated: 2026-05-12_