@echo off
REM StudyBuddy DK — Run Full Stack (Windows)

echo ==================================================
echo   ^!^! StudyBuddy DK — Full Stack Launcher
echo ==================================================
echo.
echo Starting both FastAPI backend and Streamlit frontend...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python 3.11+
    pause
    exit /b 1
)

REM Start FastAPI in a new window
echo Launching FastAPI on http://127.0.0.1:8000...
start "StudyBuddy DK - FastAPI Backend" cmd /k python api.py

REM Wait a moment for FastAPI to start
timeout /t 3 /nobreak

REM Start Streamlit
echo Launching Streamlit on http://127.0.0.1:8501...
streamlit run app.py

echo.
echo ==================================================
echo   ^!^! StudyBuddy DK Stopped
echo ==================================================
pause
