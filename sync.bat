@echo off
chcp 65001 >nul
title Sincronizar OPB - PC

:menu
cls
echo ============================================
echo   🔄 Sincronizar OPB Sistema — PC
echo ============================================
echo.
echo  1) 📤 Enviar (commit + push) — PC ^> GitHub
echo  2) 📥 Receber (pull) — GitHub ^> PC
echo  3) 🔄 Enviar + Receber
echo  4) ❌ Sair
echo.
set /p opt="  Escolha: "

if "%opt%"=="1" goto enviar
if "%opt%"=="2" goto receber
if "%opt%"=="3" goto completar
if "%opt%"=="4" exit /b

echo Opção inválida & timeout /t 2 >nul & goto menu

:enviar
cls
echo 📤 Enviando alterações para o GitHub...
cd /d "%~dp0"
git add -A
git commit -m "sync: Atualizacao %DATE% %TIME%"
git push
if %errorlevel% equ 0 (echo ✅ Enviado!) else (echo ⚠️ Nada novo ou erro)
timeout /t 3 >nul
goto menu

:receber
cls
echo 📥 Recebendo alterações do GitHub...
cd /d "%~dp0"
git pull
echo ✅ Recebido!
timeout /t 3 >nul
goto menu

:completar
cls
echo 🔄 Sincronização completa...
cd /d "%~dp0"
git add -A
git commit -m "sync: Atualizacao %DATE% %TIME%"
git push
git pull
echo ✅ Sincronizado!
timeout /t 3 >nul
goto menu
