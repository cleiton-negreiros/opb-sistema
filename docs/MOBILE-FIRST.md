# 📱 Plataforma Mobile-First — Ideias para Férias

## Princípios (Baseado em pesquisa 2026)
- **72% do tráfego web é mobile** — design para celular primeiro
- **Thumb Zone**: ações principais na parte inferior da tela
- **48x48px mínimo** para botões (evitar "fat finger")
- **16px mínimo** para texto (sem zoom)
- **3 segundos** máximo de carregamento em 4G
- **Single-column** por padrão (celular é vertical)

---

## 🎯 Ideias para Melhorar a Plataforma

### 1. Navegação Simplificada
- ✅ **Bottom Navigation** (já implementado) — 5 itens principais
- ➕ **Swipe gestures** entre páginas (Dashboard → Cérebro → Agentes)
- ➕ **Quick Actions** flutuante (botão + no centro inferior)
- ➕ **Search global** no topo (busca ideias, tarefas, arquivos)

### 2. Dashboard Otimizado para Mobile
- ➕ **Cards grandes** (fácil de tocar)
- ➕ **Resumo do dia** em 1 tela (greeting + tarefas + métricas)
- ➕ **Atalhos rápidos** (gravar áudio, nova ideia, nova tarefa)
- ➕ **Widget de clima/hora** (contexto para trabalho)

### 3. Agentes como "Apps" no Celular
- ➕ **Grid de ícones** estilo launcher de celular
- ➕ **Cada agente = 1 card** com botão "Executar"
- ➕ **Histórico por agente** (últimos resultados)
- ➕ **Notificações** quando agente termina (PWA push)

### 4. Entrada de Dados Simplificada
- ➕ **Voice-to-text** (já funciona via Telegram)
- ➕ **Formulários curtos** (máx 3 campos por tela)
- ➕ **Auto-save** (não perder dados se fechar)
- ➕ **Templates** (ideia rápida, tarefa rápida)

### 5. Modo Offline
- ➕ **Cache de dados** (últimas ideias, tarefas)
- ➕ **Fila de ações** (salva local, sincroniza quando online)
- ➕ **Service Worker** aprimorado (já existe, melhorar)

### 6. Integração com Telegram
- ➕ **Link direto** do bot para plataforma
- ➕ **Webhook** (atualiza plataforma quando recebe áudio)
- ➕ **Espelhar transcricões** no painel

### 7. Performance
- ➕ **Lazy loading** de páginas (carrega sob demanda)
- ➕ **Imagens otimizadas** (WebP/AVIF)
- ➕ **CSS mínimo** (remover não usado)
- ➕ **150KB critical path** (HTML + CSS initial)

---

## 📋 Prioridade para Férias (Simples e Útil)

### Semana 1: Essencial
1. **Voice-to-text via Telegram** ✅ (já feito)
2. **Dashboard resumido** (1 tela, 3 cards)
3. **Quick Actions** (botão flutuante +)

### Semana 2: Agentes
4. **Grid de agentes** (launcher style)
5. **Corta-silêncio** integrado na plataforma
6. **Transcrição de áudio** integrada

### Semana 3: Polimento
7. **Modo offline** básico
8. **Notificações PWA**
9. **Performance** (lazy loading)

---

## 🔧 O que já funciona hoje
| Recurso | Status | Mobile? |
|---------|--------|---------|
| Bottom Navigation | ✅ | ✅ |
| Dashboard | ✅ | ⚠️ (muita info) |
| Meu Perfil | ✅ | ✅ |
| Cérebro | ✅ | ✅ |
| Quadro de Avisos | ✅ | ✅ |
| Telegram Bot | ✅ | ✅ |
| Corta-silêncio | ✅ | ✅ (Termux) |
| Transcrição áudio | ✅ | ✅ (Termux) |

---

_2026-05-21 — Plano para férias_
