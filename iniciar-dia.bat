@echo off
chcp 65001 >nul 2>&1
echo.
echo ===== INICIANDO DIA - OPB Sistema =====
echo.

cd /d "%~dp0"

echo [1/6] Carregando contexto do cerebro...
python morning_routine.py

echo.
echo [2/6] Iniciando Servidor Flask (API)...
start python api_server.py

echo.
timeout /t 3 /nobreak > nul

echo [3/6] Iniciando Telegram Bot...
start cmd /c python agents\telegram_bot\main.py

echo.
timeout /t 2 /nobreak > nul

echo [4/6] Executando Radagast (curadoria)...
start cmd /c python agents\radagast\radagast.py --dry-run

echo.
timeout /t 2 /nobreak > nul

echo [5/6] Abrindo Plataforma no navegador...
start http://localhost:5000

echo.
echo [6/6] Verificando agentes...
dir agents\* /b /ad 2>nul

echo.
echo ========================================
echo   SISTEMA INICIADO:
echo   - Plataforma: http://localhost:5000
echo   - Telegram:   @NegreirosBot
echo   Envie /start ou /iniciar no Telegram
echo ========================================
echo.
echo Pressione qualquer tecla para sair...
pause > nul