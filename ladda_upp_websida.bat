@echo off
setlocal enabledelayedexpansion

REM ===================================================================
REM ==    Automated GitHub Pages Deployer (no prompts)               ==
REM ==    Version 3.0 - Fully automated with proper authentication   ==
REM ===================================================================
echo.
echo =====================================
echo ==   Automated GitHub Deployer     ==
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

REM --- Remove any surrounding spaces or quotes (both single and double) ---
set GITHUB_TOKEN=%GITHUB_TOKEN: =%
set GITHUB_TOKEN=%GITHUB_TOKEN:"=%
set GITHUB_TOKEN=%GITHUB_TOKEN:'=%

REM --- Get Repository URL ---
for /f "tokens=*" %%a in ('git config --get remote.origin.url') do set REPO_URL=%%a

REM --- Validate inputs ---
if not defined GITHUB_TOKEN (
    echo [FATAL ERROR] Could not read GITHUB_TOKEN from .env file.
    echo Make sure the file contains: GITHUB_TOKEN=ghp_YourTokenHere
    goto:end
)

REM --- Check if token looks valid (both old ghp_ and new github_pat_ formats) ---
echo %GITHUB_TOKEN% | findstr /b "ghp_ github_pat_" >nul
if %errorlevel% neq 0 (
    echo [FATAL ERROR] Invalid token format. GitHub tokens should start with 'ghp_' or 'github_pat_'
    echo Please check your .env file.
    goto:end
)

echo "%REPO_URL%" | find "https://" >nul
if %errorlevel% neq 0 (
    echo [FATAL ERROR] Your Git repository is using an SSH URL, not an HTTPS URL.
    echo The script needs an HTTPS URL. Please run this command to fix it:
    echo.
    echo   git remote set-url origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
    echo.
    goto:end
)

REM --- Debug output (show first 8 chars of token for verification) ---
set "TOKEN_START=!GITHUB_TOKEN:~0,8!"
echo [INFO] Token found: !TOKEN_START!...
echo [INFO] Repository URL: %REPO_URL%

REM --- Extract username and repo from URL ---
REM Remove https://github.com/ from the URL
set "REPO_PATH=%REPO_URL:https://github.com/=%"
REM Remove .git from the end if present
set "REPO_PATH=%REPO_PATH:.git=%"

REM --- Set up Git to use the token ---
REM Configure Git to use the token for this session
git config --local credential.helper ""
git config --local --unset-all http.https://github.com/.extraheader 2>nul

REM --- Create timestamp for commit message ---
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set datetime=%datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2% %datetime:~8,2%:%datetime:~10,2%

REM --- Git Commands ---
echo.
echo [1/3] Staging changes...
git add .
if %errorlevel% neq 0 (
    echo [ERROR] Failed to stage changes. Make sure you're in a git repository.
    goto:end
)

echo [2/3] Committing...
git commit -m "Auto deploy: %datetime%"
if %errorlevel% equ 1 (
    echo.
    echo [INFO] No changes to commit. Repository is already up to date.
    goto:end
)

echo [3/3] Pushing to GitHub...
REM Use the token directly in the push command
git push https://%GITHUB_TOKEN%@github.com/%REPO_PATH%.git main

if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo ==         DEPLOYMENT FAILED!         ==
    echo ========================================
    echo.
    echo Common issues:
    echo - Token may be expired or invalid
    echo - Token needs 'repo' permissions
    echo - Check internet connection
    echo - Ensure 'main' branch exists
    echo.
    echo If you see a login prompt, your token isn't working.
    goto:end
)

echo.
echo ========================================
echo ==      DEPLOYMENT SUCCESSFUL!        ==
echo ========================================
echo.
echo Changes pushed at: %datetime%
echo GitHub Pages will update in 1-2 minutes.
echo.

:end
REM Auto-close after 5 seconds on success, wait for keypress on error
if %errorlevel% equ 0 (
    echo Window will close in 5 seconds...
    timeout /t 5 /nobreak >nul
) else (
    echo Press any key to close...
    pause >nul
)