#!/bin/bash
# ============================================
# setup-mobile.sh — Configura Obsidian + Sync no Termux
# ============================================
# Uso: bash setup-mobile.sh
# ============================================

set -e

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; RED='\033[0;31m'; NC='\033[0m'
BOLD='\033[1m'

echo -e "${CYAN}============================================${NC}"
echo -e "${BOLD}  📱 Setup Mobile — OPB + Obsidian${NC}"
echo -e "${CYAN}============================================${NC}"
echo ""

# 1) Verificar Termux
if [ ! -d "$HOME" ]; then
    echo -e "${RED}Erro: Parece que nao esta no Termux.${NC}"
    echo "Este script e para Android (Termux)."
    exit 1
fi
echo -e "${GREEN}[OK] Termux detectado${NC}"

# 2) Verificar/storage
if [ ! -d "$HOME/storage/shared" ]; then
    echo -e "${YELLOW}Configurando acesso ao storage...${NC}"
    termux-setup-storage
    echo -e "${YELLOW}⚠️  Permissao concedida? (s/n)${NC}"
    read -r resp
    if [ "$resp" != "s" ]; then
        echo -e "${RED}Sem permissao. Rode manualmente: termux-setup-storage${NC}"
        exit 1
    fi
fi
echo -e "${GREEN}[OK] Storage acessivel${NC}"

# 3) Instalar dependencias
echo -e "${CYAN}Instalando dependencias...${NC}"
pkg update -y
pkg install -y git openssh curl
echo -e "${GREEN}[OK] Dependencias instaladas${NC}"

# 4) Configurar git
git config --global user.email "cleiton.negreiros@gmail.com"
git config --global user.name "cleiton-negreiros"
echo -e "${GREEN}[OK] Git configurado${NC}"

# 5) Clonar repositorio
OBSIDIAN_VAULT="$HOME/storage/shared/Obsidian/opb-sistema"
if [ -d "$OBSIDIAN_VAULT/.git" ]; then
    echo -e "${YELLOW}Repositorio ja existe. Atualizando...${NC}"
    cd "$OBSIDIAN_VAULT"
    git pull
else
    echo -e "${CYAN}Clonando repositorio em:${NC}"
    echo "  $OBSIDIAN_VAULT"
    mkdir -p "$(dirname "$OBSIDIAN_VAULT")"
    git clone https://github.com/cleiton-negreiros/opb-sistema.git "$OBSIDIAN_VAULT"
fi
echo -e "${GREEN}[OK] Repositorio clonado${NC}"

# 6) Link sync-safe no PATH
mkdir -p "$HOME/.opb-bin"
if [ -f "$OBSIDIAN_VAULT/sync-safe.sh" ]; then
    cp "$OBSIDIAN_VAULT/sync-safe.sh" "$HOME/.opb-bin/sync-safe"
    chmod +x "$HOME/.opb-bin/sync-safe"
fi

# Criar alias permanente
if ! grep -q "opb-sync" "$HOME/.bashrc" 2>/dev/null; then
    echo "alias opb-sync='bash $HOME/.opb-bin/sync-safe'" >> "$HOME/.bashrc"
    echo "alias opb-vault='cd $OBSIDIAN_VAULT'" >> "$HOME/.bashrc"
fi
source "$HOME/.bashrc"

echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${BOLD}  ✅ Setup concluido!${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""
echo "📱 Agora va para o Obsidian no celular:"
echo "   1. Abra o Obsidian"
echo "   2. 'Open folder as vault'"
echo "   3. Navegue ate: Internal Storage/Obsidian/opb-sistema"
echo "   4. Selecione a pasta"
echo ""
echo "🔄 Para sincronizar manualmente:"
echo "   termux:~$ opb-sync"
echo ""
echo "📂 Para ir ate a pasta:"
echo "   termux:~$ opb-vault"
echo ""
echo "📱 Para sincronizar rapidamente:"
echo "   Crie um Widget do Termux com:"
echo "   bash ~/.opb-bin/sync-safe"
echo ""
echo -e "${YELLOW}⚠️  Configure o token do GitHub na primeira sync:${NC}"
echo "   Rode: opb-sync"
echo "   (ou: bash \$HOME/.opb-bin/sync-safe)"
echo ""
