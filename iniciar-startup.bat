@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"

set LOGFILE=%TEMP%\opb-startup.log
echo [%DATE% %TIME%] ===== INICIANDO OPB STARTUP ===== >"%LOGFILE%"

:: ── Git pull silencioso ──
echo [%DATE% %TIME%] Git pull... >>"%LOGFILE%"
git pull >>"%LOGFILE%" 2>&1

:: ── Auditoria de código ──
echo [%DATE% %TIME%] Auditoria de codigo... >>"%LOGFILE%"
python audit/auditoria_diaria.py --quick >>"%LOGFILE%" 2>&1

:: ── Coordenador (insight diario + orquestracao) ──
echo [%DATE% %TIME%] Coordenador - ciclo matinal... >>"%LOGFILE%"
python agents/coordinator/main.py morning >>"%LOGFILE%" 2>&1

:: ── Morning routine ──
echo [%DATE% %TIME%] Morning routine... >>"%LOGFILE%"
python morning_routine.py --quick >>"%LOGFILE%" 2>&1

:: ── API Server ──
echo [%DATE% %TIME%] Iniciando API Server... >>"%LOGFILE%"
start /min "" python api_server.py

timeout /t 5 /nobreak > nul

:: ── Telegram Bot ──
echo [%DATE% %TIME%] Iniciando Telegram Bot... >>"%LOGFILE%"
start /min "" cmd /c python agents\telegram_bot\main.py

timeout /t 3 /nobreak > nul

:: ── Radagast (dry-run) ──
echo [%DATE% %TIME%] Radagast dry-run... >>"%LOGFILE%"
start /min "" cmd /c python agents\radagast\radagast.py --dry-run

:: ── Abrir plataforma ──
echo [%DATE% %TIME%] Abrindo navegador... >>"%LOGFILE%"
timeout /t 3 /nobreak > nul
start http://localhost:5000

echo [%DATE% %TIME%] ===== OPB STARTUP CONCLUIDO ===== >>"%LOGFILE%"
