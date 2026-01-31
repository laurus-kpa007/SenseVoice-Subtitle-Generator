@echo off
echo Testing Python environment...
call C:\Users\lauru\miniconda3\Scripts\activate.bat C:\Users\lauru\miniconda3\envs\sensevoice

echo.
echo Python location:
where python

echo.
echo Python version:
python --version

echo.
echo PyTorch location:
python -c "import torch; print(torch.__file__)"

echo.
echo PyTorch version:
python -c "import torch; print('PyTorch:', torch.__version__); print('CUDA:', torch.cuda.is_available())"

pause
