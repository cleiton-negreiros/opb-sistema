#!/bin/bash
# ============================================
# ðŸŽ¯ PAZ NA CONTA - OPB Sistema
# Menu Principal para Termux (Android)
# ============================================

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
PURPLE='\033[0;35m'
NC='\033[0m'
BOLD='\033[1m'

# Cache do diretÃ³rio do projeto
OPB_CACHE="$HOME/.cache/opb-dir"
mkdir -p "$HOME/.cache"

# ========== LOCALIZAR PROJETO ==========
find_project() {
    if [ -n "$OPB_PROJETO" ] && [ -d "$OPB_PROJETO" ]; then
        echo "$OPB_PROJETO"
        return
    fi

    if [ -f "$OPB_CACHE" ]; then
        cached=$(cat "$OPB_CACHE")
        if [ -d "$cached" ]; then
            echo "$cached"
            return
        fi
    fi

    POSSIVEIS=(
        "$HOME/storage/downloads/opb-sistema"
        "$HOME/Documents/opb-sistema"
        "$HOME/Desktop/opb-sistema"
        "$HOME/opb-sistema"
        "/sdcard/Download/opb-sistema"
        "/sdcard/Documents/opb-sistema"
        "/data/data/com.termux/files/home/opb-sistema"
        "$HOME/../storage/downloads/opb-sistema"
    )

    for p in "${POSSIVEIS[@]}"; do
        if [ -d "$p" ]; then
            echo "$p" > "$OPB_CACHE"
            echo "$p"
            return
        fi
    done

    echo ""
}

PROJETO=$(find_project)

# ========== UTILITÃRIOS ==========
check_api() {
    if command -v curl &> /dev/null; then
        curl -s -o /dev/null -w "%{http_code}" --connect-timeout 2 http://localhost:5000/ 2>/dev/null
    else
        echo "000"
    fi
}

check_port() {
    if command -v ss &> /dev/null; then
        ss -tlnp | grep -q ":$1 " && echo "ok" || echo "no"
    elif command -v netstat &> /dev/null; then
        netstat -tlnp 2>/dev/null | grep -q ":$1 " && echo "ok" || echo "no"
    else
        echo "unknown"
    fi
}

# ========== TELAS ==========
show_header() {
    clear
    echo -e "${GREEN}${BOLD}â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”${NC}"
    echo -e "${GREEN}${BOLD}â”‚  ðŸŽ¯ PAZ NA CONTA â€” OPB Sistema       â”‚${NC}"
    echo -e "${GREEN}${BOLD}â”‚  Menu Principal (Termux)             â”‚${NC}"
    echo -e "${GREEN}${BOLD}â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜${NC}"
    echo ""
    echo -e "${CYAN}ðŸ“ ${PROJETO:-âš ï¸  NÃ£o encontrado}${NC}"
    echo ""

    # Verificar serviÃ§os rodando
    API_STATUS=$(check_api)
    BOT_PID=$(pgrep -f "python.*telegram_bot/main.py" 2>/dev/null | head -1)

    echo -e "${BOLD}ðŸ“Š Status:${NC}"
    if [ "$API_STATUS" = "200" ]; then
        echo -e "  ${GREEN}âœ… API Server  (porta 5000)${NC}"
    elif [ "$API_STATUS" != "000" ]; then
        echo -e "  ${YELLOW}âš ï¸  API Server (HTTP $API_STATUS)${NC}"
    else
        echo -e "  ${RED}âŒ API Server  (parado)${NC}"
    fi

    if [ -n "$BOT_PID" ]; then
        echo -e "  ${GREEN}âœ… Telegram Bot (PID $BOT_PID)${NC}"
    else
        echo -e "  ${RED}âŒ Telegram Bot (parado)${NC}"
    fi
    echo ""
}

show_menu() {
    echo -e "${BOLD}ðŸš€ INICIAR SERVIÃ‡OS:${NC}"
    echo -e "  ${CYAN}1)${NC}  ðŸŽ¯ Iniciar TUDO (API + Bot)"
    echo -e "  ${CYAN}2)${NC}  ðŸŒ API Server + Plataforma Web"
    echo -e "  ${CYAN}3)${NC}  ðŸ¤– Telegram Bot"
    echo ""
    echo -e "${BOLD}ðŸ§  AGENTES (execuÃ§Ã£o Ãºnica):${NC}"
    echo -e "  ${CYAN}4)${NC}  ðŸ“¡ Radagast (curadoria automÃ¡tica)"
    echo -e "  ${CYAN}5)${NC}  ðŸŽ  Gerar Carrossel"
    echo -e "  ${CYAN}6)${NC}  âœï¸  Gerar Post para Instagram"
    echo ""
    echo -e "${BOLD}ðŸ“‹ FERRAMENTAS:${NC}"
    echo -e "  ${CYAN}7)${NC}  ðŸ“‹ Quadro de Avisos (tarefas)"
    echo -e "  ${CYAN}8)${NC}  ðŸ’¡ Ver Ãºltimas ideias"
    echo -e "  ${CYAN}9)${NC}  ðŸ“– Ver posicionamento/quem-sou"
    echo ""
    echo -e "${BOLD}âš™ï¸  SISTEMA:${NC}"
    echo -e "  ${CYAN}a)${NC}  ðŸ”„ Parar todos os serviÃ§os"
    echo -e "  ${CYAN}b)${NC}  ðŸ“± Abrir plataforma web (navegador)"
    echo -e "  ${CYAN}c)${NC}  ðŸ—‘ï¸  Limpar cache"
    echo -e "  ${CYAN}0)${NC}  âŒ Sair"
    echo -e "  ${CYAN}s)${NC}  🔄 Sincronizar com GitHub (sync.sh)"
    echo ""
}

# ========== AÃ‡Ã•ES ==========
start_api() {
    echo -e "\n${YELLOW}ðŸŒ Iniciando API Server...${NC}"
    cd "$PROJETO"
    python api_server.py &
    API_PID=$!
    echo "$API_PID" > /tmp/opb-api.pid
    sleep 2

    HTTP_STATUS=$(check_api)
    if [ "$HTTP_STATUS" = "200" ]; then
        echo -e "${GREEN}âœ… API rodando em http://localhost:5000${NC}"
    else
        echo -e "${YELLOW}âš ï¸  Aguardando API iniciar... (HTTP $HTTP_STATUS)${NC}"
    fi
    echo ""
}

start_bot() {
    echo -e "\n${YELLOW}ðŸ¤– Iniciando Telegram Bot...${NC}"
    cd "$PROJETO"
    python agents/telegram_bot/main.py &
    BOT_PID=$!
    echo "$BOT_PID" > /tmp/opb-bot.pid
    sleep 1
    echo -e "${GREEN}âœ… Bot iniciado (PID $BOT_PID)${NC}"
    echo -e "${CYAN}   Envie /start no Telegram para comeÃ§ar${NC}"
    echo ""
}

start_all() {
    start_api
    start_bot
    echo -e "${GREEN}â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”${NC}"
    echo -e "${GREEN}â”‚  ðŸŽ¯ Sistema completo iniciado!       â”‚${NC}"
    echo -e "${GREEN}â”‚  â€¢ API: http://localhost:5000         â”‚${NC}"
    echo -e "${GREEN}â”‚  â€¢ Bot: @NegreirosBot                 â”‚${NC}"
    echo -e "${GREEN}â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜${NC}"
    echo ""
}

run_radagast() {
    echo -e "\n${YELLOW}ðŸ“¡ Executando Radagast (curadoria)...${NC}"
    echo -e "   Isso pode levar 2-3 minutos...\n"
    cd "$PROJETO"
    python agents/radagast/radagast.py
    echo -e "\n${GREEN}âœ… Curadoria concluÃ­da!${NC}"
    read -p "Pressione ENTER para voltar..."
}

run_carrossel() {
    echo -e "\n${YELLOW}ðŸŽ  Gerar Carrossel${NC}"
    echo -e "${CYAN}Digite o tema (ex: DÃ­zimo e organizaÃ§Ã£o financeira):${NC} "
    read -r tema
    if [ -n "$tema" ]; then
        cd "$PROJETO"
        python agents/carrossel/main.py "$tema" "educational" "5"
    fi
    echo ""
    read -p "Pressione ENTER para voltar..."
}

run_texto() {
    echo -e "\n${YELLOW}âœï¸  Gerar Post para Instagram${NC}"
    echo -e "${CYAN}Digite o objetivo (ex: Como economizar no supermercado):${NC} "
    read -r objetivo
    if [ -n "$objetivo" ]; then
        cd "$PROJETO"
        python agents/text_generator/main.py "$objetivo" "educational"
    fi
    echo ""
    read -p "Pressione ENTER para voltar..."
}

show_quadro() {
    echo -e "\n${YELLOW}ðŸ“‹ Quadro de Avisos${NC}"
    cd "$PROJETO" 2>/dev/null

    python agents/quadro-de-avisos/main.py listar 2>/dev/null

    echo ""
    echo -e "${CYAN}OpÃ§Ãµes:${NC}"
    echo "  1) Adicionar tarefa"
    echo "  2) Concluir tarefa"
    echo "  3) Voltar"
    read -n1 -r -p "Escolha: " opt
    echo ""

    case "$opt" in
        1)
            echo ""
            echo -e "${CYAN}DescriÃ§Ã£o da tarefa:${NC} "
            read -r desc
            if [ -n "$desc" ]; then
                python agents/quadro-de-avisos/main.py adicionar "$desc"
            fi
            ;;
        2)
            echo ""
            echo -e "${CYAN}ID da tarefa para concluir:${NC} "
            read -r tid
            if [ -n "$tid" ]; then
                python agents/quadro-de-avisos/main.py concluir "$tid"
            fi
            ;;
    esac
    echo ""
    read -p "Pressione ENTER para voltar..."
}

show_ideias() {
    echo -e "\n${YELLOW}ðŸ’¡ Ãšltimas Ideias${NC}"
    cd "$PROJETO" 2>/dev/null

    if [ -d "acervo/ideias" ]; then
        echo ""
        for f in $(ls -t acervo/ideias/*.md 2>/dev/null | head -10); do
            nome=$(basename "$f" .md)
            echo "  â€¢ ${nome:0:60}"
        done
        echo ""
        echo -e "${CYAN}Total: $(ls acervo/ideias/*.md 2>/dev/null | wc -l) ideias${NC}"
    else
        echo -e "${YELLOW}Nenhuma ideia encontrada.${NC}"
    fi
    echo ""
    read -p "Pressione ENTER para voltar..."
}

show_posicionamento() {
    echo -e "\n${YELLOW}ðŸ“– Posicionamento${NC}"
    cd "$PROJETO" 2>/dev/null
    if [ -f "negocio/governanca/quem-sou.md" ]; then
        echo ""
        if grep -q "## Posicionamento" "negocio/governanca/quem-sou.md"; then
            sed -n '/## Posicionamento/,/^## /p' "negocio/governanca/quem-sou.md" | head -n -1
        else
            head -80 "negocio/governanca/quem-sou.md"
        fi
    else
        echo -e "${RED}Arquivo nÃ£o encontrado.${NC}"
    fi
    echo ""
    read -p "Pressione ENTER para voltar..."
}

stop_all() {
    echo -e "\n${YELLOW}ðŸ”„ Parando serviÃ§os...${NC}"

    if [ -f /tmp/opb-bot.pid ]; then
        kill $(cat /tmp/opb-bot.pid) 2>/dev/null
        rm -f /tmp/opb-bot.pid
        echo -e "  ${RED}â¹ï¸  Bot parado${NC}"
    fi

    if [ -f /tmp/opb-api.pid ]; then
        kill $(cat /tmp/opb-api.pid) 2>/dev/null
        rm -f /tmp/opb-api.pid
        echo -e "  ${RED}â¹ï¸  API parada${NC}"
    fi

    # Mata processos Ã³rfÃ£os
    pkill -f "python.*api_server.py" 2>/dev/null && echo -e "  ${RED}â¹ï¸  API (fallback)${NC}"
    pkill -f "python.*telegram_bot/main.py" 2>/dev/null && echo -e "  ${RED}â¹ï¸  Bot (fallback)${NC}"

    echo -e "\n${GREEN}âœ… Todos os serviÃ§os parados.${NC}"
    echo ""
    read -p "Pressione ENTER para voltar..."
}

open_web() {
    echo -e "\n${YELLOW}ðŸ“± Abrindo plataforma web...${NC}"
    HTTP_STATUS=$(check_api)
    if [ "$HTTP_STATUS" = "200" ]; then
        echo -e "${GREEN}âœ… API rodando â€” abrindo navegador...${NC}"
        termux-open-url "http://localhost:5000/" 2>/dev/null || \
        am start -a android.intent.action.VIEW -d "http://localhost:5000/" 2>/dev/null || \
        echo -e "${YELLOW}   Abra manualmente: http://localhost:5000/${NC}"
    else
        echo -e "${YELLOW}âš ï¸  API nÃ£o estÃ¡ rodando.${NC}"
        echo -e "   Inicie primeiro com a opÃ§Ã£o 1 ou 2."
    fi
    echo ""
    read -p "Pressione ENTER para voltar..."
}

clear_cache() {
    rm -f "$OPB_CACHE" /tmp/opb-*.pid 2>/dev/null
    echo -e "\n${GREEN}âœ… Cache limpo.${NC}"
    echo -e "${YELLOW}O diretÃ³rio serÃ¡ re-detectado na prÃ³xima execuÃ§Ã£o.${NC}"
    PROJETO=""
    echo ""
    read -p "Pressione ENTER para voltar..."
}

# ========== MAIN ==========
main() {
    while true; do
        # Re-detectar projeto se nÃ£o encontrado
        if [ -z "$PROJETO" ]; then
            PROJETO=$(find_project)
        fi

        show_header

        if [ -z "$PROJETO" ]; then
            echo -e "${RED}âŒ Projeto OPB Sistema nÃ£o encontrado!${NC}"
            echo -e "${YELLOW}   Certifique-se de que o projeto foi copiado para o celular.${NC}"
            echo -e "   Caminhos procurados:"
            echo -e "   â€¢ ~/storage/downloads/opb-sistema"
            echo -e "   â€¢ /sdcard/Download/opb-sistema"
            echo ""
            echo -e "${CYAN}   Para copiar do PC:${NC}"
            echo -e "   1. Conecte o cabo USB"
            echo -e "   2. Copie a pasta 'opb-sistema' para Downloads"
            echo -e "   3. Execute: termux-setup-storage"
            echo ""
            read -p "Pressione ENTER para tentar novamente..."
            PROJETO=$(find_project)
            continue
        fi

        show_menu
        read -n1 -r -p "ðŸ‘‰ Escolha uma opÃ§Ã£o: " opt
        echo ""

        case "$opt" in
            1) start_all ;;
            2) start_api ;;
            3) start_bot ;;
            4) run_radagast ;;
            5) run_carrossel ;;
            6) run_texto ;;
            7) show_quadro ;;
            8) show_ideias ;;
            9) show_posicionamento ;;
            a|A) stop_all ;;
            b|B) open_web ;;
            c|C) clear_cache ;;
            s|S) bash sync.sh ;;
            0)
                echo -e "\n${GREEN}ðŸ™ AtÃ© logo! Paz na Conta!${NC}"
                exit 0
                ;;
            *)
                echo -e "\n${RED}OpÃ§Ã£o invÃ¡lida!${NC}"
                sleep 1
                ;;
        esac
    done
}

main
