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

# ============================================
# 0) MOVER SELF PARA ~/.opb-bin/ (se baixado via curl)
# ============================================
# Quando o usuario roda `curl ... sync-safe.sh && bash sync-safe.sh`,
# o arquivo fica untracked na working tree. Se a gente tentar
# `git pull`/`git merge` depois, o git recusa sobrescrever untracked
# ("would be overwritten by merge"). Solucao: mover o script para um
# diretorio fora do repo e remover da working tree. O bash ja carregou
# o script em memoria, entao a execucao continua normal.
SELF_PATH="$HOME/.opb-bin/sync-safe"
mkdir -p "$HOME/.opb-bin"
if [ -f "sync-safe.sh" ]; then
    if [ -f "$SELF_PATH" ]; then
        # Ja existe versao instalada — mantem a do curl (mais nova)
        cp sync-safe.sh "$SELF_PATH"
    else
        cp sync-safe.sh "$SELF_PATH"
    fi
    chmod +x "$SELF_PATH"
    rm -f sync-safe.sh
    echo "📦 sync-safe.sh movido para $SELF_PATH (working tree limpa pro merge)"
    echo "   Para re-rodar depois: bash $SELF_PATH  (ou re-curl do GitHub)"
    echo ""
fi

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

# Pre-flight: mover arquivos untracked que seriam sobrescritos pelo pull/merge
UNTRACKED_STASH=$(mktemp -d /tmp/.opb-untracked.XXXXXX)
MOVED=()
while read -r f; do
    [ -z "$f" ] && continue
    if git cat-file -e "origin/master:${f}" 2>/dev/null; then
        mkdir -p "$UNTRACKED_STASH/$(dirname "$f")"
        cp -r "$f" "$UNTRACKED_STASH/$f"
        rm -rf "$f"
        MOVED+=("$f")
    fi
done < <(git ls-files --others --exclude-standard)

if [ ${#MOVED[@]} -gt 0 ]; then
    echo "💾 Movi ${#MOVED[@]} arquivo(s) untracked pra nao bloquear o pull/merge:"
    for f in "${MOVED[@]}"; do
        echo "   - $f  →  $UNTRACKED_STASH/$f"
    done
    echo "   (restaurado no fim se tudo der certo)"
    echo ""
fi

if [ "$AHEAD" -gt 0 ] && [ "$BEHIND" -eq 0 ]; then
    echo -e "${YELLOW}📥 Voce esta $AHEAD commit(s) atras. Puxando do PC...${NC}"
    git pull --rebase
    echo -e "${GREEN}✅ Atualizado!${NC}"

    # Restaurar arquivos movidos
    if [ -d "$UNTRACKED_STASH" ] && [ -n "$(ls -A "$UNTRACKED_STASH" 2>/dev/null)" ]; then
        cp -r "$UNTRACKED_STASH"/. . 2>/dev/null
        rm -rf "$UNTRACKED_STASH"
        echo "✅ Arquivos untracked restaurados"
    fi
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
        # Diferenciar 2 cenarios de erro:
        # A) "untracked working tree files would be overwritten by merge" — working tree suja
        # B) "CONFLICT (...)" — conflito de conteudo (ex: perfil/PERFIL.md)
        UNTRACKED_BLOCKED=$(git status --porcelain | grep '^??' | awk '{print $2}' | while read f; do
            if git cat-file -e "origin/master:${f}" 2>/dev/null; then echo "$f"; fi
        done)
        CONFLICTED=$(git diff --name-only --diff-filter=U)

        if [ -n "$UNTRACKED_BLOCKED" ]; then
            echo -e "${RED}❌ Working tree tem arquivos untracked que serao sobrescritos pelo merge.${NC}"
            echo ""
            echo "Arquivos bloqueando:"
            for f in $UNTRACKED_BLOCKED; do
                echo "  - $f"
            done
            echo ""
            echo -e "${CYAN}📋 O que fazer (escolha 1):${NC}"
            echo "  a) Mover manualmente e re-rodar:"
            echo "     mkdir -p /tmp/opb-stash && mv sync-safe.sh /tmp/opb-stash/  # (exemplo)"
            echo "     bash $SELF_PATH"
            echo ""
            echo "  b) Limpar tudo (CUIDADO: apaga arquivos nao commitados):"
            echo "     git clean -fd  # pergunta antes de cada arquivo"
            echo "     bash $SELF_PATH"
            echo ""
        fi

        if [ -n "$CONFLICTED" ]; then
            echo -e "${RED}❌ Conflito de CONTEUDO no merge.${NC}"
            echo ""
            echo "Arquivos em conflito:"
            echo "$CONFLICTED"
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
        fi

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

    # Restaurar arquivos untracked movidos no pre-flight
    if [ -d "$UNTRACKED_STASH" ] && [ -n "$(ls -A "$UNTRACKED_STASH" 2>/dev/null)" ]; then
        cp -r "$UNTRACKED_STASH"/. . 2>/dev/null
        rm -rf "$UNTRACKED_STASH"
        echo "✅ Arquivos untracked restaurados"
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
