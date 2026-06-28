@echo off
echo  PhishGuard - Stopping server...
taskkill /F /IM pythonw.exe >nul 2>&1
taskkill /F /IM python.exe /FI "WINDOWTITLE eq PhishGuard*" >nul 2>&1
echo  Done! Server stopped.
pause
