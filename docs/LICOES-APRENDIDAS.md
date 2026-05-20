# Lições Aprendidas — OPB Sistema

> Última atualização: 2026-05-20

---

## Bugs Corrigidos

### 1. `js/api.js` — Missing closing brace
**Problema:** Função `apiCall` sem `}` de fechamento.
**Sintoma:** `Uncaught SyntaxError: await is only valid in async functions`
**Correção:** Adicionado `}` antes de `escapeHtml`.
**Lição:** Sempre verificar balanceamento de braces após edições.

### 2. `dashboard.html` — Link para plataforma
**Problema:** Link "Plataforma" apontava para `/` (landing page).
**Correção:** Mudado para `/plataforma.html` em 2 lugares (href + função `abrirPlataforma()`).
**Lição:** Service worker cacheia versões antigas — sempre bump cache version.

### 3. `sw.js` — Cache stale
**Problema:** Service worker servia versão antiga do dashboard.
**Correção:** Bump de `opb-studio-v1` para `opb-studio-v2`.
**Lição:** Sempre atualizar versão do cache quando mudar HTML/JS.

### 4. `auth.html` — Extensão de navegador
**Problema:** Erro `A listener indicated an asynchronous response...` no console.
**Causa:** Extensão do navegador (password manager, adblock).
**Solução:** Não é bug do código — ignorar ou testar em aba anônima.
**Lição:** Nem todo erro no console é do seu código.

### 5. `api_server.py` — `sys.stdout.reconfigure()` no Termux
**Problema:** API não inicia no Termux (Android).
**Causa:** `sys.stdout.reconfigure()` pode falhar em terminais Android.
**Correção:** Envolver em `try/except`.
**Lição:** Sempre tratar encoding com fallback para mobile/Termux.

### 6. Telegram Bot — Conflict error
**Problema:** `Conflict: terminated by other getUpdates request`
**Causa:** Múltiplas instâncias do bot com mesmo token.
**Correção:** `pkill -f "python.*telegram_bot"` antes de iniciar.
**Lição:** Sempre matar processos antigos antes de iniciar bot.

### 7. Auth desabilitado temporariamente
**Problema:** Login bloqueava acesso durante desenvolvimento.
**Solução:** `AUTH_ENABLED = False` + comentários nos redirects.
**Lição:** Manter feature flags para habilitar/desabilitar funcionalidades.

---

## Progresso do Projeto

### ✅ Concluído
- [x] Sistema de autenticação (login/registro/logout)
- [x] Multi-tenant (isolamento de dados por usuário)
- [x] Onboarding flow (3 passos)
- [x] Validação de inputs + rate limiting
- [x] Guia de instalação (Windows, Mac, Android, iOS)
- [x] API documentation (`docs/API.md`)
- [x] Manual do usuário (`docs/MANUAL.md`)
- [x] Landing page responsiva
- [x] Plataforma SPA com 17 páginas
- [x] PWA mobile instalável
- [x] Telegram bot com comandos
- [x] Termux menu interativo
- [x] Sync PC-Celular via Git
- [x] Tema claro/escuro
- [x] Deploy Vercel

### 🔄 Em Progresso
- [ ] Performance (lazy loading, code splitting)
- [ ] Loading states + skeleton screens
- [ ] Analytics dashboard para mentor
- [ ] Testes automatizados
- [ ] Notificações push

### 📋 Backlog
- [ ] Tela de login/registro (reabilitar auth)
- [ ] Pagamento/planos (Stripe, Mercado Pago)
- [ ] Notificações por email
- [ ] Backup automático
- [ ] Docker compose para deploy fácil
- [ ] Documentação de contribuição

---

## Comandos Úteis

### PC (Windows)
```powershell
cd C:\Users\cleit\Desktop\opb-sistema
python api_server.py
# ou
iniciar-dia.bat
```

### Termux (Android)
```bash
cd ~/storage/downloads/opb-sistema
git pull
pip install flask flask-cors python-telegram-bot requests jinja2 markdown
bash termux.sh
# Opção 2 (só API) ou 1 (API + Bot)
```

### Debug no Termux
```bash
# Ver log da API
cat /tmp/opb-api.log

# Ver se API está rodando
curl -s http://localhost:5000/api/health

# Matar processos
pkill -f "python.*api_server"
pkill -f "python.*telegram_bot"

# Rodar API diretamente para ver erro
cd ~/storage/downloads/opb-sistema
python api_server.py
```

### Sync PC → Celular
```bash
# No PC
cd C:\Users\cleit\Desktop\opb-sistema
git add -A
git commit -m "sync"
git push

# No celular
cd ~/storage/downloads/opb-sistema
git pull
```

### Deploy Vercel
```bash
cd C:\Users\cleit\Desktop\opb-sistema
vercel --prod
```

---

## Arquitetura Atual

```
opb-sistema/
├── api_server.py          # Flask API (porta 5000)
├── auth.py                # Autenticação SQLite
├── validation.py          # Validação de inputs
├── termux.sh              # Menu Android
├── sync.sh / sync.bat     # Sync Git
├── iniciar-dia.bat        # Rotina matinal PC
│
├── cerebro/perfil-empreendedor-solo/
│   ├── landing.html       # Página de vendas
│   ├── plataforma.html    # App SPA (17 páginas)
│   ├── auth.html          # Login/Registro
│   ├── onboarding.html    # Wizard 3 passos
│   ├── dashboard.html     # PWA mobile
│   ├── manifest.json      # PWA manifest
│   ├── sw.js              # Service worker
│   ├── js/                # Módulos JS
│   └── styles/            # CSS
│
├── agents/                # Agentes IA
│   ├── telegram_bot/      # Bot Telegram
│   ├── carrossel/         # Gerador de carrossel
│   ├── text_generator/    # Gerador de posts
│   ├── transcricao/       # Transcrição YouTube
│   ├── consumo/           # Processamento de conteúdo
│   ├── posicionamento/    # Análise de posicionamento
│   ├── radagast/          # Curadoria de conteúdo
│   ├── narvi/             # Editor de vídeo
│   └── quadro-de-avisos/  # Sistema de tarefas
│
├── docs/
│   ├── API.md             # Documentação da API
│   └── MANUAL.md          # Manual do usuário
│
└── GUIA-INSTALACAO.md     # Guia de instalação
```

---

## Decisões de Design

1. **Flask sobre FastAPI** — Flask já estava no projeto, menor curva de aprendizado
2. **SQLite sobre PostgreSQL** — Local-first, sem dependência externa
3. **File-based storage** — Simples, versionável com Git, fácil backup
4. **PWA sobre app nativo** — Um código, todos os dispositivos
5. **Ollama sobre APIs pagas** — Custo zero, privacidade total
6. **Git para sync** — Já usado pelo projeto, sem necessidade de servidor adicional
7. **Auth desabilitado temporariamente** — Para desenvolvimento rápido, reabilitar antes de lançar

---

## Notas para o Futuro

- **Reabilitar auth:** Mudar `AUTH_ENABLED = False` para `True` em `api_server.py` e descomentar os redirects em `js/app.js` e `onboarding.html`
- **Termux:** Sempre usar `try/except` em `sys.stdout.reconfigure()` e `sys.stderr.reconfigure()`
- **Service Worker:** Sempre bump versão do cache quando mudar HTML/JS
- **Telegram Bot:** Sempre matar instâncias antigas antes de iniciar novo bot
- **Vercel:** Deploy estático serve frontend, API só roda localmente
