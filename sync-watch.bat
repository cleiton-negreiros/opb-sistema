@echo off
chcp 65001 >nul
title 🔄 Auto-Sync OPB + Obsidian

cd /d "%~dp0"

:MENU
cls
echo ╔══════════════════════════════════════════════════════╗
echo ║      🔄 Auto-Sync OPB Sistema + Obsidian            ║
echo ╚══════════════════════════════════════════════════════╝
echo.
echo  1) ▶ Iniciar Watch (auto-sync a cada 2min)
echo  2) ⏹ Parar Watch
echo  3) 📤 Sincronizar Agora
echo  4) 📥 Receber do GitHub
echo  5) ❌ Sair
echo.

set /p opt="  Escolha: "

if "%opt%"=="1" goto start_watch
if "%opt%"=="2" goto stop_watch
if "%opt%"=="3" goto sync_now
if "%opt%"=="4" goto pull_now
if "%opt%"=="5" exit /b
echo Opcao invalida & timeout /t 2 >nul & goto MENU

:start_watch
cls
echo ▶ Iniciando watch (auto-sync a cada 2 minutos)...
echo   Pressione qualquer tecla para parar.
echo.
echo   🔍 Observando: acervo\ideias\ inbox\ _templates\
echo.

:WATCH_LOOP
call :sync_now_silent
echo %TIME% - Sync automático concluído
choice /t 120 /d s /n /m "  Proximo sync em 2min (S)air (P)arar..." >nul
if errorlevel 2 goto MENU
if errorlevel 1 goto WATCH_LOOP

:stop_watch
cls
echo ⏹ Watch parado.
timeout /t 2 >nul
goto MENU

:sync_now
cls
echo 📤 Sincronizando...
call :sync_now_silent
echo ✅ Concluido!
timeout /t 3 >nul
goto MENU

:pull_now
cls
echo 📥 Recebendo do GitHub...
git pull
echo ✅ Recebido!
timeout /t 3 >nul
goto MENU

:sync_now_silent
git add -A 2>nul
git diff --cached --quiet 2>nul
if errorlevel 1 (
    git commit -m "sync: Obsidian %DATE% %TIME%" >nul 2>nul
    git push >nul 2>nul
)
exit /b
