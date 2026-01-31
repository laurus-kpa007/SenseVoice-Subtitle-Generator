@echo off
echo ========================================
echo Creating Portable SenseVoice Package
echo ========================================
echo.

echo [1/4] Activating environment...
call C:\Users\lauru\miniconda3\Scripts\activate.bat C:\Users\lauru\miniconda3\envs\sensevoice

echo.
echo [2/4] Installing PyInstaller...
pip install pyinstaller

echo.
echo [3/4] Creating executable...
pyinstaller --name="SenseVoice" ^
  --windowed ^
  --onedir ^
  --icon=NONE ^
  --add-data "*.py;." ^
  --hidden-import=funasr ^
  --hidden-import=modelscope ^
  --hidden-import=librosa ^
  --hidden-import=soundfile ^
  --hidden-import=torch ^
  --hidden-import=torchaudio ^
  --collect-all funasr ^
  --collect-all modelscope ^
  --collect-all librosa ^
  main.py

echo.
echo [4/4] Creating portable package...
mkdir portable_sensevoice 2>nul
xcopy /E /I /Y dist\SenseVoice portable_sensevoice\SenseVoice
copy README.md portable_sensevoice\ 2>nul

echo.
echo ========================================
echo Portable package created!
echo ========================================
echo.
echo Location: portable_sensevoice\
echo Size: ~3-5GB (includes Python + PyTorch + models cache)
echo.
echo To distribute:
echo 1. Compress portable_sensevoice folder to ZIP
echo 2. Users extract and run SenseVoice\SenseVoice.exe
echo.
echo Note: Models will be downloaded on first run (~500MB)
echo.
pause
