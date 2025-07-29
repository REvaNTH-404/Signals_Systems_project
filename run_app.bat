@echo off
call .\.venv\Scripts\activate
pip install --upgrade pip
pip install numpy matplotlib
python main.py
pause
