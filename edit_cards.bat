@echo off
REM ============================================================
REM  Bran Castle – OPEN THE CARD EDITOR LOCALLY
REM  ------------------------------------------------------------
REM  • Creates a Python venv the first time it runs
REM  • Installs requirements (quietly)
REM  • Launches the Flask app and opens the browser
REM ============================================================

echo.
echo ===============================
echo   Bran Castle – Card Editor
echo ===============================
echo.

REM ---- 1. Create virtual-env if it doesn't exist ----------------
if not exist ".venv" (
    echo Creating local Python environment …
    python -m venv .venv
)

REM ---- 2. Activate the venv ------------------------------------
call ".venv\Scripts\activate.bat"

REM ---- 3. Install/upgrade requirements -------------------------
echo Installing/Updating required packages …
pip install -q -r requirements.txt

REM ---- 4. Fire up the editor -----------------------------------
echo.
echo Starting the editor – a browser window will open shortly.
start "" http://localhost:5000

REM   Flask will keep running until this window is closed
echo Press Ctrl+C to stop the server.
python app.py
