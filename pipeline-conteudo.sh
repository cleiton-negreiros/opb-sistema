#!/bin/bash
# ============================================
# pipeline-conteudo.sh — Pipeline de Conteudo Diario (Termux/Linux)
# Uso: bash pipeline-conteudo.sh [arquivo_ideia]
# Se sem argumento, pega o arquivo mais recente de:
#   _conteudo/email-diario/ > inbox/ > acervo/ideias/
# ============================================

set -e

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; RED='\033[0;31m'; NC='\033[0m'
BOLD='\033[1m'

cd "$(dirname "$0")"

IDEIA="$1"

if [ -z "$IDEIA" ]; then
    IDEIA=$(ls -t _conteudo/email-diario/*.md 2>/dev/null | head -1)
    if [ -z "$IDEIA" ]; then
        IDEIA=$(ls -t inbox/*.md 2>/dev/null | head -1)
    fi
    if [ -z "$IDEIA" ]; then
        IDEIA=$(ls -t acervo/ideias/*.md 2>/dev/null | head -1)
    fi
    if [ -z "$IDEIA" ]; then
        echo -e "${RED}Nenhum arquivo encontrado${NC}"
        exit 1
    fi
fi

ABSOLUTE_PATH="$(pwd)/$IDEIA"

echo -e "${CYAN}============================================${NC}"
echo -e "${BOLD}  📦 Pipeline de Conteudo Diario${NC}"
echo -e "${CYAN}============================================${NC}"
echo ""
echo -e "Ideia: ${YELLOW}$IDEIA${NC}"
echo ""

# Garante pastas _conteudo
mkdir -p _conteudo/carrossel _conteudo/reels _conteudo/video

# 1) Gerar Carrossel
echo -e "[1/4] ${CYAN}🎠 Gerando Carrossel...${NC}"
python agents/carrossel/main.py --ideia "$ABSOLUTE_PATH" --tipo educacional --formato carrossel --exportar
CAR_FILE=$(ls -t acervo/carrossel/*.md 2>/dev/null | head -1)
if [ -n "$CAR_FILE" ]; then
    cp "$CAR_FILE" _conteudo/carrossel/
    echo -e "${GREEN}  ✅ Carrossel gerado!${NC}"
fi
echo ""

# 2) Gerar Reels Script
echo -e "[2/4] ${CYAN}📱 Gerando roteiro Reels...${NC}"
python agents/reels_script/main.py "$IDEIA" --ideia "$ABSOLUTE_PATH" --duracao 60 --formato reels --exportar
REEL_FILE=$(ls -t acervo/ideias/script_*.txt 2>/dev/null | head -1)
if [ -n "$REEL_FILE" ]; then
    cp "$REEL_FILE" _conteudo/reels/
    echo -e "${GREEN}  ✅ Reels gerado!${NC}"
fi
echo ""

# 3) Gerar Video 10min
echo -e "[3/4] ${CYAN}🎬 Gerando roteiro Video Semanal...${NC}"
python agents/video_10min/main.py --ideia "$ABSOLUTE_PATH" --exportar
VID_FILE=$(ls -t acervo/video/*.txt 2>/dev/null | head -1)
if [ -n "$VID_FILE" ]; then
    cp "$VID_FILE" _conteudo/video/
    echo -e "${GREEN}  ✅ Video gerado!${NC}"
fi
echo ""

# 4) Gerar Post Instagram
echo -e "[4/4] ${CYAN}📝 Gerando Post Instagram...${NC}"
python agents/text_generator/main.py "$IDEIA" educational --perfil paz-na-conta
echo -e "${GREEN}  ✅ Post gerado!${NC}"
echo ""

echo -e "${GREEN}============================================${NC}"
echo -e "${BOLD}  ✅ Pipeline Concluido!${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""
echo "📂 Outputs (Obsidian):"
echo "  📧 Email original: _conteudo/email-diario/"
echo "  🎠 Carrossel:      _conteudo/carrossel/"
echo "  📱 Reels:          _conteudo/reels/"
echo "  🎬 Video 10min:    _conteudo/video/"
echo "  ✅ Publicar em:    _conteudo/publicados/"
echo ""
echo "🔗 Abra _home.md no Obsidian para ver tudo."
echo ""
