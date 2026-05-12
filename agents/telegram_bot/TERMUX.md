# Guia de Instalação - Termux (Android)

## Passos para rodar o bot no seu celular

### 1. Clone o projeto (se ainda não tem)

```bash
cd ~/storage/downloads
git clone https://github.com/cleiton-negreiros/opb-sistema.git
cd opb-sistema
```

### 2. Instale as dependências

```bash
pip install python-telegram-bot requests jinja2
```

### 3. Configure o token (opcional - já vem incluso)

```bash
export TELEGRAM_BOT_TOKEN="8789174206:AAEFbU9kz0PQQLFlCw4vMVzIYiXSnmVRjxQ"
```

### 4. Inicie o bot

```bash
cd agents/telegram_bot
python main.py
```

### 5. Use no Telegram

Abra o chat com seu bot e use os comandos:

- `/start` - Iniciar
- `/ideia [sua ideia]` - Cadastrar ideia
- `/listar` - Ver ideias
- `/status` - Ver status
- `/agents` - Ver agentes
- `/executar ls` - Testar comando

---

## Dica: Mantém o bot rodando

No Termux, use `nohup` para manter o bot ativo mesmo fechando o app:

```bash
nohup python main.py > bot.log 2>&1 &
```

Para ver logs:
```bash
tail -f bot.log
```

---

_Last updated: 2026-05-12_