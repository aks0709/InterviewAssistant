@echo off
echo ========================================
echo Starting Interview Assistant
echo ========================================
echo.

REM Start Backend in new terminal
echo [1/2] Starting Backend Server...
start "Interview Assistant - Backend" cmd /k "cd /d %~dp0backend && call C:\venvs\interview-assistant-313\Scripts\activate.bat && python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload"

REM Wait 3 seconds for backend to initialize
timeout /t 3 /nobreak >nul

REM Start Frontend in new terminal
echo [2/2] Starting Frontend Server...
start "Interview Assistant - Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ========================================
echo Both servers are starting...
echo ========================================
echo Backend:  http://localhost:8001
echo Frontend: http://localhost:5173
echo.
echo Press any key to exit this window...
pause >nul
