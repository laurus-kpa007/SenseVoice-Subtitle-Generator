@echo off
echo ========================================
echo Python 3.12 Environment Setup (Conda)
echo ========================================
echo.

echo [1/5] Creating Python 3.12 environment...
conda create -n sensevoice python=3.12 -y

echo.
echo [2/5] Activating environment...
call conda activate sensevoice

echo.
echo [3/5] Installing basic packages...
pip install PyQt5 ffmpeg-python pydub librosa soundfile numpy

echo.
echo [4/5] Installing PyTorch with GPU support...
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu121

echo.
echo [5/5] Installing FunASR and ModelScope...
pip install -U funasr modelscope python-Levenshtein

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo How to run:
echo 1. conda activate sensevoice
echo 2. pythonw main.py
echo.
echo Or simply run: run_sensevoice.bat
echo.
pause
