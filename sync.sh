#!/bin/bash
# ============================================
# Sincronizar OPB Sistema - Termux
# ============================================

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; RED='\033[0;31m'; NC='\033[0m'

cd "$(dirname "$0")" || { echo -e "${RED}Erro ao entrar no diretorio${NC}"; exit 1; }

# Garante config minima do git
git config --global user.email "cleiton.negreiros@gmail.com" 2>/dev/null
git config --global user.name "cleiton-negreiros" 2>/dev/null
git config --global --add safe.directory "$(pwd)" 2>/dev/null

# Usa credential store persistente (se ja configurou token antes)
if [ -f "$HOME/.opb-git-credentials" ]; then
    git config --global credential.helper "store --file $HOME/.opb-git-credentials" 2>/dev/null
else
    # Fallback: cache com 1h de timeout
    git config --global credential.helper "cache --timeout=3600" 2>/dev/null
fi

encerrar() { echo -e "\n${GREEN}Concluido!${NC}"; read -p "Pressione ENTER para voltar..."; }

menu() {
    while true; do
        clear
        echo -e "${CYAN}============================================"
        echo "   Sincronizar OPB Sistema - Termux"
        echo -e "============================================${NC}"
        echo ""
        echo "  $(pwd)"
        echo ""
        echo -e "  ${CYAN}1)${NC} Enviar (commit + push)"
        echo -e "  ${CYAN}2)${NC} Receber (pull)"
        echo -e "  ${CYAN}3)${NC} Enviar + Receber"
        echo -e "  ${CYAN}t)${NC} Configurar token GitHub"
        echo -e "  ${CYAN}0)${NC} Sair"
        echo ""
        read -p "  Escolha: " opt
        case "$opt" in
            1) enviar;;
            2) receber;;
            3) enviar; receber;;
            t|T) configurar_token;;
            0) exit 0;;
            *) echo -e "${RED}Opcao invalida${NC}"; sleep 1;;
        esac
    done
}

enviar() {
    echo -e "\n${YELLOW}Enviando alteracoes para GitHub...${NC}"

    # Verifica se ha algo pra commit
    if git diff --quiet && git diff --cached --quiet && test -z "$(git ls-files --others --exclude-standard)"; then
        echo -e "${YELLOW}Nada novo para commitar.${NC}"
        encerrar
        return
    fi

    git add -A
    git commit -m "sync: Atualizacao $(date '+%Y-%m-%d %H:%M')" || {
        echo -e "${YELLOW}Nada para commitar (ou commit falhou)${NC}"
        encerrar
        return
    }
    if git push; then
        echo -e "${GREEN}Enviado com sucesso!${NC}"
    else
        echo -e "${RED}Falha ao enviar.${NC}"
        echo -e "${YELLOW}Possiveis causas:${NC}"
        echo "  1. Token expirou - use a opcao 't' para configurar novamente"
        echo "  2. Sem internet"
        echo "  3. Conflito - tente 'Receber' primeiro"
    fi
    encerrar
}

receber() {
    echo -e "\n${YELLOW}Recebendo alteracoes do GitHub...${NC}"

    # Guarda modificacoes locais antes do pull
    HAS_STASH=false
    if ! git diff --quiet || ! git diff --cached --quiet; then
        echo -e "${CYAN}Salvando alteracoes locais temporariamente...${NC}"
        git stash push -m "sync-stash-$(date '+%Y%m%d%H%M%S')"
        HAS_STASH=true
    fi

    if git pull --rebase; then
        echo -e "${GREEN}Recebido com sucesso!${NC}"
        # Restaura alteracoes locais se foram guardadas
        if $HAS_STASH; then
            echo -e "${CYAN}Restaurando alteracoes locais...${NC}"
            if git stash pop; then
                echo -e "${GREEN}Alteracoes locais restauradas.${NC}"
            else
                echo -e "${YELLOW}Alteracoes locais guardadas em stash. Para recuperar: git stash pop${NC}"
            fi
        fi
    else
        echo -e "${RED}Falha ao receber.${NC}"
        if $HAS_STASH; then
            echo -e "${YELLOW}Alteracoes locais estao guardadas em stash.${NC}"
            echo -e "  Para recuperar: git stash pop"
            echo -e "  Para ver: git stash list"
        fi
    fi
    encerrar
}

configurar_token() {
    echo -e "\n${YELLOW}Configurar GitHub Token${NC}"
    echo -e "${CYAN}Como gerar um token:${NC}"
    echo "  1. Va em https://github.com/settings/tokens"
    echo "  2. Clique 'Generate new token (classic)'"
    echo "  3. Marque 'repo' e 'workflow'"
    echo "  4. Gere e copie o token"
    echo ""
    echo -e "${CYAN}Cole o token abaixo (nao vai aparecer enquanto digita):${NC}"
    read -s token
    echo ""
    if [ -n "$token" ]; then
        # Salva token em arquivo (formato git credential-store)
        echo "https://cleiton-negreiros:${token}@github.com" > "$HOME/.opb-git-credentials"
        chmod 600 "$HOME/.opb-git-credentials"
        # Configura o git para usar o token via arquivo
        git config --global credential.helper "store --file $HOME/.opb-git-credentials" 2>/dev/null
        echo -e "${GREEN}Token configurado! Tente enviar novamente.${NC}"
    else
        echo -e "${RED}Token vazio. Nada alterado.${NC}"
    fi
    encerrar
}

# Verifica se ha config de email/nome
CURRENT_EMAIL=$(git config user.email)
if [ "$CURRENT_EMAIL" = "u0_a90@localhost" ] || [ "$CURRENT_EMAIL" = "" ]; then
    echo -e "${YELLOW}Aviso: git user.email nao configurado. Configure com:${NC}"
    echo '  git config --global user.email "seu@email.com"'
    echo '  git config --global user.name "Seu Nome"'
fi

menu
