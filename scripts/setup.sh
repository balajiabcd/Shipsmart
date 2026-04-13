#!/bin/bash
# Shipsmart Setup Script for Linux/Mac

echo "========================================"
echo "Shipsmart Environment Setup"
echo "========================================"

# Check Python version
python3 --version || {
    echo "Python not found. Please install Python 3.10+"
    exit 1
}

echo "[1/6] Creating virtual environment..."
python3 -m venv venv

echo "[2/6] Activating virtual environment..."
source venv/bin/activate

echo "[3/6] Upgrading pip..."
pip install --upgrade pip wheel setuptools

echo "[4/6] Installing dependencies..."
pip install -r requirements.txt

echo "[5/6] Copying environment file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "WARNING: Please edit .env with your API keys"
fi

echo "[6/6] Verifying installation..."
python -c "import pandas; import sklearn; import xgboost; print('OK')"

echo "========================================"
echo "Setup complete!"
echo ""
echo "To activate the environment:"
echo "  source venv/bin/activate"
echo ""
echo "To start the API:"
echo "  uvicorn src.api.main:app --reload"
echo "========================================"