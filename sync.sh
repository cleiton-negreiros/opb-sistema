#!/bin/bash
# ============================================
# ðŸ”„ Sincronizar OPB Sistema â€” Termux
# ============================================

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

# Vai pra pasta do projeto
cd "$(dirname "$0")" || {
    echo -e "${RED}âŒ Erro ao entrar no diretÃ³rio${NC}"
    exit 1
}

# Cache do git (evita pedir usuario/senha toda vez)
git config --global credential.helper cache 2>/dev/null

encerrar() {
    echo -e "\n${GREEN}âœ… ConcluÃ­do!${NC}"
    read -p "Pressione ENTER para voltar..."
}

menu() {
    clear
    echo -e "${CYAN}============================================"
    echo "   ðŸ”„ Sincronizar OPB Sistema â€” Termux"
    echo -e "============================================${NC}"
    echo ""
    echo "  ðŸ“ $(pwd)"
    echo ""
    echo -e "  ${CYAN}1)${NC} ðŸ“¤ Enviar (commit + push) â€” Celular > GitHub"
    echo -e "  ${CYAN}2)${NC} ðŸ“¥ Receber (pull) â€” GitHub > Celular"
    echo -e "  ${CYAN}3)${NC} ðŸ”„ Enviar + Receber"
    echo -e "  ${CYAN}0)${NC} âŒ Sair"
    echo ""
    read -p "  Escolha: " opt

    case "$opt" in
        1) enviar ;;
        2) receber ;;
        3) enviar; receber ;;
        0) exit 0 ;;
        *) echo -e "${RED}OpÃ§Ã£o invÃ¡lida${NC}"; sleep 1; menu ;;
    esac
}

enviar() {
    echo -e "\n${YELLOW}ðŸ“¤ Enviando alteraÃ§Ãµes para GitHub...${NC}"
    git add -A
    git commit -m "sync: Atualizacao $(date '+%Y-%m-%d %H:%M')"
    if git push; then
        echo -e "${GREEN}âœ… Enviado!${NC}"
    else
        echo -e "${YELLOW}âš ï¸  Nada novo ou erro de conexÃ£o${NC}"
    fi
    encerrar
}

receber() {
    echo -e "\n${YELLOW}ðŸ“¥ Recebendo alteraÃ§Ãµes do GitHub...${NC}"
    if git pull; then
        echo -e "${GREEN}âœ… Recebido!${NC}"
    else
        echo -e "${RED}âŒ Erro ao receber. Verifique conexÃ£o ou conflitos.${NC}"
    fi
    encerrar
}

# Garantir linha segura pro git
git config --global --add safe.directory "$(pwd)" 2>/dev/null

menu
