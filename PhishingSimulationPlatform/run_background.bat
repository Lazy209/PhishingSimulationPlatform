@echo off
title PhishGuard - Cybersecurity Project
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    py -m venv .venv
    call .venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    call .venv\Scripts\activate.bat
)

echo.
echo  PhishGuard - Starting in background...
echo  Open: http://127.0.0.1:5000
echo  Admin: http://127.0.0.1:5000/admin
echo.
echo  To stop the server: double-click stop.bat
echo.

start /B pythonw app.py > phishguard.log 2>&1

timeout /t 2 >nul
echo  Server started! Opening browser...
start http://127.0.0.1:5000
