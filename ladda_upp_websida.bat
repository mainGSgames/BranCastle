@echo off
setlocal

REM ===================================================================
REM ==    Simple GitHub Pages Deployer (for 'main' branch deploy)    ==
REM ===================================================================
echo.
echo =====================================
echo ==   Bran Castle Card Deployer     ==
echo =====================================
echo.

REM --- Check for .env file ---
IF NOT EXIST .env (
    echo [ERROR] The .env file is missing!
    echo Please create a file named .env and add your GitHub token to it.
    echo Example: GITHUB_TOKEN=ghp_YourTokenHere
    goto:end
)

REM --- Read Token and Repo URL ---
set /p GITHUB_TOKEN= < .env
for /f "tokens=*" %%a in ('git config --get remote.origin.url') do set REPO_URL=%%a

REM --- Check if token was read ---
if not defined GITHUB_TOKEN (
    echo [ERROR] Could not read GITHUB_TOKEN from .env file.
    echo Make sure the file is not empty and is formatted correctly.
    goto:end
)

REM --- Construct the authenticated URL ---
set "AUTH_URL=%REPO_URL:https://=%
set "AUTH_URL=https://%GITHUB_TOKEN%@%AUTH_URL%"

REM --- Get commit message from user ---
set /p COMMIT_MESSAGE="Enter a short description for this update: "
if not defined COMMIT_MESSAGE set COMMIT_MESSAGE="Site update via deploy script"

echo.
echo Preparing to push changes...

REM --- Git Commands ---
git add .
git commit -m "%COMMIT_MESSAGE%"

echo.
echo Pushing to the 'main' branch...
git push %AUTH_URL% main

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to push to GitHub.
    echo Please check your token in the .env file and your internet connection.
    goto:end
)

echo.
echo ========================================
echo ==      DEPLOYMENT SUCCESSFUL!        ==
echo ========================================
echo.
echo Your changes have been pushed to the 'main' branch.
echo GitHub will update your site in a few minutes.
echo.

:end
echo Press any key to close this window.
pause > nul