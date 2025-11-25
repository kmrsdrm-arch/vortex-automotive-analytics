@echo off
echo ========================================
echo Push VORTEX to GitHub
echo ========================================
echo.

:: Prompt for GitHub username
set /p GITHUB_USERNAME="Enter your GitHub username: "

:: Confirm repository name
echo.
echo Repository will be: https://github.com/%GITHUB_USERNAME%/vortex-automotive-analytics
echo.
set /p CONFIRM="Is this correct? (Y/N): "

if /i "%CONFIRM%" NEQ "Y" (
    echo.
    echo Cancelled. Please run this script again.
    pause
    exit /b
)

echo.
echo ========================================
echo Pushing to GitHub...
echo ========================================
echo.

:: Add remote
echo Adding GitHub remote...
git remote add origin https://github.com/%GITHUB_USERNAME%/vortex-automotive-analytics.git

:: Check if remote was added (might already exist)
if errorlevel 1 (
    echo Remote 'origin' already exists. Updating URL...
    git remote set-url origin https://github.com/%GITHUB_USERNAME%/vortex-automotive-analytics.git
)

:: Ask for branch name preference
echo.
set /p BRANCH_NAME="Branch name (main/master, default: main): "
if "%BRANCH_NAME%"=="" set BRANCH_NAME=main

:: Rename branch if needed
echo.
echo Setting branch to %BRANCH_NAME%...
git branch -M %BRANCH_NAME%

:: Push to GitHub
echo.
echo Pushing code to GitHub...
git push -u origin %BRANCH_NAME%

if errorlevel 1 (
    echo.
    echo ========================================
    echo ERROR: Push failed!
    echo ========================================
    echo.
    echo Possible reasons:
    echo 1. Repository doesn't exist on GitHub yet
    echo 2. Authentication failed (check your credentials)
    echo 3. Wrong username or repository name
    echo.
    echo Please:
    echo 1. Verify the repository exists at:
    echo    https://github.com/%GITHUB_USERNAME%/vortex-automotive-analytics
    echo 2. Make sure you have write access
    echo 3. Check your GitHub credentials
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS! 🎉
echo ========================================
echo.
echo Your code has been pushed to GitHub!
echo.
echo Repository URL:
echo https://github.com/%GITHUB_USERNAME%/vortex-automotive-analytics
echo.
echo Next steps:
echo 1. Visit your repository on GitHub
echo 2. Follow DEPLOYMENT_QUICKSTART.md to deploy on Render.com
echo 3. Share the live link with hiring managers!
echo.
pause

