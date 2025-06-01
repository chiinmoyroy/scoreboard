@echo off
echo Cricket Scoreboard Analyzer
echo ==========================
echo.
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found! Please install Python from python.org
    echo.
    pause
    exit /b 1
)

echo Python found!
echo.
echo Installing required packages...
pip install pyyaml >nul 2>&1

echo.
echo Starting Cricket Scoreboard Analyzer...
echo.
python gui_app.py

if errorlevel 1 (
    echo.
    echo Application closed with error. Check the files and try again.
    pause
)