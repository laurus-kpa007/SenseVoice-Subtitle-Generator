@echo off
echo ========================================
echo GPU Acceleration Setup for SenseVoice
echo ========================================
echo.
echo This will install PyTorch with CUDA support for NVIDIA RTX 5070 Ti
echo.

echo [1/3] Uninstalling CPU-only PyTorch (if exists)...
pip uninstall torch torchaudio -y

echo.
echo [2/3] Installing PyTorch with CUDA 12.1 support...
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu121

echo.
echo [3/3] Verifying CUDA installation...
python -c "import torch; print(f'\nPyTorch: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA version: {torch.version.cuda}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}')"

echo.
echo ========================================
echo GPU setup complete!
echo ========================================
echo.
echo Press any key to exit...
pause >nul
