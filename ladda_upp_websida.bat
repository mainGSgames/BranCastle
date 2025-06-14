@echo off
setlocal enabledelayedexpansion

REM ===================================================================
REM ==    Simple GitHub Pages Deployer (for 'main' branch deploy)    ==
REM ==    Version 2.1 - Fixed token reading and URL construction     ==
REM ===================================================================
echo.
echo =====================================
echo ==   Bran Castle Card Deployer     ==
echo =====================================
echo.

REM --- Pre-flight Checks ---
IF EXIST .env.txt (
    echo [FATAL ERROR] Your secret file is named '.env.txt' instead of '.env'.
    echo.
    echo Please rename it to '.env' to fix this.
    echo ^(You may need to enable 'File name extensions' in Windows Explorer's View tab^).
    goto:end
)
IF NOT EXIST .env (
    echo [FATAL ERROR] The .env file is missing!
    echo.
    echo Please create a file named .env in this folder.
    echo Inside the file, add one line: GITHUB_TOKEN=ghp_YourTokenHere
    goto:end
)

REM --- Read Token from .env file ---
for /f "tokens=2 delims==" %%a in ('type .env ^| findstr /i "GITHUB_TOKEN"') do set GITHUB_TOKEN=%%a

REM --- Remove any surrounding spaces or quotes ---
set GITHUB_TOKEN=%GITHUB_TOKEN: =%
set GITHUB_TOKEN=%GITHUB_TOKEN:"=%

REM --- Get Repository URL ---
for /f "tokens=*" %%a in ('git config --get remote.origin.url') do set REPO_URL=%%a

REM --- Validate inputs ---
if not defined GITHUB_TOKEN (
    echo [FATAL ERROR] Could not read GITHUB_TOKEN from .env file.
    echo Make sure the file contains: GITHUB_TOKEN=ghp_YourTokenHere
    goto:end
)

echo "%REPO_URL%" | find "https://" >nul
if %errorlevel% neq 0 (
    echo [FATAL ERROR] Your Git repository is using an SSH URL, not an HTTPS URL.
    echo The script needs an HTTPS URL. Please run this command to fix it:
    echo.
    echo   git remote set-url origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
    echo.
    echo Replace YOUR_USERNAME and YOUR_REPO with your actual GitHub username and repository name.
    goto:end
)

REM --- Debug output (show first 4 chars of token for verification) ---
set "TOKEN_START=!GITHUB_TOKEN:~0,4!"
echo [INFO] Found token starting with: !TOKEN_START!...
echo [INFO] Repository URL: %REPO_URL%

REM --- Extract username and repo from URL ---
REM Remove https://github.com/ from the URL
set "REPO_PATH=%REPO_URL:https://github.com/=%"
REM Remove .git from the end if present
set "REPO_PATH=%REPO_PATH:.git=%"

REM --- Construct the authenticated URL ---
set "AUTH_URL=https://%GITHUB_TOKEN%@github.com/%REPO_PATH%.git"

REM --- Get commit message from user ---
echo.
set /p COMMIT_MESSAGE="Enter a short description for this update: "
if not defined COMMIT_MESSAGE set COMMIT_MESSAGE=Site update via deploy script

echo.
echo Preparing to push changes...

REM --- Git Commands ---
git add .
if %errorlevel% neq 0 (
    echo [ERROR] Failed to stage changes. Make sure you're in a git repository.
    goto:end
)

git commit -m "%COMMIT_MESSAGE%"
if %errorlevel% equ 1 (
    echo.
    echo [INFO] No changes to commit. Your repository is already up to date.
    goto:end
)

echo.
echo Pushing to the 'main' branch...
git push "%AUTH_URL%" main

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to push to GitHub.
    echo Common issues:
    echo - Check that your token in the .env file is correct and not expired
    echo - Ensure your token has 'repo' permissions
    echo - Check your internet connection
    echo - Make sure the 'main' branch exists (not 'master')
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