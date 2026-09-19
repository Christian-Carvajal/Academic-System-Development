@echo off
title UPHSD CCS - OBE AI Microservice 18-Week Institutional Pipeline Runner
color 0B
cd /d "%~dp0"

echo ======================================================================
echo    UPHSD CCS - OBE AI Microservice 18-Week Institutional Pipeline
echo    Course: BSCS 3112 / Artificial Intelligence (Lesson 5 Milestones 1 and 2)
echo    Students: Christian Ezekiel L. Carvajal and John Miko P. Sarsalijo
echo    Evaluator: Prof. Roberto L. Malitao
echo    Model Engine: Strictly locked to qwen3.5:4b
echo ======================================================================
echo.

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

:: Step 1: Check Python
"%PY_EXE%" --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [ERROR] Python is not detected or invalid.
    pause
    exit /b 1
)

:: Step 2: Run Milestone 1 Engine (qwen3.5:4b)
echo.
echo ======================================================================
echo    [1/3] RUNNING MILESTONE 1: 18-Week Full Syllabus Engine (qwen3.5:4b)
echo ======================================================================
"%PY_EXE%" llm_engine.py %*
if errorlevel 1 (
    color 0C
    echo [ERROR] Milestone 1 LLM engine encountered an error.
    pause
    exit /b 1
)

:: Step 3: Run Milestone 2 Relational Database Manager
echo.
echo ======================================================================
echo    [2/3] RUNNING MILESTONE 2: Relational SQLite Ingestion and CRUD Check
echo ======================================================================
"%PY_EXE%" db_manager.py
if errorlevel 1 (
    color 0C
    echo [ERROR] Database manager encountered an error.
    pause
    exit /b 1
)

:: Step 4: Run Institutional Jinja2 Document Compiler
echo.
echo ======================================================================
echo    [3/3] RUNNING MILESTONE 2: Jinja2 Institutional HTML Compilation
echo ======================================================================
"%PY_EXE%" export_engine.py "CS 3110"
if errorlevel 1 (
    color 0C
    echo [ERROR] Document compilation encountered an error.
    pause
    exit /b 1
)

color 0A
echo.
echo ======================================================================
echo    SUCCESS: 18-Week Pipeline, SQLite DB and HTML Syllabus Compiled!
echo    Output Location: outputs\official_syllabus_CS_3110.html
echo ======================================================================
echo.

if exist "outputs\official_syllabus_CS_3110.html" (
    start "" "outputs\official_syllabus_CS_3110.html"
)

pause
