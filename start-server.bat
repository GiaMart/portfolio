@echo off
cd /d "%~dp0"
echo Starting portfolio at http://localhost:5500
echo.
echo   Homepage:  http://localhost:5500/
echo   Demo:      http://localhost:5500/work/employee-portal-2.html
echo.
echo Press Ctrl+C to stop.
python -m http.server 5500
