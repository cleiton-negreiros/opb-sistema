@echo off
chcp 65001 >nul
title 📦 Pipeline de Conteudo — OPB Sistema

cd /d "%~dp0"

:: ============================================
:: Pipeline de Conteudo Diario
:: Uso: pipeline-conteudo.bat [arquivo_ideia]
:: Se sem argumento, pega o arquivo mais recente de:
::   _conteudo\email-diario\  >  inbox\  >  acervo\ideias\
:: ============================================

set "IDEIA=%~1"

if "%IDEIA%"=="" (
    for /f "delims=" %%f in ('dir /b /o-d /a-d "_conteudo\email-diario\*.md" 2^>nul') do (
        set "IDEIA=_conteudo\email-diario\%%f"
        goto found
    )
    for /f "delims=" %%f in ('dir /b /o-d /a-d "inbox\*.md" 2^>nul') do (
        set "IDEIA=inbox\%%f"
        goto found
    )
    for /f "delims=" %%f in ('dir /b /o-d /a-d "acervo\ideias\*.md" 2^>nul') do (
        set "IDEIA=acervo\ideias\%%f"
        goto found
    )
    echo Nenhum arquivo encontrado.
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
set "TIMESTAMP=%DATE:/=%_%TIME::=%"
set "TIMESTAMP=%TIMESTAMP: =0%

:: 1) Gerar Carrossel
echo [1/4] 🎠 Gerando Carrossel...
python agents/carrossel/main.py --ideia "%ABSOLUTE_PATH%" --tipo educacional --formato carrossel --exportar
if %errorlevel% equ 0 (
    echo   ✅ Carrossel gerado!
    for /f "delims=" %%f in ('dir /b /o-d /a-d "acervo\carrossel\*.md" 2^>nul') do (
        copy "acervo\carrossel\%%f" "_conteudo\carrossel\" >nul 2>nul
        goto car_done
    )
)
:car_done
echo.

:: 2) Gerar Reels Script
echo [2/4] 📱 Gerando roteiro Reels...
python agents/reels_script/main.py "%IDEIA%" --ideia "%ABSOLUTE_PATH%" --duracao 60 --formato reels --exportar
if %errorlevel% equ 0 (
    echo   ✅ Reels gerado!
    for /f "delims=" %%f in ('dir /b /o-d /a-d "acervo\ideias\script_*.txt" 2^>nul') do (
        copy "acervo\ideias\%%f" "_conteudo\reels\" >nul 2>nul
        goto reel_done
    )
)
:reel_done
echo.

:: 3) Gerar Video 10min
echo [3/4] 🎬 Gerando roteiro Video Semanal...
python agents/video_10min/main.py --ideia "%ABSOLUTE_PATH%" --exportar
if %errorlevel% equ 0 (
    echo   ✅ Video gerado!
    for /f "delims=" %%f in ('dir /b /o-d /a-d "acervo\video\*.txt" 2^>nul') do (
        copy "acervo\video\%%f" "_conteudo\video\" >nul 2>nul
        goto vid_done
    )
)
:vid_done
echo.

:: 4) Gerar Post Instagram
echo [4/4] 📝 Gerando Post Instagram...
python agents/text_generator/main.py "%IDEIA%" educational --perfil paz-na-conta
if %errorlevel% equ 0 (echo   ✅ Post gerado!) else (echo   ⚠️ Falha no post)
echo.

echo ╔══════════════════════════════════════════════╗
echo ║     ✅ Pipeline Concluido!                    ║
echo ╚══════════════════════════════════════════════╝
echo.
echo 📂 Outputs (Obsidian):
echo   📧 Email original: _conteudo\email-diario\
echo   🎠 Carrossel:      _conteudo\carrossel\
echo   📱 Reels:          _conteudo\reels\
echo   🎬 Video 10min:    _conteudo\video\
echo   ✅ Publicar em:    _conteudo\publicados\
echo.
echo 🔗 Abra _home.md no Obsidian para ver tudo.
echo.

pause
