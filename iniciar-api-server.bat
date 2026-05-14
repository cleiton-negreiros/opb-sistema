@echo off
chcp 65001 >nul
title OPB API Server - Plataforma Web
color 09
cls

echo ============================================
echo   OPB API Server
echo   Plataforma Web + Agentes
echo ============================================
echo.

cd /d "%~dp0"

echo 🔧 Verificando dependencias Python...
pip install flask flask-cors >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️ Erro ao instalar Flask. Tentando novamente...
    pip install flask flask-cors
)

echo ✅ Flask instalado com sucesso!
echo.
echo 🚀 Iniciando servidor...
echo 🌐 Acesse: http://localhost:5000
echo.
echo    (Pressione Ctrl+C para parar)
echo ============================================
echo.

python api_server.py

echo.
echo ============================================
echo   Servidor encerrado.
echo ============================================
pause