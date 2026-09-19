#!/usr/bin/env bash
# ======================================================================
# UPHSD CCS - OBE AI Microservice Environment Setup (Linux / macOS / WSL)
# Evaluator: Prof. Roberto L. Malitao
# Student: Christian Ezekiel L. Carvajal
# ======================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "======================================================================"
echo "  UPHSD CCS - OBE AI Studio Environment Setup"
echo "======================================================================"

# Step 1: Virtual Environment Setup
if [ ! -d ".venv" ]; then
    echo "[*] Creating isolated Python virtual environment (.venv)..."
    if command -v python3 &> /dev/null; then
        python3 -m venv .venv
    else
        python -m venv .venv
    fi
fi

# Step 2: Activate virtual environment
echo "[*] Activating virtual environment..."
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
elif [ -f ".venv/Scripts/activate" ]; then
    source .venv/Scripts/activate
fi

# Step 3: Install dependencies
echo "[*] Installing required dependencies (pydantic, ollama)..."
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
echo "[+] Python dependencies successfully installed."

# Step 4: Check Ollama & pull model
echo "[*] Checking Ollama installation and local service..."
if ! command -v ollama &> /dev/null; then
    echo "[!] Warning: Ollama CLI is not found in PATH."
    echo "    Please install Ollama from https://ollama.com if you wish to run local inference."
else
    echo "[+] Ollama CLI detected."
    echo "[*] Ensuring model 'qwen3.5:4b' is downloaded locally..."
    ollama pull qwen3.5:4b || true
    echo "[+] Model 'qwen3.5:4b' ready."
fi

echo ""
echo "======================================================================"
echo "  Setup complete! You can now start the studios with:"
echo "    18-Week Studio (Port 8001): cd 18thWeekOutput && python run_18thweek.py"
echo "    14-Week Studio (Port 8000): cd 14thWeekOutput && python run_14thweek.py"
echo "======================================================================"
