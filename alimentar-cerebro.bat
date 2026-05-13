@echo off
chcp 65001 >nul
title OPB - Alimentar Cerebro
color 0A
cls

echo ========================================
echo   ALIMENTAR CEREBRO - OPB Sistema
echo ========================================
echo.
echo  Passo 1: Abra o formulario.html no navegador
echo  Passo 2: Preencha todos os campos
echo  Passo 3: Clique em "Exportar Tudo"
echo  Passo 4: O texto foi copiado automaticamente
echo.
echo  Agora este script vai processar o conteudo...
echo.
echo  (Cole o conteudo se solicitado)
echo ========================================
echo.

python agents\consumo\alimentar.py

echo.
echo ========================================
echo  Pronto! O cerebro foi alimentado.
echo  Agora gere carrossel:
echo  python agents\carrossel\main.py "tema"
echo ========================================
pause