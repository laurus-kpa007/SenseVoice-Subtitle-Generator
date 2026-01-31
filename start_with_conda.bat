@echo off
echo Activating sensevoice environment...
call C:\Users\lauru\miniconda3\Scripts\activate.bat C:\Users\lauru\miniconda3\envs\sensevoice
if errorlevel 1 (
    echo Error: Failed to activate sensevoice environment
    pause
    exit /b 1
)

echo Starting SenseVoice GUI...
python main.py

pause
