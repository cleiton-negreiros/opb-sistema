#!/bin/bash
# ============================================
# 🔧 Diagnóstico OPB Sistema - Termux
# Execute este script para identificar problemas
# ============================================

echo "🔧 DIAGNÓSTICO OPB SISTEMA"
echo "=========================="
echo ""

# 1. Verificar Termux
echo "1️⃣  Termux:"
echo "   Versão: $(termux-info 2>/dev/null | grep -i version | head -1 || echo 'N/A')"
echo "   Python: $(python --version 2>&1)"
echo "   Bash: $(bash --version | head -1)"
echo ""

# 2. Verificar permissões
echo "2️⃣  Permissões:"
if [ -d "$HOME/storage" ]; then
    echo "   ✅ storage/ existe"
    ls -la $HOME/storage/ 2>/dev/null | head -5
else
    echo "   ❌ storage/ NÃO existe"
    echo "   💡 Execute: termux-setup-storage"
fi
echo ""

# 3. Verificar projeto
echo "3️⃣  Projeto:"
POSSIVEIS=(
    "$HOME/storage/downloads/opb-sistema"
    "$HOME/Documents/opb-sistema"
    "$HOME/opb-sistema"
    "/sdcard/Download/opb-sistema"
)

for p in "${POSSIVEIS[@]}"; do
    if [ -d "$p" ]; then
        echo "   ✅ Encontrado: $p"
        echo "   Arquivos: $(ls "$p" | wc -l)"
        echo "   Permissões: $(ls -ld "$p" | awk '{print $1}')"
        PROJETO="$p"
        break
    fi
done

if [ -z "$PROJETO" ]; then
    echo "   ❌ Projeto NÃO encontrado!"
    echo "   💡 Copie para: ~/storage/downloads/opb-sistema"
fi
echo ""

# 4. Verificar dependências
echo "4️⃣  Dependências Python:"
if python -c "import flask" 2>/dev/null; then
    echo "   ✅ Flask instalado"
else
    echo "   ❌ Flask NÃO instalado"
    echo "   💡 Execute: pip install flask flask-cors"
fi

if python -c "import flask_cors" 2>/dev/null; then
    echo "   ✅ Flask-CORS instalado"
else
    echo "   ❌ Flask-CORS NÃO instalado"
fi
echo ""

# 5. Verificar porta 5000
echo "5️⃣  Porta 5000:"
if curl -s -o /dev/null --connect-timeout 1 http://localhost:5000/ 2>/dev/null; then
    echo "   ⚠️  Porta 5000 em uso (API respondendo)"
else
    echo "   ✅ Porta 5000 livre"
fi
echo ""

# 6. Verificar processos
echo "6️⃣  Processos OPB:"
if pgrep -f "api_server.py" >/dev/null; then
    echo "   ⚠️  API já rodando (PID: $(pgrep -f api_server.py))"
else
    echo "   ✅ API não está rodando"
fi

if pgrep -f "telegram_bot" >/dev/null; then
    echo "   ⚠️  Bot já rodando (PID: $(pgrep -f telegram_bot))"
else
    echo "   ✅ Bot não está rodando"
fi
echo ""

# 7. Testar API (se estiver rodando)
echo "7️⃣  Teste de conexão:"
if command -v curl &>/dev/null; then
    HTTP=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 2 http://localhost:5000/ 2>/dev/null)
    if [ "$HTTP" = "200" ]; then
        echo "   ✅ API respondendo (HTTP $HTTP)"
    elif [ "$HTTP" = "000" ]; then
        echo "   ❌ API não está rodando"
    else
        echo "   ⚠️  API respondendo com HTTP $HTTP"
    fi
else
    echo "   ⚠️  curl não instalado"
fi
echo ""

# 8. Verificar logs
echo "8️⃣  Logs recentes:"
if [ -f /tmp/opb-api.log ]; then
    echo "   📋 Últimas 10 linhas do log:"
    tail -10 /tmp/opb-api.log
else
    echo "   ℹ️  Nenhum log encontrado"
fi
echo ""

# 9. Verificar git status
if [ -n "$PROJETO" ] && [ -d "$PROJETO/.git" ]; then
    echo "9️⃣  Git status:"
    cd "$PROJETO"
    echo "   Branch: $(git branch --show-current 2>/dev/null || echo 'N/A')"
    echo "   Status: $(git status --short | wc -l) alterações"
    if [ $(git status --short | wc -l) -gt 0 ]; then
        git status --short | head -5
    fi
    
    # Verificar se há arquivos não sincronizados
    echo ""
    echo "   🔄 Último commit: $(git log --oneline -1 2>/dev/null || echo 'N/A')"
fi
echo ""

echo "=========================="
echo "💡 Para corrigir problemas comuns:"
echo "   1. termux-setup-storage"
echo "   2. pip install flask flask-cors"
echo "   3. git pull (na pasta do projeto)"
echo "   4. bash termux.sh"
echo ""
echo "📋 Cole este output no suporte para ajuda!"
