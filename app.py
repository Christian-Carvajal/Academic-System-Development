"""
app.py — Interactive Web GUI & REST API Server for OBE AI Microservice
Uses Python Standard Library (ThreadingHTTPServer) — Zero additional dependencies required.
"""
import json
import os
import sys
import threading
import urllib.request
import urllib.error
import webbrowser
from http import HTTPStatus
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path

# Ensure local directory is on sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from obe_schemas import CourseOutcomesPayload, FullSyllabusPayload
from lab1_1_generator import generate_course_outcomes
from lab1_2_pipeline import generate_weekly_schedule

PORT = 8000
HOST = "127.0.0.1"

# In-memory background generation state
generation_state = {
    "stage": None,       # "stage1" or "stage2"
    "status": "idle",    # "idle", "running", "success", "error"
    "message": "",
    "attempt": 0,
    "result": None,
    "error": None
}

def check_ollama_status():
    """Checks if Ollama daemon is active and if qwen3.5:4b is present."""
    status = {"running": False, "has_model": False, "models": []}
    try:
        req = urllib.request.Request("http://127.0.0.1:11434/api/tags")
        with urllib.request.urlopen(req, timeout=2.0) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                status["running"] = True
                model_names = [m.get("name", "") for m in data.get("models", [])]
                status["models"] = model_names
                status["has_model"] = any("qwen3.5:4b" in m for m in model_names)
    except Exception:
        pass
    return status

def run_stage1_worker(course_data):
    global generation_state
    generation_state["stage"] = "stage1"
    generation_state["status"] = "running"
    generation_state["message"] = "Querying qwen3.5:4b with format='json' (Stage 1)..."
    generation_state["error"] = None
    try:
        payload = generate_course_outcomes(**course_data)
        out_file = BASE_DIR / "co_output_lab1_1.json"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(payload.model_dump_json(indent=2))
        generation_state["status"] = "success"
        generation_state["message"] = "Course Outcomes generated and validated successfully!"
        generation_state["result"] = payload.model_dump()
    except Exception as exc:
        generation_state["status"] = "error"
        generation_state["message"] = f"Stage 1 failed: {str(exc)}"
        generation_state["error"] = str(exc)

def run_stage2_worker():
    global generation_state
    generation_state["stage"] = "stage2"
    generation_state["status"] = "running"
    generation_state["message"] = "Generating 14-Week Schedule with Week 7/14 locks (Stage 2)..."
    generation_state["error"] = None
    try:
        co_file = BASE_DIR / "co_output_lab1_1.json"
        if not co_file.exists():
            raise FileNotFoundError("co_output_lab1_1.json not found. Run Stage 1 first.")
        with open(co_file, "r", encoding="utf-8") as f:
            co_payload = CourseOutcomesPayload(**json.load(f))
        
        syllabus = generate_weekly_schedule(co_payload)
        out_file = BASE_DIR / "sample_output_syllabus.json"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(syllabus.model_dump_json(indent=2))
        generation_state["status"] = "success"
        generation_state["message"] = "14-Week Syllabus generated and validated successfully!"
        generation_state["result"] = syllabus.model_dump()
    except Exception as exc:
        generation_state["status"] = "error"
        generation_state["message"] = f"Stage 2 failed: {str(exc)}"
        generation_state["error"] = str(exc)

class OBEHttpHandler(BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(HTTPStatus.NO_CONTENT)
        self.end_headers()

    def send_json(self, status_code: int, data: dict):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?")[0]
        
        # Static index.html
        if path == "/" or path == "/index.html":
            index_file = BASE_DIR / "index.html"
            if index_file.exists():
                with open(index_file, "rb") as f:
                    content = f.read()
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return
            else:
                self.send_error(HTTPStatus.NOT_FOUND, "index.html not found.")
                return

        # API: Status
        if path == "/api/status":
            ollama_info = check_ollama_status()
            co_exists = (BASE_DIR / "co_output_lab1_1.json").exists()
            syllabus_exists = (BASE_DIR / "sample_output_syllabus.json").exists()
            self.send_json(200, {
                "ollama": ollama_info,
                "files": {
                    "co_output_lab1_1.json": co_exists,
                    "sample_output_syllabus.json": syllabus_exists
                },
                "generation_state": generation_state
            })
            return

        # API: Generation status polling
        if path == "/api/generation-status":
            self.send_json(200, generation_state)
            return

        # API: Get Stage 1 COs
        if path == "/api/co":
            co_file = BASE_DIR / "co_output_lab1_1.json"
            if co_file.exists():
                with open(co_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.send_json(200, {"success": True, "data": data})
            else:
                self.send_json(404, {"success": False, "error": "co_output_lab1_1.json does not exist."})
            return

        # API: Get Stage 2 Syllabus
        if path == "/api/syllabus":
            s_file = BASE_DIR / "sample_output_syllabus.json"
            if s_file.exists():
                with open(s_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.send_json(200, {"success": True, "data": data})
            else:
                self.send_json(404, {"success": False, "error": "sample_output_syllabus.json does not exist."})
            return

        # API: Run Rubric & Invariant Audit
        if path == "/api/audit":
            s_file = BASE_DIR / "sample_output_syllabus.json"
            if not s_file.exists():
                self.send_json(400, {"success": False, "error": "sample_output_syllabus.json not found."})
                return
            
            with open(s_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            weeks = data.get("weekly_schedule", [])
            cos = data.get("course_outcomes", [])
            gb = data.get("grading_breakdown", {})

            checks = []
            
            # Check 1: 14 Weeks
            c1 = len(weeks) == 14
            checks.append({
                "id": "14_weeks",
                "label": "Strict 14-Week Total Schedule",
                "passed": c1,
                "detail": f"Found {len(weeks)} of 14 weeks"
            })

            # Check 2: Week 7 Midterm
            w7 = next((w for w in weeks if w.get("week_number") == 7), {})
            c2 = "midterm" in w7.get("topic", "").lower() and w7.get("period") == "MIDTERM"
            checks.append({
                "id": "w7_midterm",
                "label": "Week 7 Midterm Exam Milestone Lock",
                "passed": c2,
                "detail": f"Topic: '{w7.get('topic', '')}' | Period: '{w7.get('period', '')}'"
            })

            # Check 3: Week 14 Final
            w14 = next((w for w in weeks if w.get("week_number") == 14), {})
            c3 = "final" in w14.get("topic", "").lower() and w14.get("period") == "FINAL"
            checks.append({
                "id": "w14_final",
                "label": "Week 14 Final Exam / Capstone Defense Lock",
                "passed": c3,
                "detail": f"Topic: '{w14.get('topic', '')}' | Period: '{w14.get('period', '')}'"
            })

            # Check 4: Tripartite K/S/A in instructional weeks
            tripartite_ok = True
            for w in weeks:
                llos = w.get("llos", [])
                cats = {l.get("category") for l in llos}
                if cats != {"K", "S", "A"}:
                    tripartite_ok = False
                    break
            checks.append({
                "id": "tripartite_ksa",
                "label": "Tripartite Outcomes (1 K, 1 S, 1 A) Every Week",
                "passed": tripartite_ok,
                "detail": "Every week has verified Knowledge, Skills, and Attitude outcomes" if tripartite_ok else "One or more weeks missing K/S/A categories"
            })

            # Check 5: 100% CLO Coverage
            clo_ids = {c.get("clo_number") for c in cos}
            covered = set()
            for w in weeks:
                covered.update(w.get("aligned_co", []))
            coverage_ok = clo_ids.issubset(covered)
            checks.append({
                "id": "clo_coverage",
                "label": "100% Course Outcome Schedule Alignment",
                "passed": coverage_ok,
                "detail": f"Covered CLO IDs: {sorted(list(covered))} of {sorted(list(clo_ids))}"
            })

            # Check 6: UPHSD Institutional Grading
            grading_ok = (
                gb.get("class_standing_weight") == 70.0 and
                gb.get("major_exam_weight") == 30.0 and
                gb.get("quizzes_pct") == 30.0 and
                gb.get("research_pct") == 20.0 and
                gb.get("seatwork_lab_pct") == 50.0
            )
            checks.append({
                "id": "uphsd_grading",
                "label": "UPHSD CCS Institutional Grading Breakdown",
                "passed": grading_ok,
                "detail": "70% Class Standing (30Q / 20R / 50L) + 30% Major Exam"
            })

            all_passed = all(c["passed"] for c in checks)
            self.send_json(200, {
                "success": True,
                "all_passed": all_passed,
                "checks": checks
            })
            return

        self.send_error(HTTPStatus.NOT_FOUND, f"Endpoint {path} not found.")

    def do_POST(self):
        path = self.path.split("?")[0]
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
        
        try:
            req_data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            req_data = {}

        # POST /api/generate-co
        if path == "/api/generate-co":
            if generation_state["status"] == "running":
                self.send_json(409, {"success": False, "error": "A generation task is already in progress."})
                return
            
            course_data = {
                "course_title": req_data.get("course_title", "Data Structures and Algorithms"),
                "course_code": req_data.get("course_code", "CS 3110"),
                "description": req_data.get("description", "Fundamental data structures, recursive algorithms, and complexity analysis."),
                "target_pos": req_data.get("target_pos", "PLO 1 (Computing Knowledge), PLO 2 (Problem Analysis), PLO 3 (Systems Development)")
            }
            threading.Thread(target=run_stage1_worker, args=(course_data,), daemon=True).start()
            self.send_json(202, {"success": True, "message": "Stage 1 generation started."})
            return

        # POST /api/generate-syllabus
        if path == "/api/generate-syllabus":
            if generation_state["status"] == "running":
                self.send_json(409, {"success": False, "error": "A generation task is already in progress."})
                return
            
            threading.Thread(target=run_stage2_worker, daemon=True).start()
            self.send_json(202, {"success": True, "message": "Stage 2 generation started."})
            return

        self.send_error(HTTPStatus.NOT_FOUND, f"Endpoint {path} not found.")

def start_server(open_browser=True):
    server_address = (HOST, PORT)
    httpd = ThreadingHTTPServer(server_address, OBEHttpHandler)
    url = f"http://{HOST}:{PORT}"
    print("=" * 70)
    print("  UPHSD CCS - OBE AI Microservice Interactive Studio")
    print(f"  Local Web Interface: {url}")
    print("  Press Ctrl+C in terminal to stop server.")
    print("=" * 70)

    if open_browser:
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Server shutting down cleanly.")
        httpd.server_close()

if __name__ == "__main__":
    should_open = "--no-browser" not in sys.argv
    start_server(open_browser=should_open)
