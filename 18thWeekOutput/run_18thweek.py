"""
run_18thweek.py
Universal cross-platform launcher & pre-flight verification system for the
UPHSD CCS 18-Week OBE Microservice Interactive Studio (Lesson 5 Milestones 1 & 2).

Authors:
- Christian Ezekiel L. Carvajal (Lead Systems Architect & Engineer)
- John Miko P. Sarsalijo (Collaborative Partner & Systems Engineer)

Features:
 1. Verifies Python runtime (>= 3.10).
 2. Checks package dependencies (pydantic, jinja2, requests, ollama).
 3. Verifies local Ollama service & 'qwen3.5:4b' model availability.
 4. Launches 18-Week Studio on http://127.0.0.1:8001 and opens the browser.
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
REQUIRED_PACKAGES = ["pydantic>=2.0.0", "jinja2>=3.1.0", "requests>=2.28.0", "ollama>=0.2.0"]
MODEL_TAG = "qwen3.5:4b"
HOST = "127.0.0.1"
PORT = 8001


def print_banner():
    banner = f"""
======================================================================
   UPHSD CCS - OBE 18-Week Microservice Studio (Lesson 5)
   Course: BSCS 3112 / Artificial Intelligence (Milestones 1 & 2)
   Students: Christian Ezekiel L. Carvajal & John Miko P. Sarsalijo
   Evaluator: Prof. Roberto L. Malitao
   Model Architecture: Strictly locked to qwen3.5:4b
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
    except Exception:
        missing.append("pydantic")
    try:
        import jinja2
    except Exception:
        missing.append("jinja2")
    try:
        import requests
    except Exception:
        missing.append("requests")
    try:
        import ollama
    except Exception:
        missing.append("ollama")

    if missing:
        print(f"[!] Missing packages detected: {', '.join(missing)}")
        print("[*] Installing required packages via pip...")
        cmd = [sys.executable, "-m", "pip", "install"] + REQUIRED_PACKAGES
        try:
            subprocess.check_call(cmd)
            print("[+] Dependencies successfully installed.")
        except Exception as e:
            print(f"[-] Error installing dependencies: {e}")
            sys.exit(1)
    else:
        print("[+] All Python dependencies (pydantic, jinja2, requests, ollama) are installed.")


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
                    subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                for _ in range(10):
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
        print("          launch Ollama in another window: ollama serve")
        print("          NOTE: The GUI Studio will still launch, allowing full review,")
        print("          CLO editing, and HTML syllabus export of existing courses.")
        print("=" * 70)
        return

    print("[+] Ollama service is active and responsive.")

    models = [m.get("name", "") for m in data.get("models", [])]
    model_installed = any(m.startswith(MODEL_TAG) or MODEL_TAG in m for m in models)

    if not model_installed:
        print(f"[!] Required model '{MODEL_TAG}' was not found in local Ollama repository.")
        print(f"[*] Pulling '{MODEL_TAG}' now...")
        try:
            subprocess.run(["ollama", "pull", MODEL_TAG], check=True)
            print(f"[+] Model '{MODEL_TAG}' downloaded and ready.")
        except Exception as e:
            print(f"[-] Error auto-pulling '{MODEL_TAG}': {e}")
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
    print("  LAUNCHING 18-WEEK OBE MICROSERVICE INTERACTIVE STUDIO")
    print(f"  URL: http://{HOST}:{PORT}")
    print("  Curriculum Subjects: 8 Official 3rd-Year CS Courses Pre-Loaded")
    print("  Launcher Command: python run_18thweek.py")
    print("  Press Ctrl+C in this console to terminate the server.")
    print("=" * 70 + "\n")

    if str(BASE_DIR) not in sys.path:
        sys.path.insert(0, str(BASE_DIR))

    from app import start_server
    should_open = "--no-browser" not in sys.argv
    start_server(open_browser=should_open)


if __name__ == "__main__":
    main()
