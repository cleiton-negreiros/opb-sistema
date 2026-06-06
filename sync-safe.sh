#!/bin/bash
# ============================================
# sync-safe.sh — Sincronização SEGURA OPB (Termux)
# Um único comando. Faz backup, autentica, sincroniza.
#
# Uso: bash sync-safe.sh
# ============================================

set -e  # Para em qualquer erro (mas com mensagens claras)

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'
BOLD='\033[1m'

cd "$(dirname "$0")" || { echo -e "${RED}Erro ao entrar no diretorio${NC}"; exit 1; }

# Garante config minima
git config --global user.email "cleiton.negreiros@gmail.com" 2>/dev/null
git config --global user.name "cleiton-negreiros" 2>/dev/null
git config --global --add safe.directory "$(pwd)" 2>/dev/null

echo -e "${CYAN}============================================${NC}"
echo -e "${BOLD}  🔄 Sync Seguro — OPB Sistema (Termux)${NC}"
echo -e "${CYAN}============================================${NC}"
echo ""

# ============================================
# 1) BACKUP DO PERFIL (sempre, antes de tudo)
# ============================================
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="$HOME/.opb-backups/perfil_$TIMESTAMP"
mkdir -p "$BACKUP_DIR"
if [ -d "perfil" ]; then
    cp -r perfil/ "$BACKUP_DIR/"
    echo -e "${GREEN}✅ Backup do perfil salvo em:${NC}"
    echo -e "   $BACKUP_DIR"
    echo -e "   ${CYAN}(seguro mesmo se algo der errado abaixo)${NC}"
else
    echo -e "${YELLOW}⚠️  Pasta 'perfil/' nao encontrada. Backup ignorado.${NC}"
fi
echo ""

# ============================================
# 2) CONFIGURAR TOKEN (se necessario)
# ============================================
if [ ! -f "$HOME/.opb-git-credentials" ] || [ ! -s "$HOME/.opb-git-credentials" ]; then
    echo -e "${YELLOW}🔑 Token GitHub nao configurado. Vamos configurar agora.${NC}"
    echo -e "${CYAN}Como gerar um token:${NC}"
    echo "  1. Va em https://github.com/settings/tokens"
    echo "  2. 'Generate new token (classic)'"
    echo "  3. Marque 'repo' e 'workflow'"
    echo "  4. Copie o token gerado"
    echo ""
    echo -e "${CYAN}Cole o token abaixo (nao vai aparecer enquanto digita):${NC}"
    read -s token
    echo ""
    if [ -z "$token" ]; then
        echo -e "${RED}❌ Token vazio. Abortando.${NC}"
        exit 1
    fi
    echo "https://cleiton-negreiros:${token}@github.com" > "$HOME/.opb-git-credentials"
    chmod 600 "$HOME/.opb-git-credentials"
    git config --global credential.helper "store --file $HOME/.opb-git-credentials" 2>/dev/null
    echo -e "${GREEN}✅ Token configurado!${NC}"
    echo ""
else
    echo -e "${GREEN}🔑 Token ja configurado em ~/.opb-git-credentials${NC}"
    git config --global credential.helper "store --file $HOME/.opb-git-credentials" 2>/dev/null
    echo ""
fi

# ============================================
# 3) VERIFICAR ESTADO vs REMOTO
# ============================================
echo -e "${CYAN}📡 Verificando conexao com GitHub...${NC}"
if ! git fetch origin 2>/dev/null; then
    echo -e "${RED}❌ Nao consegui falar com o GitHub. Verifique sua internet.${NC}"
    echo -e "${YELLOW}   Se o token estiver expirado, apague ~/.opb-git-credentials e rode de novo:${NC}"
    echo "   rm ~/.opb-git-credentials && bash sync-safe.sh"
    exit 1
fi
echo -e "${GREEN}✅ Conectado${NC}"
echo ""

LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/master)
BASE=$(git merge-base HEAD origin/master 2>/dev/null || echo "")

echo "📊 Estado:"
echo "   Local:  $(git log -1 --format='%h %s' HEAD)"
echo "   Remoto: $(git log -1 --format='%h %s' origin/master)"
echo ""

# Caso 1: sem divergencia
if [ "$LOCAL" = "$REMOTE" ]; then
    echo -e "${GREEN}✅ Sincronizado. Nada a fazer.${NC}"
    exit 0
fi

# Caso 2: local atras do remoto (apenas pull)
AHEAD=$(git rev-list --count origin/master ^HEAD)
BEHIND=$(git rev-list --count HEAD ^origin/master)

if [ "$AHEAD" -gt 0 ] && [ "$BEHIND" -eq 0 ]; then
    echo -e "${YELLOW}📥 Voce esta $AHEAD commit(s) atras. Puxando do PC...${NC}"
    git pull --rebase
    echo -e "${GREEN}✅ Atualizado!${NC}"
    exit 0
fi

# Caso 3: divergencia (local tem commits proprio E remoto tem commits que faltam)
if [ "$AHEAD" -gt 0 ] && [ "$BEHIND" -gt 0 ]; then
    echo -e "${YELLOW}⚠️  DIVERGENCIA DETECTADA${NC}"
    echo "   Seu celular tem: $BEHIND commit(s) proprio(s) (suas anotacoes)"
    echo "   O PC enviou:     $AHEAD commit(s) novo(s)"
    echo ""
    echo -e "${CYAN}Vamos fazer MERGE (preserva tudo das duas partes).${NC}"
    echo ""

    # Guardar mudancas locais em stash temporario (caso tenha working tree sujo)
    HAS_STASH=false
    if ! git diff --quiet || ! git diff --cached --quiet; then
        echo "💾 Salvando alteracoes locais nao commitadas..."
        git stash push -m "sync-safe-stash-$TIMESTAMP"
        HAS_STASH=true
    fi

    # Tentar merge
    if git merge origin/master --no-edit; then
        echo -e "${GREEN}✅ Merge feito com sucesso!${NC}"
    else
        echo ""
        echo -e "${RED}❌ Conflito no merge (provavelmente em perfil/PERFIL.md).${NC}"
        echo ""
        echo "Arquivos em conflito:"
        git diff --name-only --diff-filter=U
        echo ""
        echo -e "${CYAN}📋 O que fazer:${NC}"
        echo "  1. Abra cada arquivo em conflito no editor (vim/nano/IDE)"
        echo "  2. Procure por marcadores <<<<<<< ======= >>>>>>>"
        echo "  3. Escolha: manter SUA versao OU a do PC OU mesclar"
        echo "  4. Apos resolver, rode:"
        echo "     git add <arquivo>"
        echo "     git commit -m 'merge: resolucao de conflito'"
        echo "     git push origin master"
        echo ""
        echo -e "${YELLOW}Seu backup esta em: $BACKUP_DIR${NC}"
        echo -e "${YELLOW}Suas alteracoes locais estao em: git stash list${NC}"
        echo "  Para recupera-las depois do merge: git stash pop"
        exit 1
    fi

    # Restaurar stash se houve
    if [ "$HAS_STASH" = true ]; then
        echo "📦 Restaurando alteracoes locais..."
        if git stash pop 2>/dev/null; then
            echo -e "${GREEN}✅ Alteracoes locais restauradas${NC}"
        else
            echo -e "${YELLOW}⚠️  Conflito ao restaurar stash. Rode: git stash pop${NC}"
        fi
    fi
fi

# ============================================
# 4) PUSH
# ============================================
echo ""
echo -e "${CYAN}📤 Enviando tudo para GitHub...${NC}"
if git push origin master; then
    echo -e "${GREEN}✅ Sincronizado!${NC}"
    echo ""
    echo "📊 Estado final:"
    git log --oneline -3
else
    echo -e "${RED}❌ Push falhou.${NC}"
    echo -e "${YELLOW}Possiveis causas: token expirou, conflito de push, sem internet.${NC}"
    echo "  Tente: rm ~/.opb-git-credentials && bash sync-safe.sh"
    exit 1
fi
