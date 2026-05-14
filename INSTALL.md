# OPB Sistema - Guia de Instalação

## Requisitos

- Python 3.8+ 
- Windows 10/11 (ou Linux/Mac com ajustes)
- [Ollama](https://ollama.ai) (opcional - o sistema funciona em modo fallback sem IA)

## Instalação em Novo Computador

### Passo 1: Clonar o Projeto
```bash
git clone https://github.com/cleiton-negreiros/opb-sistema.git
cd opb-sistema
```

### Passo 2: Executar Instalação
```bash
setup.bat
```

Isso vai:
- Atualizar pip
- Instalar dependências (Flask, Telegram Bot, etc)
- Verificar Ollama
- Configurar token do Telegram (se desejado)

### Passo 3: Iniciar o Sistema
```bash
iniciar.bat
```

O script vai:
- Iniciar o servidor API na porta 5000
- Abrir a plataforma no navegador

---

## Configuração do Telegram Bot (Opcional)

1. Crie um bot via @BotFather no Telegram
2. Copie o token fornecido
3. Configure no Windows:
   ```cmd
   setx TELEGRAM_BOT_TOKEN "SEU_TOKEN_AQUI"
   ```
4. Reinicie o terminal

---

## Configuração do Ollama (Opcional)

Para ter geração de IA real:

1. Instale Ollama: https://ollama.ai
2. Execute no terminal:
   ```bash
   ollama pull tinyllama
   ollama list
   ```

---

## Estrutura de Arquivos

```
opb-sistema/
├── setup.bat           # Script de instalação
├── iniciar.bat         # Inicia o sistema
├── api_server.py       # Servidor Flask (API + Frontend)
├── requirements.txt    # Dependências Python
├── cerebro/            # Cérebro (documentação)
├── agents/             # Agentes Python
├── utils/              # Utilitários
└── cerebro/perfil-empreendedor-solo/
    ├── plataforma.html # Dashboard principal
    └── formulario.html # Formulário de perfil
```

---

## Acesso

- **Plataforma Web:** http://localhost:5000
- **API Health:** http://localhost:5000/api/health
- **Stats:** http://localhost:5000/api/stats

---

## Deploy no Vercel (Frontend apenas)

```bash
vercel --prod
```

Nota: O backend Flask não funciona no Vercel. Use localmente ou em servidor próprio.

---

## Solução de Problemas

### "Porta 5000 já em uso"
```cmd
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### "Module not found"
```bash
pip install -r requirements.txt
```

### Ollama não responde
O sistema会自动 usa fallback (respostas mock) quando Ollama indisponível.

---

_Última atualização: 2026-05-13_