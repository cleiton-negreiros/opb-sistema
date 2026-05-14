@echo off
echo ========================================
echo OPB Sistema - Iniciando
echo ========================================

echo.
echo [1/4] Verificando Ollama...
where ollama >nul 2>nul
if %errorlevel% equ 0 (
    echo Ollama encontrado!
    ollama list
) else (
    echo AVISO: Ollama nao encontrado - modo fallback
)

echo.
echo [2/4] Iniciando Servidor API...
start "OPB API Server" cmd /c "cd /d %~dp0 && python api_server.py"

echo.
echo [3/4] Aguardando servidor iniciar...
timeout /t 5 /nobreak >nul

echo.
echo [4/4] Abrindo plataforma no navegador...
start http://localhost:5000

echo.
echo ========================================
echo Sistema iniciado com sucesso!
echo ========================================
echo.
echo PLATAFORMA: http://localhost:5000
echo API HEALTH:  http://localhost:5000/api/health
echo.
echo O servidor continuara rodando em background.
echo Para parar: feche a janela "OPB API Server"
echo.
echo Pressione qualquer tecla para abrir o navegador...
pause >nul
start http://localhost:5000