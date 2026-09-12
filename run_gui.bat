@echo off
title UPHSD CCS - OBE AI Microservice Studio Web GUI
color 0B

cd /d "%~dp0"

echo ======================================================================
echo    UPHSD CCS - OBE AI Microservice Studio Web GUI Runner
echo    Student: Christian Ezekiel L. Carvajal
echo    Evaluator: Prof. Rob Malitao
echo    Subject: Artificial Intelligence
echo ======================================================================
echo.

:: Step 1: Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [ERROR] Python is not detected in your system PATH.
    echo Please install Python 3.10+ and add it to your PATH.
    goto :FAIL
)
echo [+] Python installation detected.

:: Step 2: Virtual Environment Setup
if not exist ".venv" (
    if exist "..\.venv" (
        echo [*] Using parent virtual environment ..\.venv...
        call ..\.venv\Scripts\activate.bat
    ) else (
        echo [*] Creating isolated virtual environment .venv...
        python -m venv .venv
        if errorlevel 1 (
            color 0C
            echo [ERROR] Failed to create .venv.
            goto :FAIL
        )
        call .venv\Scripts\activate.bat
    )
) else (
    echo [*] Activating local virtual environment .venv...
    call .venv\Scripts\activate.bat
)

:: Step 3: Install Dependencies
echo [*] Verifying required dependencies...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    color 0C
    echo [ERROR] Failed to install dependencies from requirements.txt.
    goto :FAIL
)
echo [+] Dependencies verified.
echo.

:: Step 4: Check Ollama & Model
echo [*] Checking Ollama installation and local service...
ollama --version >nul 2>&1
if errorlevel 1 (
    color 0E
    echo [WARNING] Ollama CLI is not found in PATH or Ollama service is not running.
    echo The GUI will load cached outputs and allow live auditing, but generation requires Ollama.
) else (
    echo [+] Ollama CLI detected.
    echo [*] Verifying model qwen3.5:4b...
    ollama list | findstr /i "qwen3.5:4b" >nul 2>&1
    if errorlevel 1 (
        echo [!] Model 'qwen3.5:4b' was not found locally.
        echo [*] Pulling model via: ollama pull qwen3.5:4b...
        ollama pull qwen3.5:4b
    ) else (
        echo [+] Model 'qwen3.5:4b' is ready.
    )
)
echo.

:: Step 5: Launch GUI Server & Open Browser
echo ======================================================================
echo    STARTING LOCAL HTTP SERVER ON http://127.0.0.1:8000
echo ======================================================================
echo.
echo Launching default web browser...
start http://127.0.0.1:8000

echo.
echo The OBE Web Studio is running. Keep this console window open!
echo Press Ctrl+C in this window to stop the server.
echo.

python app.py
if errorlevel 1 (
    color 0C
    echo.
    echo [ERROR] Server encountered a runtime error.
    goto :FAIL
)

goto :END

:FAIL
echo.
echo ======================================================================
echo    EXECUTION HALTED: Please review the log above.
echo ======================================================================

:END
echo.
echo Press any key to close this window...
pause >nul
