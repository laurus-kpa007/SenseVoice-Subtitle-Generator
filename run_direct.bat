@echo off
call C:\Users\lauru\miniconda3\Scripts\activate.bat sensevoice
if errorlevel 1 (
    echo Error: sensevoice environment not found.
    echo Please run setup_python312_env.bat first.
    pause
    exit /b 1
)
start "" pythonw main.py
