# TODO.md - Quadro de Tarefas do OPB Sistema

> Para agentes: leia este quadro antes de qualquer trabalho!

---

## 📋 Backlog

### Deploy & Infraestrutura
- [x] **Configurar GH CLI e autenticar** ✓
- [x] Criar repositório Git no GitHub ✓
- [x] Deploy inicial no Vercel ✓
- [x] Configurar CI/CD automático (GitHub Actions) ✓

### Cérebro (OPB School Template)
- [x] Integrar template cerebro-template ✓
- [x] Converter context-brain JSON para markdown ✓
- [x] Atualizar AGENTS.md para usar cérebro ✓
- [ ] Configurar install.sh para Windows (opcional)

### Agentes a Desenvolver
- [x] **Agente Coordenador** ✓
- [ ] **Agente Carrossel** - Transforma texto em estrutura de carrossel
- [ ] **Agente Transcrição** - Transcreve áudios/vídeos para texto
- [ ] **Agente Email** - Gera e envia emails automáticos
- [ ] **Agente Analytics** - Dashboard de métricas e insights

### Melhorias no Hub
- [ ] Adicionar gráficos de finanças (chart.js)
- [ ] Exportar dados para JSON/CSV
- [x] Sincronizar com cérebro para personalização ✓
- [ ] Adicionar modo offline (PWA)
- [ ] Temas claro/escuro

### Conteúdo & Marketing
- [ ] Template de posts para cada tipo
- [ ] Calendário editorial
- [ ] Banco de hashtags
- [ ] Análise de concorrentes (placeholder)

---

## 🚧 Em Andamento

_(Nenhuma tarefa em progresso)_

---

## ✅ Concluídos

| Data | Tarefa | Agente |
|------|--------|--------|
| 2026-05-08 | Setup inicial do projeto | opencode |
| 2026-05-08 | Agente de texto (Instagram) | opencode |
| 2026-05-08 | Hub de produtividade | opencode |
| 2026-05-08 | Página de configuração de perfil | opencode |
| 2026-05-08 | Agente coordenador | opencode |
| 2026-05-08 | Configuração Vercel e GitHub Actions | opencode |
| 2026-05-12 | GH CLI autenticado | opencode |
| 2026-05-12 | Repositório GitHub criado | opencode |
| 2026-05-12 | CI/CD configurado | opencode |
| 2026-05-12 | Deploy Vercel (via Vercel CLI) | opencode |
| 2026-05-12 | Template Cerebro integrado | opencode |

---

## 📝 Estrutura do Cérebro

```
cérebro/
├── MAPA.md                           ← LEIA PRIMEIRO
├── negocio/governanca/
│   ├── regras/
│   │   ├── quem-sou.md              ← IDENTIDADE
│   │   ├── linguagem-escrita.md
│   │   └── cerebro-manutencao.md
│   └── projetos/
│       └── ativos.md                 ← METAS ATUAIS
├── agentes/
├── playbooks/
└── acervo/
```

---

## 🔄 Fluxo de Trabalho

```
Novo Agente → Leia AGENTS.md → Leia MAPA → Execute → Atualize cérebro → Commit → Deploy
```

---

## 📌 URLs

- **Vercel**: https://opb-sistema.vercel.app
- **GitHub**: https://github.com/cleiton-negreiros/opb-sistema

---

_Last updated: 2026-05-12_