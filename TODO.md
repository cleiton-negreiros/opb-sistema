# TODO.md - OPB Sistema

> Quadro de tarefas atualizado em 2026-05-15

## ✅ Concluído

### Infraestrutura
- [x] Servidor Flask API (`api_server.py`) - 14+ endpoints REST
- [x] Telegram Bot integrado (NegreirosBot @NegreirosBot)
- [x] Ollama com tinyllama configurado
- [x] Deploy no Vercel (frontend estático): https://opb-sistema.vercel.app

### PWA Mobile
- [x] manifest.json com icons, shortcuts, orientação portrait
- [x] Service Worker (`sw.js`) para offline
- [x] Meta tags para Apple/Android
- [x] Plataforma responsiva (mobile-first)

### Setup para Outro Computador
- [x] setup.bat - Script de instalação
- [x] iniciar.bat - Script para iniciar sistema
- [x] requirements.txt - Dependências completas
- [x] INSTALL.md - Guia de instalação

### Agentes
- [x] Agente Carrossel (`agents/carrossel/`) - 4 tipos
- [x] Agente de Consumo (`agents/consumo/`) - 5 tipos de análise
- [x] Agente Text Generator
- [x] Agente Transcrição
- [x] Agente Posicionamento
- [x] Agente Narvi (`agents/narvi/`) - Editor de vídeo (requer FFmpeg)
- [x] Agente Radagast (`agents/radagast/`) - Curadoria de conteúdo EN

### Frontend
- [x] Plataforma Web (`plataforma.html`) - Dashboard completo
- [x] Formulário de Perfil (`formulario.html`) - 6 seções
- [x] Templates de Perfil (HABILIDADES, HISTORIAS, COSMOVISAO, PUBLICO-ALVO, POSICIONAMENTO, NARRATIVA)
- [x] Layout moderno com gradientes e glassmorphism (15/05/2026)

## 🔄 Em Progresso

- [ ] Preencher perfil do empreendedor com conteúdo real

## 🔧 Notas Técnicas
- Timeout Ollama: 180s (phi3:mini mais rápido que tinyllama)
- Modelo padrão: **phi3:mini** (2.2GB - funciona com ~3.4GB RAM)
- Modelos que NÃO funcionam: llama3 (~4.7GB), llama3.2-vision (~7.8GB)
- Scoop instalado: use `scoop install ffmpeg` para Narvi

### Correções Realizadas (15/05/2026)
- server.py: corrige path para servir plataforma.html corretamente
- llm_provider.py: modelo padrão phi3:mini (funciona com RAM limitada)
- Layout plataforma.html: novo visual moderno com gradientes e glassmorphism
- Lições salvas em: `cerebro/negocio/governanca/licoes/2026-05.md`

## ⚙️ Agentes Integrados

### Narvi - Editor de Vídeo
- **Uso:** `python agents/narvi/narvi.py <video.mp4> [flags]`
- **Flags:** `--corte={brando|medio|agressivo}`, `--ratio={9x16|16x9|both}`, `--sample`
- **Dependência:** FFmpeg (`scoop install ffmpeg`)
- **Saída:** `~/Desktop/narvi-saida/<nome-video>/`

### Radagast - Curadoria de Conteúdo
- **Uso:** `python agents/radagast/radagast.py`
- **Configuração Obrigatória:**
  - `agents/radagast/.env` - API keys (Apify, Anthropic, Telegram)
  - `agents/radagast/config/keywords.json` - Termos de busca
  - `agents/radagast/config/inspiracoes.json` - Perfis para monitorar
- **Dependências:** API Apify, Anthropic API, Bot Telegram
- **Agendamento:** Executar diariamente (criar task manualmente)

## 📋 Próximos Passos

1. **Em outro computador:**
   ```bash
   git clone https://github.com/cleiton-negreiros/opb-sistema.git
   cd opb-sistema
   setup.bat
   iniciar.bat
   ```

2. **Usar no celular:**
   - Acesse https://opb-sistema.vercel.app
   - No iOS: Compartilhar > "Adicionar à Tela de Início"
   - No Android: Menu > "Instalar App" ou "Adicionar à tela inicial"

3. **Para ter API funcionando (localmente):**
   - O Flask server precisa rodar localmente
   - O Vercel serve apenas frontend estático

## 🚧 Blocked
- (none)

---

## 📁 Estrutura do Projeto

```
opb-sistema/
├── api_server.py          # Servidor Flask (rode localmente)
├── setup.bat              # Install dependencias
├── iniciar.bat            # Inicia sistema
├── requirements.txt       # Dependências Python
├── INSTALL.md            # Guia de instalação
├── vercel.json           # Config deploy
├── agents/               # Agentes Python
├── cerebro/perfil-empreendedor-solo/
│   ├── plataforma.html   # Dashboard PWA
│   ├── formulario.html   # Formulario PWA
│   ├── manifest.json     # PWA manifest
│   └── sw.js            # Service Worker
└── utils/                # Utilitários (llm_provider.py)
```

## 🔗 Links Úteis

- **Vercel:** https://opb-sistema.vercel.app
- **GitHub:** https://github.com/cleiton-negreiros/opb-sistema
- **API Local:** http://localhost:5000 (rode api_server.py)
- **Frontend:** http://localhost:8088 (rode server.py)

## 🚀 Como Usar

```bash
# Terminal 1 - API (porta 5000)
python api_server.py

# Terminal 2 - Frontend (porta 8088)
python server.py
```

Acesse:
- http://localhost:5000 → API + frontend completo
- http://localhost:8088/plataforma.html → apenas frontend (sem API)