@echo off
chcp 65001 >nul
title 📦 Pipeline de Conteudo — OPB Sistema

cd /d "%~dp0"

:: ============================================
:: Pipeline de Conteudo Diario
:: Uso: pipeline-conteudo.bat [arquivo_ideia]
:: Se sem argumento, pega o arquivo mais recente de inbox\
:: ============================================

set "IDEIA=%~1"

if "%IDEIA%"=="" (
    for /f "delims=" %%f in ('dir /b /o-d /a-d "inbox\*.md" 2^>nul') do (
        set "IDEIA=inbox\%%f"
        goto found
    )
    for /f "delims=" %%f in ('dir /b /o-d /a-d "acervo\ideias\*.md" 2^>nul') do (
        set "IDEIA=acervo\ideias\%%f"
        goto found
    )
    echo Nenhum arquivo encontrado em inbox\ ou acervo\ideias\
    pause
    exit /b 1
)

:found

echo ╔══════════════════════════════════════════════╗
echo ║     📦 Pipeline de Conteudo                  ║
echo ╚══════════════════════════════════════════════╝
echo.
echo Ideia: %IDEIA%
echo.

set "ABSOLUTE_PATH=%CD%\%IDEIA%"

:: 1) Gerar Carrossel
echo [1/4] 🎠 Gerando Carrossel...
python agents/carrossel/main.py --ideia "%ABSOLUTE_PATH%" --tipo educacional --formato carrossel --exportar
if %errorlevel% equ 0 (echo   ✅ Carrossel gerado!) else (echo   ⚠️ Falha no carrossel)
echo.

:: 2) Gerar Reels Script
echo [2/4] 📱 Gerando roteiro Reels...
python agents/reels_script/main.py --ideia "%ABSOLUTE_PATH%" --duracao 60 --formato reels --exportar
if %errorlevel% equ 0 (echo   ✅ Reels gerado!) else (echo   ⚠️ Falha no reels)
echo.

:: 3) Gerar Video 10min
echo [3/4] 🎬 Gerando roteiro Video Semanal...
python agents/video_10min/main.py --ideia "%ABSOLUTE_PATH%" --exportar
if %errorlevel% equ 0 (echo   ✅ Video gerado!) else (echo   ⚠️ Falha no video)
echo.

:: 4) Gerar Post Instagram
echo [4/4] 📝 Gerando Post Instagram...
:: Extrai tema da primeira linha # do arquivo
python agents/text_generator/main.py "%IDEIA%" educational --perfil paz-na-conta
if %errorlevel% equ 0 (echo   ✅ Post gerado!) else (echo   ⚠️ Falha no post)
echo.

echo ╔══════════════════════════════════════════════╗
echo ║     ✅ Pipeline Concluido!                    ║
echo ╚══════════════════════════════════════════════╝
echo.
echo 📂 Outputs:
echo   🎠 Carrossel:    acervo\carrossel\
echo   📱 Reels:        acervo\ideias\
echo   🎬 Video 10min:  acervo\video\
echo   📝 Post:         perfis\paz-na-conta\output\text_posts\
echo.

pause
