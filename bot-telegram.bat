@echo off
chcp 65001 >nul
title 🤖 NegreirosBot - OPB Sistema
color 0A
cls

echo ============================================
echo   🤖 NEGREIROSBOT - OPB Sistema
echo   Telegram Bot - Agente de Captura
echo ============================================
echo.

cd /d "%~dp0"
cd ..

echo 📁 Projeto: %CD%
echo.

echo 🔧 Verificando dependencias...
pip install python-telegram-bot requests jinja2 >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️  Falha ao instalar dependencias. Tentando novamente...
    pip install python-telegram-bot requests jinja2
)
echo.

echo 🟢 Iniciando o Telegram Bot...
echo 💬 Envie /start no Telegram para interagir
echo.
echo    (Pressione Ctrl+C para parar o bot)
echo ============================================
echo.

python agents\telegram_bot\main.py

echo.
echo ============================================
echo   Bot encerrado.
echo ============================================
pause