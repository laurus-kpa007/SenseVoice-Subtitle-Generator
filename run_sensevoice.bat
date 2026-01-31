@echo off
REM SenseVoice launcher (Python 3.12 environment)

call conda activate sensevoice
if errorlevel 1 (
    echo Error: sensevoice environment not found.
    echo Please run setup_python312_env.bat first.
    pause
    exit /b 1
)

start "" pythonw main.py
