@echo off
echo ========================================
echo Python 3.12 환경 설정 (Conda)
echo ========================================
echo.

echo [1/5] Python 3.12 환경 생성 중...
conda create -n sensevoice python=3.12 -y

echo.
echo [2/5] 환경 활성화...
call conda activate sensevoice

echo.
echo [3/5] 기본 패키지 설치...
pip install PyQt5 ffmpeg-python pydub librosa soundfile numpy

echo.
echo [4/5] GPU 지원 PyTorch 설치...
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu121

echo.
echo [5/5] FunASR 및 ModelScope 설치...
pip install -U funasr modelscope python-Levenshtein

echo.
echo ========================================
echo 설치 완료!
echo ========================================
echo.
echo 다음부터 실행 방법:
echo 1. conda activate sensevoice
echo 2. pythonw main.py
echo.
echo 또는 run_sensevoice.bat 실행
echo.
pause
