@echo off
REM ============================================================================
REM  Automotive Analytics - Universal Startup Script
REM  One script to rule them all!
REM ============================================================================

setlocal enabledelayedexpansion

REM Check for command line arguments
set "ACTION=%~1"
if "%ACTION%"=="" set "ACTION=start"

REM Display header
echo.
echo ============================================================================
echo   AUTOMOTIVE ANALYTICS SYSTEM
echo ============================================================================
echo.

REM Handle different actions
if /i "%ACTION%"=="start" goto :start
if /i "%ACTION%"=="stop" goto :stop
if /i "%ACTION%"=="restart" goto :restart
if /i "%ACTION%"=="test" goto :test
if /i "%ACTION%"=="help" goto :help
goto :help

:start
echo [ACTION] Starting services...
echo.

REM Check if .env exists
if not exist ".env" (
    echo [ERROR] .env file not found!
    echo.
    echo Please create a .env file with:
    echo   DATABASE_URL=postgresql://user:pass@localhost:5432/db
    echo   OPENAI_API_KEY=sk-your-key-here
    echo.
    pause
    exit /b 1
)

REM Load environment variables
echo [1/6] Loading environment variables...
for /f "usebackq tokens=1,* delims==" %%a in (".env") do (
    set "%%a=%%b"
)
echo       OPENAI_API_KEY: %OPENAI_API_KEY:~0,20%...
echo       DATABASE_URL: %DATABASE_URL:~0,40%...
echo.

REM Check virtual environment
echo [2/6] Checking virtual environment...
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo.
    echo Run this first: python -m venv venv
    echo Then install: venv\Scripts\pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)
call venv\Scripts\activate.bat
echo       Virtual environment activated
echo.

REM Test OpenAI connection
echo [3/6] Testing OpenAI API connection...
python verify_openai_api.py >nul 2>&1
if errorlevel 1 (
    echo [WARNING] OpenAI API test failed. Check your API key.
    echo           Services will start but AI features may not work.
    timeout /t 3 /nobreak >nul
) else (
    echo       OpenAI API connection OK
)
echo.

REM Kill existing processes
echo [4/6] Checking for existing services...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000" 2^>nul') do (
    taskkill /F /PID %%a >nul 2>&1
)
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8501" 2^>nul') do (
    taskkill /F /PID %%a >nul 2>&1
)
echo       Ports 8000 and 8501 are available
echo.

REM Start API server
echo [5/6] Starting API server on port 8000...
start "Automotive API" cmd /k "cd /d "%~dp0" && call venv\Scripts\activate.bat && set OPENAI_API_KEY=%OPENAI_API_KEY% && set DATABASE_URL=%DATABASE_URL% && uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload"
echo       API server starting...
timeout /t 5 /nobreak >nul
echo.

REM Start Dashboard
echo [6/6] Starting Dashboard on port 8501...
start "Automotive Dashboard" cmd /k "cd /d "%~dp0" && call venv\Scripts\activate.bat && streamlit run src/dashboard/app.py --server.port 8501"
echo       Dashboard starting...
timeout /t 3 /nobreak >nul
echo.

REM Success message
echo ============================================================================
echo   SERVICES STARTED SUCCESSFULLY!
echo ============================================================================
echo.
echo   Dashboard:  http://localhost:8501
echo   API Docs:   http://localhost:8000/docs
echo   API:        http://localhost:8000
echo.
echo   Press Ctrl+C in the service windows to stop them.
echo.
echo ============================================================================
echo.

REM Wait then open browser
timeout /t 3 /nobreak >nul
start http://localhost:8501

echo Services are running. You can close this window.
echo.
pause
goto :eof

:stop
echo [ACTION] Stopping services...
echo.
taskkill /F /FI "WINDOWTITLE eq Automotive API*" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq Automotive Dashboard*" >nul 2>&1
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000" 2^>nul') do (
    taskkill /F /PID %%a >nul 2>&1
)
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8501" 2^>nul') do (
    taskkill /F /PID %%a >nul 2>&1
)
echo [OK] Services stopped
echo.
goto :eof

:restart
echo [ACTION] Restarting services...
echo.
call :stop
timeout /t 2 /nobreak >nul
call :start
goto :eof

:test
echo [ACTION] Testing system configuration...
echo.

REM Test .env
if exist ".env" (
    echo [OK] .env file found
) else (
    echo [ERROR] .env file missing
    exit /b 1
)

REM Test venv
if exist "venv\Scripts\activate.bat" (
    echo [OK] Virtual environment found
) else (
    echo [ERROR] Virtual environment missing
    exit /b 1
)

REM Test OpenAI
call venv\Scripts\activate.bat
echo.
echo Testing OpenAI API...
python verify_openai_api.py
echo.
pause
goto :eof

:help
echo USAGE: start.bat [command]
echo.
echo COMMANDS:
echo   start     Start both API and Dashboard (default)
echo   stop      Stop all services
echo   restart   Restart all services
echo   test      Test system configuration
echo   help      Show this help message
echo.
echo EXAMPLES:
echo   start.bat           # Start services
echo   start.bat start     # Start services
echo   start.bat stop      # Stop services
echo   start.bat restart   # Restart services
echo   start.bat test      # Test configuration
echo.
pause
goto :eof

