@echo off
title OPB Sistema
cd /d "%~dp0"
echo ==========================================
echo    OPB - Sistema de Produtividade
echo ==========================================
echo.
echo Iniciando servidor...
echo Abra: http://localhost:8088
echo.
echo Pressione Ctrl+C para parar
echo ==========================================
python server.py
