@echo off
REM run.bat - Activate venv and run app.py
if not exist .venv\Scripts\activate (
    echo Virtual environment not found. Run setup.bat first.
    exit /b 1
)
call .venv\Scripts\activate
python app.py
