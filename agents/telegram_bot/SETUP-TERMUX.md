# 📱 Como rodar o Telegram Bot no celular (Termux)

## Setup Inicial (só na primeira vez)

### 1. Instale o Termux
Baixe na [Google Play](https://play.google.com/store/apps/details?id=com.termux) ou [F-Droid](https://f-droid.org/pt-BR/packages/com.termux/)

### 2. Configure o Termux
Abra o Termux e execute:

```bash
# Atualizar pacotes
pkg update && pkg upgrade -y

# Instalar Python e Git
pkg install python git -y

# Permitir acesso ao armazenamento
termux-setup-storage
```

### 3. Clone o projeto (se ainda não tem)
```bash
cd ~/storage/downloads
git clone https://github.com/cleiton-negreiros/opb-sistema.git
cd opb-sistema
```

### 4. Instale as dependências Python
```bash
pip install python-telegram-bot requests jinja2
```

### 5. Inicie o bot
```bash
bash bot-telegram-termux.sh
```

Ou diretamente:
```bash
cd ~/storage/downloads/opb-sistema
python agents/telegram_bot/main.py
```

---

## Criar Atalho na Tela Inicial (sem root)

### Opção A: Usando o aplicativo "Shortcut Maker"
1. Instale [Shortcut Maker](https://play.google.com/store/apps/details?id=com.mbm.ShortcutMaker)
2. Abra o app
3. Selecione **"Activity"**
4. Procure por **"Termux"** na lista
5. Selecione **"com.termux/.app.TermuxActivity"**
6. No campo de argumentos, coloque:
   ```
   -e "cd ~/storage/downloads/opb-sistema && bash bot-telegram-termux.sh"
   ```
7. Nomeie como **"🤖 NegreirosBot"**
8. Toque em **Criar**

### Opção B: Widget Termux (root)
```bash
# Requer root
pkg install termux-widget
# Depois crie um widget na home
```

### Opção C: Script + Widget simples
Crie o arquivo `~/storage/downloads/opb-sistema/abrir-bot.sh`:
```bash
#!/bin/bash
am start --user 0 -a android.intent.action.MAIN -n com.termux/.app.TermuxActivity -d "https://termux.com"
sleep 2
echo "cd ~/storage/downloads/opb-sistema && python agents/telegram_bot/main.py" > ~/.termux_last_cmd
```

---

## Manter o bot rodando em segundo plano

```bash
# Iniciar em background (nohup)
cd ~/storage/downloads/opb-sistema
nohup python agents/telegram_bot/main.py > ~/bot-log.txt 2>&1 &

# Verificar se está rodando
ps aux | grep python

# Ver logs
tail -f ~/bot-log.txt

# Parar o bot
pkill -f "python agents/telegram_bot/main.py"
```

---

## Solução de Problemas

| Problema | Solução |
|----------|---------|
| `ModuleNotFoundError: telegram` | `pip install python-telegram-bot` |
| `Permission denied` | `chmod +x bot-telegram-termux.sh` |
| Token expirado | Gere novo token no [@BotFather](https://t.me/BotFather) |
| Bot não responde | Verifique se o telefone está conectado à internet |

---

_Last updated: 2026-05-14_