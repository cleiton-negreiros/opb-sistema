#!/bin/bash
# ============================================
# 🤖 NEGREIROSBOT - OPB Sistema
# Telegram Bot - Agente de Captura
# Para Termux (Android)
# ============================================

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

clear
echo -e "${GREEN}============================================"
echo "   🤖 NEGREIROSBOT - OPB Sistema"
echo "   Telegram Bot - Agente de Captura"
echo -e "============================================${NC}"
echo ""

# Ir para a pasta do projeto
# Ajuste o caminho abaixo se necessário
PROJETO="$HOME/storage/downloads/opb-sistema"

if [ ! -d "$PROJETO" ]; then
    echo -e "${YELLOW}⚠️  Projeto não encontrado em: $PROJETO"
    echo "Procurando em outros locais..."

    # Tentar localizar automaticamente
    POSSIVEIS=(
        "$HOME/storage/downloads/opb-sistema"
        "$HOME/Documents/opb-sistema"
        "$HOME/Desktop/opb-sistema"
        "$HOME/opb-sistema"
        "/sdcard/Download/opb-sistema"
        "/sdcard/Documents/opb-sistema"
        "/data/data/com.termux/files/home/opb-sistema"
    )

    for p in "${POSSIVEIS[@]}"; do
        if [ -d "$p" ]; then
            PROJETO="$p"
            echo -e "${GREEN}✅ Encontrado: $PROJETO${NC}"
            break
        fi
    done

    if [ ! -d "$PROJETO" ]; then
        echo -e "${RED}❌ Projeto não encontrado!${NC}"
        echo "Clone o projeto:"
        echo "  git clone https://github.com/cleiton-negreiros/opb-sistema.git"
        echo "  cd opb-sistema"
        exit 1
    fi
fi

echo -e "${CYAN}📁 Projeto: $PROJETO${NC}"
echo ""

# Instalar dependências se necessário
echo -e "${YELLOW}🔧 Verificando dependências...${NC}"
pip install python-telegram-bot requests jinja2 2>/dev/null
echo ""

# Iniciar o bot
echo -e "${GREEN}🟢 Iniciando o Telegram Bot...${NC}"
echo "💬 Envie /start no Telegram para interagir"
echo ""
echo -e "    (Pressione ${RED}Ctrl+C${NC} para parar o bot)"
echo "============================================"
echo ""

cd "$PROJETO"
python agents/telegram_bot/main.py

echo ""
echo "============================================"
echo "   Bot encerrado."
echo "============================================"