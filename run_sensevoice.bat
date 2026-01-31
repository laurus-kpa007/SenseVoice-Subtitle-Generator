@echo off
REM SenseVoice 실행 스크립트 (Python 3.12 환경)

call conda activate sensevoice
if errorlevel 1 (
    echo 오류: sensevoice 환경이 없습니다.
    echo setup_python312_env.bat 를 먼저 실행하세요.
    pause
    exit /b 1
)

start "" pythonw main.py
