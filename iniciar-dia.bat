@echo off
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║          INICIANDO DIA - OPB Sistema                         ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo [1/3] Carregando contexto do cerebro...
python morning_routine.py

echo.
echo [2/3] Verificando agentes...
dir agents\* /b /ad 2>nul

echo.
echo [3/3] Configuracoes:
echo.
echo   Para iniciar o Telegram Bot:
echo   python agents\telegram_bot\main.py
echo.
echo   Para acessar o Hub:
echo   http://localhost:8088/hub.html
echo.
echo   Deploy: https://opb-sistema.vercel.app
echo.
echo ═══════════════════════════════════════════════════════════════
echo   Dia iniciado! Bom trabalho!
echo ═══════════════════════════════════════════════════════════════
echo.

pause