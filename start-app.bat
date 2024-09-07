@echo off

REM Change to the directory where the script is located
cd /d %~dp0

REM Creation, installation & activation of local env
IF NOT EXIST .env (
    echo Creation of the environment...
    python -m venv .env
    cd .env\Scripts
    call activate.bat
    cd ../..
    pip install -r requirements.txt
) ELSE (
    echo Environnement activation...
    cd .env\Scripts
    call activate.bat
    cd ../..
)

FOR /F "tokens=*" %%A IN ('powershell -Command "Get-Command ollama"') DO SET OLLAMA_COMMAND=%%A
IF "%OLLAMA_COMMAND%"=="" (
    echo Ollama is not installed on your system.
    echo Please download it from https://ollama.com/download/windows
    pause
    exit
) ELSE (
    start cmd /k ollama serve
)

streamlit run menu.py