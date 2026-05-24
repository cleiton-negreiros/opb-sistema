@echo off
chcp 65001 >nul 2>&1
echo.
echo ===== INICIANDO DIA - OPB Sistema =====
echo.

cd /d "%~dp0"

:: ── Sincronizar com GitHub ──
echo [0/7] Sincronizar com GitHub?
echo   (S) Sim - Enviar alteracoes locais primeiro
echo   (N) Nao - Pular sync
echo   (R) Receber - Baixar do celular primeiro
echo.
choice /c SNR /n /m "Escolha (S/N/R): "
if errorlevel 3 goto receber
if errorlevel 2 goto iniciar
if errorlevel 1 goto enviar
goto iniciar

:enviar
echo.
echo --- Enviando alteracoes para GitHub...
git add -A
git commit -m "sync: Atualizacao PC %DATE% %TIME%"
git push
echo --- Sync enviado!
goto iniciar

:receber
echo.
echo --- Recebendo alteracoes do GitHub...
git pull
echo --- Sync recebido!
goto iniciar

:iniciar
echo.

echo [1/7] Auditoria de codigo + Contexto do cerebro...
python morning_routine.py

echo.
echo [2/7] Iniciando Servidor Flask (API)...
start python api_server.py

echo.
timeout /t 3 /nobreak > nul

echo [3/7] Iniciando Telegram Bot...
start cmd /c python agents\telegram_bot\main.py

echo.
timeout /t 2 /nobreak > nul

echo [4/7] Executando Radagast (curadoria)...
start cmd /c python agents\radagast\radagast.py --dry-run

echo.
timeout /t 2 /nobreak > nul

echo [5/7] Abrindo Plataforma no navegador...
start http://localhost:5000

echo.
echo [6/7] Abrindo Painel PWA...
start http://localhost:5000/dashboard.html

echo.
echo [7/7] Verificando agentes...
dir agents\* /b /ad 2>nul

echo.
echo ========================================
echo   SISTEMA INICIADO:
echo   - Plataforma: http://localhost:5000
echo   - Painel PWA: http://localhost:5000/dashboard.html
echo   - Telegram:   @NegreirosBot
echo   Envie /start ou /iniciar no Telegram
echo ========================================
echo.
echo Pressione qualquer tecla para sair...
pause > nul