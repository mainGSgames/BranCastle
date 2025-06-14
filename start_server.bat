@echo off
echo Starting local web server...

REM Kill any existing Python HTTP servers on port 8000
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do (
    echo Killing existing server on port 8000 (PID: %%a)
    taskkill /f /pid %%a >nul 2>&1
)

REM Start Python HTTP server in background
echo Starting Python HTTP server on port 8000...
start /min python -m http.server 8000

REM Wait for server to start
echo Waiting for server to start...
timeout /t 3 /nobreak >nul

REM Open Chrome with the local server
echo Opening Chrome...
start chrome "http://localhost:8000/index.html"

echo Server started! Press any key to stop the server...
pause >nul

REM Kill the Python server when user presses a key
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do (
    echo Stopping server (PID: %%a)
    taskkill /f /pid %%a >nul 2>&1
)

echo Server stopped.
pause
