# TODO.md - Quadro de Tarefas do OPB Sistema

> Para agentes: leia este quadro antes de começar qualquer trabalho.

---

## 📋 Backlog

### Deploy & Infraestrutura
- [ ] **Configurar GH CLI e autenticar** ⚠️ PRIORIDADE
  - Instalar via `winget install GitHub.cli`
  - Executar `gh auth login`
- [ ] Criar repositório Git no GitHub
- [ ] Configurar credenciais Vercel no GitHub
- [ ] Deploy inicial no Vercel
- [ ] Configurar CI/CD automático (GitHub Actions)

### Agentes a Desenvolver
- [ ] **Agente Coordenador** - Coordena todos os outros agentes
- [ ] **Agente Carrossel** - Transforma texto em estrutura de carrossel (imagens)
- [ ] **Agente Transcrição** - Transcreve áudios/vídeos para texto
- [ ] **Agente Email** - Gera e envia emails automáticos
- [ ] **Agente Analytics** - Dashboard de métricas e insights

### Melhorias no Hub
- [ ] Adicionar gráficos de finanças (chart.js)
- [ ] Exportar dados para JSON/CSV
- [ ] Sincronizar com context-brain para personalização
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
| 2026-05-08 | Documentação (AGENTS.md, TODO.md) | opencode |
| 2026-05-08 | Configuração Vercel e GitHub Actions | opencode |

---

## 📝 Notas da Sessão

### Problema Atual
- GH CLI não está autenticado
- Usuário tentou instalar mas não conseguiu fazer login
- **Solução**: Tentar novamente depois ou usar método alternativo

### Alternativas se GH CLI não funcionar
1. Usar GitHub REST API diretamente (requer Personal Access Token)
2. Usar SSH/HTTPS manual (git clone, git push)
3. Deploy via Vercel CLI (`vercel deploy`)

### Como Continuar na Próxima Sessão
1. Abrir terminal PowerShell
2. `gh auth login` 
3. Seguir instruções (preferir autenticação via browser)
4. Continuar do passo de Deploy

---

## 🔄 Fluxo de Trabalho

```
Novo Agente → Leia AGENTS.md → Leia TODO.md → Escolha tarefa → Execute → Atualize TODO.md → Commit → Deploy
```

---

## 📌 Checklist para Deploy

- [x] Estrutura do projeto criada
- [x] Hub HTML (Pomodoro, Planner, Finanças, Ideias)
- [x] Página de perfil
- [x] Agente coordenador
- [x] Configuração Vercel (vercel.json)
- [x] CI/CD (GitHub Actions)
- [x] .gitignore
- [ ] GH CLI autenticado ← **BLOQUEADO**
- [ ] Repo criado no GitHub ← **AGUARDA GH CLI**
- [ ] Primeiro commit pushado
- [ ] Deploy no Vercel via GitHub

---

_Last updated: 2026-05-08_
