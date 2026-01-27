@echo off
echo Starting SenseVoice Subtitle Generator...
python main.py
if errorlevel 1 (
    echo.
    echo [ERROR] An error occurred while running the program.
    echo Please run install.bat first to install required packages.
    pause
)
