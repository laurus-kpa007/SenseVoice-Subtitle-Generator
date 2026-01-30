@echo off
echo ========================================
echo NPU Support Setup (Experimental)
echo ========================================
echo.
echo Intel NPU support via DirectML (Windows only)
echo Note: This is experimental and may not work with all models
echo.

echo [1/2] Installing PyTorch with DirectML...
pip install torch-directml

echo.
echo [2/2] Verifying DirectML installation...
python -c "import torch_directml; print('DirectML installed successfully')"

echo.
echo ========================================
echo NPU setup complete!
echo Note: To use NPU, set device='privateuseone' in code
echo ========================================
echo.
echo Press any key to exit...
pause >nul
