@echo off
setlocal
cd /d "%~dp0"
echo ==========================================
echo       NOVA AI - JOHN SKY DESIGN
echo ==========================================
py --version >nul 2>&1
if errorlevel 1 (
  echo ERRO: Python nao foi encontrado.
  echo Instala Python 3.12 de 64 bits e marca a opcao Add Python to PATH.
  pause
  exit /b 1
)
if not exist .venv (
  echo A criar ambiente virtual...
  py -m venv .venv
  if errorlevel 1 goto erro
)
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
if errorlevel 1 goto erro
echo A instalar dependencias...
pip install -r requirements.txt
if errorlevel 1 goto erro
if not exist .env copy .env.example .env >nul
if not exist .env (
  echo ERRO: nao foi possivel criar o ficheiro .env
  goto erro
)
echo.
echo Confirma que colocaste a nova chave Groq no ficheiro .env.
echo O painel sera aberto em http://127.0.0.1:5055
echo Mantem esta janela aberta enquanto usas a NOVA.
python app.py
if errorlevel 1 goto erro
exit /b 0
:erro
echo.
echo A instalacao ou execucao encontrou um erro. Le a mensagem acima.
pause
exit /b 1
