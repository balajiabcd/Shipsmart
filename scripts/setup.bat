@echo off
REM Shipsmart Setup Script for Windows

echo ========================================
echo Shipsmart Environment Setup
echo ========================================

REM Check Python version
python --version
if errorlevel 1 (
    echo Python not found. Please install Python 3.10+
    exit /b 1
)

echo [1/6] Creating virtual environment...
python -m venv venv

echo [2/6] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/6] Upgrading pip...
python -m pip install --upgrade pip wheel setuptools

echo [4/6] Installing dependencies...
pip install -r requirements.txt

echo [5/6] Copying environment file...
if not exist .env (
    copy .env.example .env
    echo WARNING: Please edit .env with your API keys
)

echo [6/6] Verifying installation...
python -c "import pandas; import sklearn; import xgboost; print('OK')"

echo ========================================
echo Setup complete!
echo.
echo To activate the environment:
echo   venv\Scripts\activate
echo.
echo To start the API:
echo   uvicorn src.api.main:app --reload
echo ========================================