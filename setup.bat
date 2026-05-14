@echo off
echo ========================================
echo OPB Sistema - Instalacao
echo ========================================

echo.
echo [1/4] Atualizando pip...
python -m pip install --upgrade pip

echo.
echo [2/4] Instalando dependencias do Python...
pip install -r requirements.txt

echo.
echo [3/4] Verificando Ollama...
where ollama >nul 2>nul
if %errorlevel% neq 0 (
    echo AVISO: Ollama nao encontrado. Instale em: https://ollama.ai
    echo        O sistema funcionara em modo fallback.
) else (
    echo Ollama encontrado!
    ollama list
)

echo.
echo [4/4] Verificando Telegram Bot Token...
if defined TELEGRAM_BOT_TOKEN (
    echo Token do Telegram configurado!
) else (
    echo AVISO: TELEGRAM_BOT_TOKEN nao definido.
    echo Para definir: setx TELEGRAM_BOT_TOKEN "SEU_TOKEN_AQUI"
)

echo.
echo ========================================
echo Instalacao concluida!
echo ========================================
echo.
echo Para iniciar: executar "iniciar.bat"
echo.
pause