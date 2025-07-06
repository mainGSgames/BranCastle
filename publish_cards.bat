@echo off
REM ============================================================
REM  Bran Castle – PUBLISH CHANGES TO GITHUB
REM  ------------------------------------------------------------
REM  • Asks for a commit message (or uses date/time by default)
REM  • git add         (cards + templates)
REM  • git commit
REM  • git pull --rebase   (just in case)
REM  • git push
REM  ------------------------------------------------------------
REM  Requires: git installed and an origin remote with push
REM  rights (the repo’s GITHUB_TOKEN or cached credentials).
REM ============================================================

echo.
echo ========================================
echo   Bran Castle – Publish Card Changes
echo ========================================
echo.

SETLOCAL ENABLEDELAYEDEXPANSION

:: 1. Ask for a commit message -----------------------------------
set /P COMMIT_MSG=Enter a short description of your changes: 
if "%COMMIT_MSG%"=="" (
    set COMMIT_MSG=Card update %DATE% %TIME%
)

:: 2. Stage relevant files ---------------------------------------
echo.
echo Staging modified and new files …
git add -A

:: 3. Commit (if there is anything new) --------------------------
echo.
echo Creating commit …
git commit -m "%COMMIT_MSG%"
if errorlevel 1 (
    echo No changes to commit – nothing to do.
    goto end
)

:: 4. Pull last-minute upstream changes then push ----------------
echo.
echo Pulling latest from origin …
git pull --rebase

echo.
echo Pushing to origin …
git push

echo.
echo All done!  ✅
echo Your website https://maingsgames.github.io/BranCastle/ will update automatically in a minute or two.
echo.

:end
pause
