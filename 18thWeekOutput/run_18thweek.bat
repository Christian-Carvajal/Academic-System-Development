@echo off
title UPHSD CCS - OBE AI Microservice 18-Week Interactive Studio
cd /d "%~dp0"

:: Detect Python executable (prefer local virtual environment if present)
if exist "%~dp0..\.venv\Scripts\python.exe" (
    set "PY_EXE=%~dp0..\.venv\Scripts\python.exe"
) else if exist "%~dp0..\..\.venv\Scripts\python.exe" (
    set "PY_EXE=%~dp0..\..\.venv\Scripts\python.exe"
) else if exist "%~dp0.venv\Scripts\python.exe" (
    set "PY_EXE=%~dp0.venv\Scripts\python.exe"
) else (
    set "PY_EXE=python"
)

"%PY_EXE%" run_18thweek.py %*
if errorlevel 1 (
    echo.
    echo [ERROR] 18-Week Interactive Studio encountered an error.
    pause
)
