@echo off
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║          Abrindo OPB Sistema no Obsidian                     ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

:: Verifica se Obsidian existe
if exist "%LOCALAPPDATA%\obsidian\Obsidian.exe" (
    echo [OK] Obsidian encontrado!
    echo.
    echo Abrindo pasta como vault...
    start "" "%LOCALAPPDATA%\obsidian\Obsidian.exe" "%CD%"
    echo.
    echo Feche esta janela e olhe para o Obsidian!
) else (
    echo [ERRO] Obsidian nao encontrado
    echo.
    echo Baixe em: https://obsidian.md/download
    echo.
    pause
)