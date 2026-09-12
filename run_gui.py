"""
run_gui.py
Universal cross-platform launcher & pre-flight verification system for the
UPHSD CCS OBE AI Microservice Interactive Studio.

Performs automatic environment verification:
 1. Verifies Python runtime (>= 3.10).
 2. Checks and auto-installs required packages (pydantic, ollama) from requirements.txt.
 3. Verifies Ollama local connectivity (http://127.0.0.1:11434).
    - If CLI is detected but daemon is offline, attempts auto-start via 'ollama serve'.
 4. Verifies local installation of 'qwen3.5:4b' model.
    - If missing, automatically triggers 'ollama pull qwen3.5:4b'.
 5. Launches Web GUI Studio via app.py and opens the default web browser.

Usage:
  python run_gui.py                 # Full launch with browser
  python run_gui.py --no-browser    # Launch server without opening browser
  python run_gui.py --check-only    # Perform verification check only and exit
"""
import sys
import os
import shutil
import subprocess
import time
import urllib.request
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
REQUIRED_PACKAGES = ["pydantic>=2.0.0", "ollama>=0.2.0"]
MODEL_TAG = "qwen3.5:4b"
HOST = "127.0.0.1"
PORT = 8000

def print_banner():
    banner = f"""
======================================================================
   UPHSD CCS - OBE AI Microservice Interactive Studio
   Course: BSCS 3112 / Artificial Intelligence
   Student: Christian Ezekiel L. Carvajal
   Evaluator: Prof. Roberto L. Malitao
======================================================================
"""
    print(banner.strip())
    print()

def check_python_version():
    print(f"[*] Checking Python environment: {sys.version.split()[0]} ({sys.executable})")
    if sys.version_info < (3, 10):
        print(f"[!] Warning: Python 3.10+ is recommended. Running on {sys.version.split()[0]}.")
    else:
        print("[+] Python version is compatible.")

def check_and_install_dependencies():
    print("[*] Verifying Python package dependencies...")
    missing = []
    try:
        import pydantic
    except ImportError:
        missing.append("pydantic")
    try:
        import ollama
    except ImportError:
        missing.append("ollama")

    if missing:
        print(f"[!] Missing packages detected: {', '.join(missing)}")
        print("[*] Installing required packages via pip...")
        req_file = BASE_DIR / "requirements.txt"
        cmd = [sys.executable, "-m", "pip", "install"]
        if req_file.exists():
            cmd += ["-r", str(req_file)]
        else:
            cmd += REQUIRED_PACKAGES
        try:
            subprocess.check_call(cmd)
            print("[+] Dependencies successfully installed.")
        except Exception as e:
            print(f"[-] Error installing dependencies: {e}")
            print("    Please run: pip install -r requirements.txt")
            sys.exit(1)
    else:
        print("[+] All Python dependencies (pydantic, ollama) are installed.")

def check_ollama_and_model():
    print(f"[*] Checking Ollama service and '{MODEL_TAG}' model availability...")
    tags_url = "http://127.0.0.1:11434/api/tags"
    ollama_online = False
    model_installed = False

    def ping_ollama():
        try:
            req = urllib.request.Request(tags_url, headers={"User-Agent": "UPHSD-OBE-Bootstrap"})
            with urllib.request.urlopen(req, timeout=2.5) as resp:
                if resp.status == 200:
                    return json.loads(resp.read().decode("utf-8"))
        except Exception:
            return None
        return None

    data = ping_ollama()
    if data is not None:
        ollama_online = True
    else:
        # Check if ollama CLI is available
        ollama_bin = shutil.which("ollama")
        if ollama_bin:
            print("[!] Ollama daemon is not responding. Attempting to start background service (ollama serve)...")
            try:
                if sys.platform == "win32":
                    subprocess.Popen(
                        ["ollama", "serve"],
                        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
                    )
                else:
                    subprocess.Popen(
                        ["ollama", "serve"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                # Poll for up to 6 seconds
                for _ in range(12):
                    time.sleep(0.5)
                    data = ping_ollama()
                    if data is not None:
                        ollama_online = True
                        break
            except Exception as e:
                print(f"[-] Could not auto-start ollama serve: {e}")

    if not ollama_online:
        print("=" * 70)
        print("[WARNING] Ollama service is not reachable at http://127.0.0.1:11434.")
        print("          If you wish to perform live AI syllabus generation, please")
        print("          install and launch Ollama from: https://ollama.com")
        print("          NOTE: The GUI Studio will still launch, allowing full audit")
        print("          and PDF export of cached syllabi without Ollama running.")
        print("=" * 70)
        return

    print("[+] Ollama service is active and responsive.")

    # Check model list
    models = [m.get("name", "") for m in data.get("models", [])]
    model_installed = any(m.startswith(MODEL_TAG) or MODEL_TAG in m for m in models)

    if not model_installed:
        print(f"[!] Required model '{MODEL_TAG}' was not found in local Ollama repository.")
        print(f"[*] Pulling '{MODEL_TAG}' now (this may take a few minutes depending on connection)...")
        try:
            subprocess.run(["ollama", "pull", MODEL_TAG], check=True)
            print(f"[+] Model '{MODEL_TAG}' downloaded and ready.")
        except Exception as e:
            print(f"[-] Error auto-pulling '{MODEL_TAG}': {e}")
            print(f"    You can manually pull it by running: ollama pull {MODEL_TAG}")
    else:
        print(f"[+] Model '{MODEL_TAG}' is verified and ready for live generation.")

def main():
    print_banner()
    check_python_version()
    check_and_install_dependencies()
    check_ollama_and_model()

    if "--check-only" in sys.argv:
        print("\n[+] Pre-flight verification completed successfully.")
        return

    print("\n" + "=" * 70)
    print("  LAUNCHING OBE AI MICROSERVICE INTERACTIVE STUDIO")
    print(f"  URL: http://{HOST}:{PORT}")
    print("  Press Ctrl+C in this console to terminate the server.")
    print("=" * 70 + "\n")

    # Add BASE_DIR to sys.path
    if str(BASE_DIR) not in sys.path:
        sys.path.insert(0, str(BASE_DIR))

    from app import start_server
    should_open = "--no-browser" not in sys.argv
    start_server(open_browser=should_open)

if __name__ == "__main__":
    main()
