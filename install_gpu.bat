@echo off
echo ========================================
echo GPU Acceleration Setup for SenseVoice
echo RTX 5070 Ti (CUDA 12.4+ Required)
echo ========================================
echo.
echo This will install PyTorch with latest CUDA support
echo.

echo [1/3] Uninstalling old PyTorch...
pip uninstall torch torchaudio -y

echo.
echo [2/3] Installing PyTorch with CUDA 12.4...
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu124

echo.
echo [3/3] Verifying installation...
python -c "import torch; print(f'\nPyTorch: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA version: {torch.version.cuda}'); gpu = torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A'; print(f'GPU: {gpu}'); print('\nTesting GPU...'); test = torch.zeros(1).cuda() if torch.cuda.is_available() else None; print('GPU test passed!' if test is not None else 'GPU not available')"

echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.
echo Now run: python main.py
echo.
pause
