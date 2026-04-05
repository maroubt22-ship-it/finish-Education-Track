@echo off
REM Launcher for EduTrack IA Gradio AI Demo
REM Windows Batch Script

echo ======================================
echo    EduTrack IA - Gradio AI Demo
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo Starting Gradio AI Demo Interface...
echo Demo will open at http://localhost:7860
echo.
echo Press Ctrl+C to stop the server
echo.

cd /d "%~dp0"
python frontend\gradio\app.py

pause
