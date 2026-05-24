@echo off
chcp 65001 >nul 2>&1
title OPB - Configurar Inicializacao Automatica
cd /d "%~dp0"

echo ========================================
echo  OPB Sistema - Startup Automatizado
echo ========================================
echo.
echo Isso vai registrar o OPB para iniciar
iniciar automaticamente quando voce ligar o PC.
echo.
echo Escolha o modo:
echo   1) Ao fazer login (recomendado)
echo   2) Ao ligar o PC (requer admin)
echo.
choice /c 12 /n /m "Modo (1/2): "
if errorlevel 2 goto system
if errorlevel 1 goto user

:user
echo.
echo --- Registrando tarefa no Agendador (login do usuario) ---

schtasks /create /tn "OPB-Startup" /tr "\"%~dp0iniciar-startup.bat\"" /sc onlogon /rl highest /f /it

if %errorlevel% equ 0 (
    echo ✅ Tarefa "OPB-Startup" criada com sucesso!
    echo    Executa ao fazer login no Windows.
) else (
    echo ❌ Erro ao criar tarefa. Tente executar como Administrador.
)
goto fim

:system
echo.
echo --- Registrando tarefa no Agendador (inicializacao do sistema) ---

schtasks /create /tn "OPB-Startup" /tr "\"%~dp0iniciar-startup.bat\"" /sc onstart /rl highest /f

if %errorlevel% equ 0 (
    echo ✅ Tarefa "OPB-Startup" criada com sucesso!
    echo    Executa ao ligar o PC (antes do login).
) else (
    echo ❌ Erro ao criar tarefa. Execute como Administrador.
)
goto fim

:fim
echo.
echo ========================================
echo  Para remover futuramente:
echo    schtasks /delete /tn "OPB-Startup" /f
echo ========================================
echo.
echo Pressione qualquer tecla para sair...
pause > nul
