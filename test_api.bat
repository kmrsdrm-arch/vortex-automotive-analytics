@echo off
REM ===========================================================================
REM  OpenAI API Key Test - Simple Launcher
REM ===========================================================================
REM 
REM  This script tests your OpenAI API key configuration.
REM  Run this BEFORE starting services to ensure your API key works.
REM
REM  Usage: test_api.bat
REM ===========================================================================

echo.
echo ===========================================================================
echo   TESTING OPENAI API CONFIGURATION
echo ===========================================================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo.
    echo Please run: python -m venv venv
    echo Then: venv\Scripts\pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the verification script
python verify_openai_api.py

REM Capture exit code
set EXIT_CODE=%ERRORLEVEL%

echo.
if %EXIT_CODE%==0 (
    echo ===========================================================================
    echo   ✅ TEST PASSED - Your API key is working!
    echo ===========================================================================
) else (
    echo ===========================================================================
    echo   ❌ TEST FAILED - Please fix the issues above
    echo ===========================================================================
)
echo.

pause
exit /b %EXIT_CODE%

