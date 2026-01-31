@echo off
echo ========================================
echo Creating Embedded Python Package
echo ========================================
echo.
echo This creates a portable package using Python Embedded.
echo.

echo Step 1: Download Python 3.12 Embedded
echo Visit: https://www.python.org/downloads/windows/
echo Download: Windows embeddable package (64-bit) - Python 3.12
echo Extract to: .\python_embedded\
echo.
echo Step 2: After extracting Python, press any key to continue...
pause

echo.
echo [1/4] Configuring embedded Python...
cd python_embedded
echo import site > python312._pth
echo Lib\site-packages >> python312._pth

echo.
echo [2/4] Installing pip...
curl -O https://bootstrap.pypa.io/get-pip.py
.\python.exe get-pip.py

echo.
echo [3/4] Installing dependencies (this will take 10-20 minutes)...
.\python.exe -m pip install PyQt5 ffmpeg-python pydub librosa soundfile numpy
.\python.exe -m pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu124
.\python.exe -m pip install -U funasr modelscope python-Levenshtein

echo.
echo [4/4] Creating package structure...
cd ..
mkdir portable_embedded 2>nul
xcopy /E /I /Y python_embedded portable_embedded\python
xcopy /Y *.py portable_embedded\
copy README.md portable_embedded\ 2>nul

rem Create launcher
(
echo @echo off
echo cd /d "%%~dp0"
echo start "" "%%~dp0python\pythonw.exe" main.py
) > portable_embedded\SenseVoice.bat

echo.
echo ========================================
echo Embedded package created!
echo ========================================
echo.
echo Location: portable_embedded\
echo Size: ~2-3GB
echo.
pause
