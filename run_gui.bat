@echo off
title UPHSD CCS - OBE AI Microservice Studio Web GUI
cd /d "%~dp0"
python run_gui.py %*
if errorlevel 1 (
    echo.
    echo [ERROR] Execution encountered an error.
    pause
)
