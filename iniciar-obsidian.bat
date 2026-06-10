@echo off
chcp 65001 >nul
title 🚀 Iniciar OPB + Obsidian

cd /d "%~dp0"

echo ╔══════════════════════════════════════════════════════╗
echo ║     🚀 Iniciar OPB Sistema + Obsidian               ║
echo ╚══════════════════════════════════════════════════════╝
echo.

:: 1) Puxar atualizacoes do GitHub
echo [1/4] 📥 Sincronizando com GitHub...
git pull
echo.

:: 2) Abrir Obsidian com o vault
echo [2/4] 🔗 Abrindo Obsidian...
if exist "%LOCALAPPDATA%\obsidian\Obsidian.exe" (
    start "" "%LOCALAPPDATA%\obsidian\Obsidian.exe" "%CD%"
    echo   Obsidian aberto!
) else (
    echo   [AVISO] Obsidian nao encontrado em %LOCALAPPDATA%\obsidian\
)
echo.

:: 3) Abrir a pasta inbox para captura rapida
echo [3/4] 📝 Abrindo inbox de ideias...
if exist "inbox\inbox.md" (
    start notepad "inbox\inbox.md" 2>nul
)
echo.

:: 4) Sugestao de sync
echo [4/4] ✅ Pronto!
echo.
echo 📌 Dicas:
echo   - Escreva ideias em inbox\inbox.md
echo   - Use _templates\idea.md para novas ideias
echo   - Para auto-sync: sync-watch.bat
echo   - Para sync manual: sync.bat
echo.

pause
