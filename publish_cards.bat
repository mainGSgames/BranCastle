@echo off
SETLOCAL ENABLEDELAYEDEXPANSION
REM ============================================================
REM  Bran Castle – PUBLISH CHANGES TO GITHUB (Token-based v2)
REM  ------------------------------------------------------------
REM  • Will ALWAYS attempt to pull and push, even if there are
REM    no new changes to commit.
REM ============================================================
echo.
echo ========================================
echo   Bran Castle – Publish Card Changes
echo ========================================
echo.

:: --- 1. Authentication Setup ---
IF NOT EXIST .env (
    echo [FATAL ERROR] The .env file is missing!
    echo.
    echo Please create a file named .env in this folder.
    echo Inside the file, add one line: GITHUB_TOKEN=ghp_YourTokenHere
    goto end
)

for /f "tokens=1,* delims==" %%a in ('type .env ^| findstr /i "GITHUB_TOKEN"') do set GITHUB_TOKEN=%%b
set GITHUB_TOKEN=%GITHUB_TOKEN: =%
set GITHUB_TOKEN=%GITHUB_TOKEN:"=%
set GITHUB_TOKEN=%GITHUB_TOKEN:'=%

if not defined GITHUB_TOKEN (
    echo [FATAL ERROR] Could not read GITHUB_TOKEN from .env file.
    goto end
)

for /f "tokens=*" %%a in ('git config --get remote.origin.url') do set REPO_URL=%%a
set "REPO_PATH=!REPO_URL:https://github.com/=!"
set "REPO_PATH=!REPO_PATH:.git=!"

echo [INFO] Token found and ready for use.

:: --- 2. Ask for a commit message ---
echo.
set /P COMMIT_MSG=Enter a short description of your changes: 
if "%COMMIT_MSG%"=="" (
    set COMMIT_MSG=Card update %DATE% %TIME%
)

:: --- 3. Stage relevant files ---
echo.
echo Staging modified and new files ...
git add -A

:: --- 4. Commit (if there is anything new) ---
echo.
echo Creating commit ...
git commit -m "%COMMIT_MSG%"
REM =================================================================
REM == CHANGED SECTION: We no longer stop the script here.         ==
REM == If the commit fails, we'll still try to pull and push       ==
REM == any older commits that are waiting.                         ==
REM =================================================================

:: --- 5. Pull last-minute upstream changes then push ---
echo.
echo Pulling latest from origin ...
git pull --rebase
if errorlevel 1 (
    echo [ERROR] Failed to pull from origin. Please resolve conflicts manually.
    goto end
)

echo.
echo Pushing to origin ...
for /f "tokens=*" %%a in ('git branch --show-current') do set CURRENT_BRANCH=%%a

git push https://!GITHUB_TOKEN!@github.com/!REPO_PATH!.git !CURRENT_BRANCH!

if errorlevel 1 (
    echo.
    echo [ERROR] Push failed! Please check your token and permissions.
    goto end
)

echo.
echo All done!  ✅
echo Your website https://maingsgames.github.io/BranCastle/ will update automatically in a minute or two.
echo.

:end
pause