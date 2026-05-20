# Guia de Instalação — Paz na Conta

> Sistema de Agentes IA para Mentoria de Finanças Católicas
> Versão 2.0 | Última atualização: 2026-05-20

---

## 🖥️ PC — Windows

### Requisitos
- Windows 10 ou 11
- Python 3.10+ (https://python.org/downloads)
- 4GB RAM mínimo, 8GB recomendado
- 2GB de espaço em disco

### Passo a Passo

**1. Instalar Python**
- Baixe em https://python.org/downloads
- Na instalação, marque ✅ **"Add Python to PATH"**
- Clique em "Install Now"

**2. Verificar instalação**
```cmd
python --version
pip --version
```

**3. Baixar o projeto**
- Opção A (Git): `git clone https://github.com/cleiton-negreiros/opb-sistema.git`
- Opção B (ZIP): Baixe em https://github.com/cleiton-negreiros/opb-sistema/archive/main.zip e extraia

**4. Instalar dependências**
```cmd
cd opb-sistema
pip install -r requirements.txt
```

**5. Iniciar o sistema**
```cmd
iniciar-dia.bat
```

**6. Acessar**
- Landing Page: http://localhost:5000
- Plataforma: http://localhost:5000/plataforma.html
- PWA Mobile: http://localhost:5000/dashboard.html

---

## 🍎 PC — macOS

### Requisitos
- macOS 12+ (Monterey ou superior)
- Python 3.10+ (https://python.org/downloads)
- 4GB RAM mínimo, 8GB recomendado
- 2GB de espaço em disco

### Passo a Passo

**1. Instalar Python**
```bash
# Via Homebrew (recomendado)
brew install python

# Ou baixe em https://python.org/downloads
```

**2. Verificar instalação**
```bash
python3 --version
pip3 --version
```

**3. Baixar o projeto**
```bash
git clone https://github.com/cleiton-negreiros/opb-sistema.git
cd opb-sistema
```

**4. Instalar dependências**
```bash
pip3 install -r requirements.txt
```

**5. Iniciar o sistema**
```bash
python3 api_server.py &
sleep 3
open http://localhost:5000
```

**6. Acessar**
- Landing Page: http://localhost:5000
- Plataforma: http://localhost:5000/plataforma.html
- PWA Mobile: http://localhost:5000/dashboard.html

---

## 🤖 Celular — Android (Termux)

### Requisitos
- Android 8+
- App Termux (https://f-droid.org/packages/com.termux/)
- 3GB RAM mínimo
- 2GB de espaço interno

### Passo a Passo

**1. Instalar Termux**
- Baixe do F-Droid (NÃO da Play Store — versão desatualizada)
- Link: https://f-droid.org/packages/com.termux/

**2. Abrir Termux e instalar pacotes**
```bash
pkg update -y
pkg install python git clang -y
```

**3. Dar acesso aos arquivos**
```bash
termux-setup-storage
```

**4. Baixar o projeto**
```bash
cd ~/storage/downloads
git clone https://github.com/cleiton-negreiros/opb-sistema.git
cd opb-sistema
```

**5. Instalar dependências**
```bash
pip install flask flask-cors python-telegram-bot requests jinja2 markdown
```

**6. Iniciar o sistema**
```bash
bash termux.sh
```
Escolha opção **1** (Iniciar Tudo)

**7. Acessar**
- Abra o navegador: http://localhost:5000
- Ou instale como app: aparece banner "Instalar OPB Studio"

**8. Instalar como App (PWA)**
- No Chrome: Menu (⋮) → "Adicionar à tela inicial"
- O app aparece na home como um app nativo

---

## 🍎 Celular — iOS (iPhone/iPad)

### Requisitos
- iOS 16+
- App a-Shell (https://apps.apple.com/app/a-shell/id1473805438)
- 3GB RAM mínimo

### Passo a Passo

**1. Instalar a-Shell**
- App Store → procure "a-Shell"
- Ou use o app "Pyto" (pago, mas mais completo)

**2. Instalar Python packages**
```bash
pip install flask flask-cors requests jinja2 markdown
```

**3. Baixar o projeto**
- No Safari: https://github.com/cleiton-negreiros/opb-sistema
- Baixe o ZIP e extraia em "Arquivos"

**4. Iniciar o servidor**
```bash
cd ~/Documents/opb-sistema
python api_server.py
```

**5. Acessar**
- Abra Safari: http://localhost:5000

**6. Instalar como App (PWA)**
- No Safari: Compartilhar → "Adicionar à Tela de Início"
- O app aparece na home como um app nativo

---

## 📱 Instalar como App (PWA) — Todos os dispositivos

### Chrome (Android/PC)
1. Acesse http://localhost:5000/dashboard.html
2. Menu (⋮) → "Instalar app" ou "Adicionar à tela inicial"
3. Confirme a instalação

### Safari (iPhone/iPad)
1. Acesse http://localhost:5000/dashboard.html
2. Compartilhar (⬆️) → "Adicionar à Tela de Início"
3. Nomeie e confirme

### Edge (PC)
1. Acesse http://localhost:5000/dashboard.html
2. Ícone de instalação na barra de endereço
3. Clique em "Instalar"

---

## ❌ Problemas Comuns

### "python não é reconhecido" (Windows)
- Reinstale Python marcando "Add to PATH"
- Ou use `py` no lugar de `python`

### "Port 5000 já em uso"
- Feche outros programas usando a porta 5000
- Ou edite `api_server.py` e mude `PORT = 5000` para outro número

### "ModuleNotFoundError" (celular)
```bash
pip install flask flask-cors python-telegram-bot requests jinja2 markdown
```

### "git clone falhou"
- Verifique a conexão com internet
- Ou baixe o ZIP: https://github.com/cleiton-negreiros/opb-sistema/archive/main.zip

### App PWA não instala
- Use Chrome (Android) ou Safari (iOS) — outros navegadores não suportam PWA
- Verifique se está acessando via `http://localhost:5000` (não `127.0.0.1`)

---

## 📞 Suporte

- Instagram: @paznaconta
- Email: contato@paznaconta.com
- Telegram: @NegreirosBot (comando /help)
