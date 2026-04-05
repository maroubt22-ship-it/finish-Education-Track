@echo off
REM Launcher for EduTrack IA Parent View
REM Windows Batch Script

echo ======================================
echo    EduTrack IA - Parent View Portal
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

echo Starting Parent View Portal...
echo Portal will open at http://localhost:8502
echo.
echo Press Ctrl+C to stop the server
echo.

cd /d "%~dp0"
streamlit run frontend\parent_view\app.py --server.port 8502

pause
