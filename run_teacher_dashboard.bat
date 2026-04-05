@echo off
REM Launcher for EduTrack IA Teacher Dashboard
REM Windows Batch Script

echo ======================================
echo    EduTrack IA - Teacher Dashboard
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

echo Starting Streamlit Teacher Dashboard...
echo Dashboard will open at http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

cd /d "%~dp0"
streamlit run frontend\streamlit\app.py --server.port 8501

pause
