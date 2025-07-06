@echo off
REM setup.bat - Create venv and install requirements
python -m venv .venv
if exist .venv\Scripts\activate (
    call .venv\Scripts\activate
    pip install --upgrade pip
    pip install -r requirements.txt
) else (
    echo Failed to create virtual environment.
    exit /b 1
)
echo Setup complete.
