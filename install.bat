@echo off
echo ========================================
echo SenseVoice Subtitle Generator - Install
echo ========================================
echo.

:: Check Python version
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed.
    echo Please install Python 3.8 or higher: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/5] Upgrading pip...
python -m pip install --upgrade pip

echo.
echo [2/5] Installing basic packages (PyQt5, ffmpeg-python, pydub)...
pip install PyQt5 ffmpeg-python pydub
if errorlevel 1 (
    echo [ERROR] Basic package installation failed
    pause
    exit /b 1
)

echo.
echo [3/5] Installing editdistance alternative (python-Levenshtein)...
pip install python-Levenshtein

echo.
echo [4/5] Installing FunASR without dependencies...
pip install --no-deps funasr

echo.
echo [5/5] Installing FunASR dependencies...
pip install modelscope kaldiio librosa soundfile torch_complex tensorboardX
pip install umap-learn onnxruntime-gpu sentencepiece typeguard rotary_embedding_torch
pip install hydra-core jaconv jamo jieba oss2 pytorch-wpe

echo.
echo Patching FunASR to use Levenshtein instead of editdistance...
python patch_funasr.py

echo.
echo Checking FFmpeg...
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] FFmpeg is not installed.
    echo Please install FFmpeg: https://ffmpeg.org/download.html
    echo After installation, add FFmpeg to system PATH.
    echo.
) else (
    echo [OK] FFmpeg is installed.
)

echo.
echo Creating directory structure...
if not exist "logs" mkdir logs
if not exist "temp" mkdir temp

echo.
echo Checking CUDA availability...
python -c "import torch; print('CUDA Available:', torch.cuda.is_available()); print('PyTorch Version:', torch.__version__)" 2>nul

echo.
echo ========================================
echo Installation completed!
echo ========================================
echo.
echo To run the program, execute run.bat or type:
echo   python main.py
echo.
pause
