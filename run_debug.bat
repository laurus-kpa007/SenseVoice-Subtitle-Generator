@echo off
echo Running with debug output...
python main.py 2>&1 | tee debug_output.txt
pause
