@echo off
echo ========================================
echo Creating Conda Portable Package
echo ========================================
echo.

echo [1/3] Installing conda-pack...
call C:\Users\lauru\miniconda3\Scripts\activate.bat base
pip install conda-pack

echo.
echo [2/3] Packing sensevoice environment...
conda pack -n sensevoice -o sensevoice_env.tar.gz

echo.
echo [3/3] Creating portable structure...
mkdir portable_conda_sensevoice 2>nul
mkdir portable_conda_sensevoice\env 2>nul
mkdir portable_conda_sensevoice\app 2>nul

rem Extract environment
tar -xzf sensevoice_env.tar.gz -C portable_conda_sensevoice\env

rem Copy application files
xcopy /E /Y *.py portable_conda_sensevoice\app\
xcopy /E /Y *.bat portable_conda_sensevoice\app\
copy README.md portable_conda_sensevoice\ 2>nul

rem Create launcher
(
echo @echo off
echo set ROOT=%%~dp0
echo call "%%ROOT%%env\Scripts\activate.bat"
echo cd "%%ROOT%%app"
echo pythonw main.py
) > portable_conda_sensevoice\SenseVoice.bat

echo.
echo ========================================
echo Portable conda package created!
echo ========================================
echo.
echo Location: portable_conda_sensevoice\
echo Size: ~6-8GB (full Python environment)
echo.
echo To distribute:
echo 1. Compress portable_conda_sensevoice to ZIP
echo 2. Users extract and run SenseVoice.bat
echo.
pause
