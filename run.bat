@echo off
echo ==========================================
echo   AI Job Application Agent - Setup & Run
echo ==========================================
echo.

:: Set database to SQLite (no PostgreSQL needed)
set DATABASE_URL=sqlite:///./test.db

:: Install Python dependencies
echo [1/3] Installing Python dependencies...
pip install fastapi uvicorn sqlalchemy alembic pydantic pydantic-settings python-jose[cryptography] bcrypt python-multipart aiofiles httpx email-validator >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: pip install failed. Make sure Python is installed.
    pause
    exit /b 1
)
echo       Done!

:: Install Frontend dependencies
echo [2/3] Installing Frontend dependencies...
cd frontend
call npm install >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: npm install failed. Make sure Node.js is installed.
    pause
    exit /b 1
)
echo       Done!
cd ..

:: Start both servers
echo [3/3] Starting the application...
echo.
echo ==========================================
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:3000
echo   API Docs: http://localhost:8000/docs
echo ==========================================
echo.
echo Opening browser in 5 seconds...
echo Press Ctrl+C to stop the application.
echo.

:: Start backend in background
start "AI Job Agent - Backend" cmd /k "set DATABASE_URL=sqlite:///./test.db && python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000"

:: Wait a moment for backend to start
timeout /t 3 >nul

:: Start frontend in background
start "AI Job Agent - Frontend" cmd /k "cd frontend && npm run dev"

:: Wait then open browser
timeout /t 5 >nul
start http://localhost:3000

echo Both servers are running. Close this window when done.
pause
