@echo off
setlocal

echo ============================================
echo   Consultar CNPJ - Iniciando aplicacao
echo ============================================

REM Verifica se o Python esta instalado
where python >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado no PATH.
    echo Instale o Python em https://www.python.org/downloads/ e tente novamente.
    pause
    exit /b 1
)

REM Cria ambiente virtual se nao existir
if not exist ".venv" (
    echo Criando ambiente virtual...
    python -m venv .venv
)

call .venv\Scripts\activate.bat

echo Instalando dependencias...
pip install --quiet --upgrade pip
pip install --quiet flask requests

echo.
echo Iniciando servidor em http://127.0.0.1:5000
echo Pressione CTRL+C para encerrar.
echo.

start "" http://127.0.0.1:5000
python app.py

pause
