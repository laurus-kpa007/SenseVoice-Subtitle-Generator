@echo off
echo ========================================
echo PyTorch Nightly Installation (CUDA 12.4)
echo ========================================
echo.
echo This will install the latest nightly build of PyTorch
echo which may support RTX 5070 Ti (sm_120 architecture).
echo.
echo Press Ctrl+C to cancel, or
pause

echo.
echo [1/2] Activating sensevoice environment...
call C:\Users\lauru\miniconda3\Scripts\activate.bat C:\Users\lauru\miniconda3\envs\sensevoice
if errorlevel 1 (
    echo Error: Failed to activate sensevoice environment
    echo Please run setup_python312_env.bat first
    pause
    exit /b 1
)

echo.
echo [2/2] Installing PyTorch nightly with CUDA 12.4...
pip uninstall -y torch torchaudio
pip install --pre torch torchaudio --index-url https://download.pytorch.org/whl/nightly/cu124

echo.
echo ========================================
echo Testing installation...
echo ========================================
python -c "import torch; print('PyTorch version:', torch.__version__); print('CUDA available:', torch.cuda.is_available()); print('CUDA version:', torch.version.cuda if torch.cuda.is_available() else 'N/A'); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A'); print('Compute capability:', torch.cuda.get_device_capability(0) if torch.cuda.is_available() else 'N/A')"

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo If CUDA is available and no warnings appear, GPU acceleration is ready.
echo Run start_with_conda.bat to launch SenseVoice with GPU support.
echo.
pause
