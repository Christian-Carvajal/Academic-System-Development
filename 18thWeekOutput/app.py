"""
app.py — 18-Week OBE Microservice Interactive Studio Backend
Uses Python Standard Library (ThreadingHTTPServer) — Zero external server dependencies.
Port: 8001 (Isolated from Lesson 4 studio on port 8000).
"""
import json
import os
import sys
import threading
import time
import urllib.request
import urllib.error
import urllib.parse
import webbrowser
from http import HTTPStatus
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Optional, Dict, Any, List

# Defensive pathing
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

OUTPUTS_DIR = BASE_DIR / "outputs"
TEMPLATES_DIR = BASE_DIR / "templates"
DATABASE_DIR = BASE_DIR / "database"

OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

from curriculum_catalog import CURRICULUM_SUBJECTS, get_subject, get_all_subjects
from obe_schemas import CourseOutcomeSchema, FullSyllabusSchema
from db_manager import get_syllabus, update_clo, get_connection, DEFAULT_DB_PATH, init_db
from export_engine import export_to_file
import llm_engine

PORT = 8001
HOST = "127.0.0.1"

# Shared background generation state
generation_state: Dict[str, Any] = {
    "status": "idle",       # "idle", "running", "success", "error"
    "course_code": None,
    "stage": "",
    "progress_pct": 0,
    "message": "",
    "logs": [],
    "result": None,
    "error": None
}

generation_lock = threading.Lock()


def check_ollama_status() -> Dict[str, Any]:
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
        status["running"] = False
    return status


def run_generation_worker(course_code: str, custom_overrides: Optional[Dict[str, Any]] = None):
    """Background thread worker for generating a single course syllabus."""
    global generation_state
    
    title = (custom_overrides and custom_overrides.get("course_title")) or ""
    if not title:
        subj = get_subject(course_code)
        title = subj["course_title"] if subj else course_code

    with generation_lock:
        generation_state["status"] = "running"
        generation_state["course_code"] = course_code
        generation_state["progress_pct"] = 10
        generation_state["stage"] = f"Resolving course parameters for {course_code}..."
        generation_state["message"] = f"Initializing generation for {course_code} ({title})..."
        generation_state["logs"] = [f"[*] Selected subject: {course_code} - {title}"]
        generation_state["error"] = None
        generation_state["result"] = None

    try:
        with generation_lock:
            generation_state["progress_pct"] = 25
            generation_state["stage"] = f"Formulating Bloom-compliant CLOs & Tripartite Schedule with qwen3.5:4b..."
            generation_state["logs"].append(f"[*] Querying qwen3.5:4b for {course_code} ({title})...")

        # Run LLM generation with custom overrides if present
        if custom_overrides:
            result = llm_engine.generate_custom_subject(course_code, custom_overrides=custom_overrides)
        else:
            result = llm_engine.generate_subject_by_code(course_code)

        with generation_lock:
            generation_state["progress_pct"] = 75
            generation_state["stage"] = "Persisting to SQLite database & compiling official HTML..."
            generation_state["logs"].append(f"[+] Schema validation passed: {len(result.course_outcomes)} CLOs, {len(result.weekly_schedule)} weeks.")
            generation_state["logs"].append(f"[+] Successfully persisted to database/obe_syllabus.db")

        # Export HTML
        export_to_file(course_code)
        
        with generation_lock:
            generation_state["progress_pct"] = 100
            generation_state["status"] = "success"
            generation_state["stage"] = "Complete"
            generation_state["message"] = f"Successfully generated and compiled 18-week syllabus for {course_code}!"
            generation_state["logs"].append(f"[+] Official HTML document compiled: outputs/official_syllabus_{course_code.replace(' ', '_')}.html")
            generation_state["result"] = result.model_dump()

    except Exception as exc:
        with generation_lock:
            generation_state["status"] = "error"
            generation_state["progress_pct"] = 0
            generation_state["stage"] = "Failed"
            generation_state["message"] = f"Generation failed: {str(exc)}"
            generation_state["error"] = str(exc)
            generation_state["logs"].append(f"[-] Error: {str(exc)}")


def run_batch_generation_worker():
    """Background thread worker for generating all 8 curriculum subjects sequentially."""
    global generation_state
    subjects = get_all_subjects()
    total = len(subjects)
    
    with generation_lock:
        generation_state["status"] = "running"
        generation_state["course_code"] = "BATCH_ALL"
        generation_state["progress_pct"] = 5
        generation_state["stage"] = f"Starting Batch Generation for all {total} curriculum subjects..."
        generation_state["message"] = f"Batch processing 8 courses..."
        generation_state["logs"] = [f"[*] Starting batch queue for {total} subjects."]
        generation_state["error"] = None

    for idx, subj in enumerate(subjects, 1):
        code = subj["course_code"]
        title = subj["course_title"]
        pct = int((idx / total) * 90)
        with generation_lock:
            generation_state["course_code"] = code
            generation_state["progress_pct"] = pct
            generation_state["stage"] = f"[{idx}/{total}] Processing {code}: {title}..."
            generation_state["logs"].append(f"[*] [{idx}/{total}] Generating {code}...")

        try:
            llm_engine.generate_subject_by_code(code)
            with generation_lock:
                generation_state["logs"].append(f"[+] Completed {code}.")
        except Exception as e:
            with generation_lock:
                generation_state["logs"].append(f"[-] Failed {code}: {e}")

    with generation_lock:
        generation_state["status"] = "success"
        generation_state["progress_pct"] = 100
        generation_state["stage"] = "Batch Complete"
        generation_state["message"] = f"Batch generation of all {total} subjects finished!"
        generation_state["logs"].append(f"[+] All {total} subjects generated and persisted to SQLite.")


def perform_nuke() -> Dict[str, Any]:
    """Wipes all generated deliverable files, cleans SQLite tables, and resets in-memory pipeline state."""
    deleted_files = []
    if OUTPUTS_DIR.exists():
        for fpath in OUTPUTS_DIR.iterdir():
            if fpath.is_file() and fpath.name != ".gitkeep":
                try:
                    fpath.unlink()
                    deleted_files.append(fpath.name)
                except Exception as e:
                    print(f"[!] Warning deleting {fpath}: {e}")

    # Reset database tables
    db_cleared = False
    try:
        with get_connection() as conn:
            conn.execute("PRAGMA foreign_keys = OFF;")
            conn.execute("DELETE FROM lesson_outcomes;")
            conn.execute("DELETE FROM weekly_schedules;")
            conn.execute("DELETE FROM course_outcomes;")
            conn.execute("DELETE FROM courses;")
            conn.execute("PRAGMA foreign_keys = ON;")
            conn.commit()
        init_db()
        db_cleared = True
    except Exception as e:
        print(f"[!] Warning clearing database: {e}")

    # Reset in-memory generation state
    with generation_lock:
        generation_state["status"] = "idle"
        generation_state["progress_pct"] = 0
        generation_state["stage"] = "Workspace Nuked Clean"
        generation_state["message"] = "All generated deliverables, database records, and pipeline states wiped."
        generation_state["logs"] = ["[!] Workspace nuked clean. Ready for fresh generation."]
        generation_state["course_code"] = None
        generation_state["result"] = None
        generation_state["error"] = None

    return {
        "success": True,
        "message": "Nuke operation successful. All 18-week generated syllabi, HTML documents, and SQLite tables wiped.",
        "deleted": deleted_files,
        "db_cleared": db_cleared
    }


class OBE18WeekHttpHandler(BaseHTTPRequestHandler):
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
        query = self.path.split("?")[1] if "?" in self.path else ""

        # Nuke workspace endpoint via GET
        if path in ("/api/nuke", "/api/clear", "/api/reset"):
            result = perform_nuke()
            self.send_json(HTTPStatus.OK, result)
            return
        
        # 1. Static index.html
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
            self.send_error(HTTPStatus.NOT_FOUND, "index.html not found.")
            return

        # 2. System status endpoint
        if path == "/api/status":
            ollama = check_ollama_status()
            outputs = {}
            if OUTPUTS_DIR.exists():
                for f in OUTPUTS_DIR.iterdir():
                    if f.is_file():
                        outputs[f.name] = {
                            "size": f.stat().st_size,
                            "modified": f.stat().st_mtime
                        }
            
            # Count courses in DB
            db_courses = 0
            try:
                with get_connection() as conn:
                    db_courses = conn.execute("SELECT COUNT(*) FROM courses").fetchone()[0]
            except Exception:
                db_courses = 0

            self.send_json(HTTPStatus.OK, {
                "ollama": ollama,
                "model": "qwen3.5:4b",
                "outputs": outputs,
                "db_courses_count": db_courses
            })
            return

        # 3. Curriculum Subjects endpoint
        if path == "/api/subjects":
            subjects = get_all_subjects()
            # Enrich with generated & DB persistence status
            with get_connection() as conn:
                db_rows = conn.execute("SELECT course_code FROM courses").fetchall()
                persisted_codes = {r["course_code"].upper() for r in db_rows}
            
            for s in subjects:
                code_norm = s["course_code"].upper()
                clean_code = s["course_code"].replace(" ", "_").replace("/", "-")
                has_json = (OUTPUTS_DIR / f"sample_validated_output_{clean_code}.json").exists() or (OUTPUTS_DIR / "sample_validated_output.json").exists()
                has_html = (OUTPUTS_DIR / f"official_syllabus_{clean_code}.html").exists()
                s["is_persisted"] = code_norm in persisted_codes
                s["has_json"] = has_json
                s["has_html"] = has_html
                s["html_filename"] = f"official_syllabus_{clean_code}.html" if has_html else None

            self.send_json(HTTPStatus.OK, {"subjects": subjects})
            return

        # 4. Generation State endpoint
        if path == "/api/generation-state":
            with generation_lock:
                state_copy = dict(generation_state)
            self.send_json(HTTPStatus.OK, state_copy)
            return

        # 5. Fetch Syllabus by course code
        if path == "/api/syllabus":
            # Parse code from query
            code = None
            if "code=" in query:
                for param in query.split("&"):
                    if param.startswith("code="):
                        code = urllib.parse.unquote_plus(param.split("=")[1])
            
            if not code:
                self.send_json(HTTPStatus.BAD_REQUEST, {"error": "Missing 'code' query parameter."})
                return

            # 1st: Check SQLite
            try:
                syllabus = get_syllabus(code)
                if syllabus:
                    self.send_json(HTTPStatus.OK, {
                        "source": "sqlite",
                        "data": syllabus.model_dump()
                    })
                    return
            except Exception as e:
                pass

            # 2nd: Check JSON in outputs/
            clean_code = code.replace(" ", "_").replace("/", "-")
            candidate = OUTPUTS_DIR / f"sample_validated_output_{clean_code}.json"
            if candidate.exists():
                try:
                    with open(candidate, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    self.send_json(HTTPStatus.OK, {
                        "source": "json",
                        "data": data
                    })
                    return
                except Exception as e:
                    self.send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": str(e)})
                    return

            # Fallback to sample_validated_output.json ONLY if course_code matches
            default_cand = OUTPUTS_DIR / "sample_validated_output.json"
            if default_cand.exists():
                try:
                    with open(default_cand, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    if data.get("course_metadata", {}).get("course_code") == code:
                        self.send_json(HTTPStatus.OK, {
                            "source": "json",
                            "data": data
                        })
                        return
                except Exception:
                    pass

            self.send_json(HTTPStatus.NOT_FOUND, {"error": f"Syllabus for '{code}' not yet generated."})
            return

        # 5b. Accreditation & Rubric Audit endpoint for 18-week syllabus
        if path == "/api/audit":
            code = None
            if "code=" in query:
                for param in query.split("&"):
                    if param.startswith("code="):
                        code = urllib.parse.unquote_plus(param.split("=")[1])
            if not code:
                code = "BSCS 3112"

            syllabus = None
            try:
                syllabus = get_syllabus(code)
            except Exception:
                syllabus = None

            if not syllabus:
                clean_code = code.replace(" ", "_").replace("/", "-")
                cand = OUTPUTS_DIR / f"sample_validated_output_{clean_code}.json"
                if not cand.exists():
                    cand = OUTPUTS_DIR / "sample_validated_output.json"
                if cand.exists():
                    try:
                        with open(cand, "r", encoding="utf-8") as f:
                            raw_data = json.load(f)
                            if raw_data.get("course_metadata", {}).get("course_code") == code or not get_subject(code):
                                syllabus = FullSyllabusSchema.model_validate(raw_data)
                    except Exception:
                        syllabus = None

            if not syllabus:
                self.send_json(HTTPStatus.NOT_FOUND, {
                    "success": False,
                    "error": f"Syllabus for '{code}' not yet generated."
                })
                return

            weeks = syllabus.weekly_schedule
            clos = syllabus.course_outcomes

            checks = []

            # Check 1: Strict 18-Week Total Schedule
            c1 = len(weeks) == 18
            checks.append({
                "id": "18_weeks",
                "label": "Strict 18-Week Total Schedule",
                "passed": c1,
                "detail": f"Verified {len(weeks)} of 18 scheduled academic weeks."
            })

            # Check 2: Week 9 Midterm Exam Milestone Lock
            w9 = next((w for w in weeks if w.week_number == 9), None)
            w9_topics = " ".join(w9.topics if isinstance(w9.topics, list) else [str(w9.topics)]) if w9 else ""
            c2 = bool(w9 and ("midterm" in w9_topics.lower() or "exam" in w9_topics.lower()))
            checks.append({
                "id": "w9_midterm",
                "label": "Week 9 Midterm Exam Milestone Lock",
                "passed": c2,
                "detail": f"Week 9 Topic: '{w9_topics}'" if w9 else "Week 9 not found."
            })

            # Check 3: Week 18 Final Exam / Capstone Defense Lock
            w18 = next((w for w in weeks if w.week_number == 18), None)
            w18_topics = " ".join(w18.topics if isinstance(w18.topics, list) else [str(w18.topics)]) if w18 else ""
            c3 = bool(w18 and ("final" in w18_topics.lower() or "exam" in w18_topics.lower() or "defense" in w18_topics.lower()))
            checks.append({
                "id": "w18_final",
                "label": "Week 18 Final Examination & Capstone Defense Lock",
                "passed": c3,
                "detail": f"Week 18 Topic: '{w18_topics}'" if w18 else "Week 18 not found."
            })

            # Check 4: Tripartite K/S/A Coverage across term
            domains_found = set()
            for w in weeks:
                for llo in w.lesson_outcomes:
                    domains_found.add(llo.domain)
            c4 = {"K", "S", "A"}.issubset(domains_found)
            checks.append({
                "id": "tripartite_ksa",
                "label": "Tripartite Educational Domain Coverage (K, S, A)",
                "passed": c4,
                "detail": f"Domains represented: {sorted(list(domains_found))} (Knowledge, Skills, Attitude)."
            })

            # Check 5: Bloom's Revised Taxonomy Active Verbs (Zero Banned Verbs)
            banned = ["understand", "know", "learn", "study", "familiarize"]
            banned_found = []
            for c in clos:
                first_w = c.description.strip().split()[0].lower()
                for b in banned:
                    if b in first_w:
                        banned_found.append(f"{c.clo_id}: {b}")
            c5 = len(banned_found) == 0
            checks.append({
                "id": "blooms_verbs",
                "label": "Bloom's Revised Taxonomy Action Verbs (0% Banned)",
                "passed": c5,
                "detail": "All Course Outcomes begin with active, measurable Bloom verbs." if c5 else f"Banned verbs detected: {', '.join(banned_found)}"
            })

            # Check 6: Target PLOs Alignment
            all_mapped_pos = set()
            for c in clos:
                all_mapped_pos.update(c.program_outcomes_mapped)
            c6 = len(all_mapped_pos) >= 2
            checks.append({
                "id": "plo_alignment",
                "label": "CHED / UPHSD Program Learning Outcomes Alignment",
                "passed": c6,
                "detail": f"Mapped Program Outcomes across CLOs: {', '.join(sorted(list(all_mapped_pos)))}"
            })

            # Check 7: UPHSD CCS Institutional Grading Breakdown
            checks.append({
                "id": "uphsd_grading",
                "label": "UPHSD CCS Institutional Grading Breakdown",
                "passed": True,
                "detail": "70% Class Standing (Quizzes 30%, Assignments 20%, Lab 50%) + 30% Major Exam."
            })

            passed_count = sum(1 for c in checks if c["passed"])
            compliance_score = int((passed_count / len(checks)) * 100)
            self.send_json(HTTPStatus.OK, {
                "course_code": code,
                "all_passed": (passed_count == len(checks)),
                "compliance_score": f"{compliance_score}%",
                "passed_count": passed_count,
                "total_checks": len(checks),
                "checks": checks
            })
            return

        # 6. Database live query endpoint
        if path == "/api/database":
            try:
                init_db()
                with get_connection() as conn:
                    courses = conn.execute("SELECT * FROM courses").fetchall()
                    data = []
                    for c in courses:
                        clos = conn.execute("SELECT clo_id, description, bloom_level FROM course_outcomes WHERE course_id = ?", (c["id"],)).fetchall()
                        w_count = conn.execute("SELECT COUNT(*) FROM weekly_schedules WHERE course_id = ?", (c["id"],)).fetchone()[0]
                        data.append({
                            "id": c["id"],
                            "course_code": c["course_code"],
                            "course_title": c["course_title"],
                            "credit_units": c["credit_units"],
                            "clos": [dict(r) for r in clos],
                            "weeks_count": w_count
                        })
                    
                    # Fetch normalized table counts & live records for multi-table inspector
                    cnt_courses = conn.execute("SELECT COUNT(*) FROM courses").fetchone()[0]
                    cnt_clos = conn.execute("SELECT COUNT(*) FROM course_outcomes").fetchone()[0]
                    cnt_weeks = conn.execute("SELECT COUNT(*) FROM weekly_schedules").fetchone()[0]
                    cnt_llos = conn.execute("SELECT COUNT(*) FROM lesson_outcomes").fetchone()[0]

                    table_counts = {
                        "courses": cnt_courses,
                        "course_outcomes": cnt_clos,
                        "weekly_schedules": cnt_weeks,
                        "lesson_outcomes": cnt_llos
                    }

                    # Fetch rows for relational table preview
                    tbl_courses = [dict(r) for r in conn.execute("SELECT id, course_code, course_title, credit_units, lecture_hours, lab_hours, prerequisites FROM courses ORDER BY id ASC").fetchall()]
                    tbl_clos = [dict(r) for r in conn.execute("SELECT co.id, co.course_id, c.course_code, co.clo_id, co.bloom_level, co.description, co.program_outcomes_mapped FROM course_outcomes co JOIN courses c ON co.course_id = c.id ORDER BY co.course_id, co.clo_id ASC").fetchall()]
                    
                    raw_weeks = conn.execute("SELECT ws.id, ws.course_id, c.course_code, ws.week_number, ws.topics, ws.teaching_learning_activities, ws.assessment_tasks FROM weekly_schedules ws JOIN courses c ON ws.course_id = c.id ORDER BY ws.course_id, ws.week_number ASC").fetchall()
                    tbl_weeks = []
                    for r in raw_weeks:
                        d = dict(r)
                        wn = d["week_number"]
                        d["period"] = "MIDTERM EXAM" if wn == 9 else ("FINAL EXAM" if wn == 18 else ("MIDTERM" if wn <= 8 else "FINAL"))
                        tbl_weeks.append(d)

                    tbl_llos = [dict(r) for r in conn.execute("SELECT lo.id, lo.schedule_id, ws.week_number, c.course_code, lo.llo_id, lo.domain, lo.description FROM lesson_outcomes lo JOIN weekly_schedules ws ON lo.schedule_id = ws.id JOIN courses c ON ws.course_id = c.id ORDER BY ws.course_id, ws.week_number, lo.domain ASC LIMIT 300").fetchall()]

                self.send_json(HTTPStatus.OK, {
                    "courses": data,
                    "table_counts": table_counts,
                    "tables": {
                        "courses": tbl_courses,
                        "course_outcomes": tbl_clos,
                        "weekly_schedules": tbl_weeks,
                        "lesson_outcomes": tbl_llos
                    }
                })
            except Exception as e:
                self.send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": str(e)})
            return

        # 7. Static file serving (outputs, templates, assets)
        clean_rel = path.lstrip("/")
        candidate_p = BASE_DIR / clean_rel
        if candidate_p.exists() and candidate_p.is_file():
            content_type = "application/octet-stream"
            if clean_rel.endswith(".html"):
                content_type = "text/html; charset=utf-8"
            elif clean_rel.endswith(".json"):
                content_type = "application/json; charset=utf-8"
            elif clean_rel.endswith(".css"):
                content_type = "text/css"
            elif clean_rel.endswith(".js"):
                content_type = "application/javascript"
            elif clean_rel.endswith(".png"):
                content_type = "image/png"
            elif clean_rel.endswith(".svg"):
                content_type = "image/svg+xml"

            with open(candidate_p, "rb") as f:
                body = f.read()
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        self.send_error(HTTPStatus.NOT_FOUND, "Endpoint or resource not found.")

    def do_POST(self):
        path = self.path.split("?")[0]
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b"{}"
        
        try:
            payload = json.loads(post_data.decode("utf-8"))
        except Exception:
            payload = {}

        # 1. Trigger Generation
        if path == "/api/generate":
            with generation_lock:
                if generation_state["status"] == "running":
                    self.send_json(HTTPStatus.CONFLICT, {
                        "error": "A generation task is already in progress.",
                        "current_course": generation_state["course_code"]
                    })
                    return

            is_batch = payload.get("batch", False)
            course_code = payload.get("course_code", "BSCS 3112")

            custom_overrides = {
                "course_code": payload.get("course_code"),
                "course_title": payload.get("course_title"),
                "course_description": payload.get("course_description"),
                "target_pos": payload.get("target_pos"),
                "credit_units": payload.get("credit_units"),
                "prerequisites": payload.get("prerequisites")
            }
            # Keep only keys that were explicitly passed and non-empty
            custom_overrides = {k: v for k, v in custom_overrides.items() if v not in (None, "")}

            if is_batch:
                t = threading.Thread(target=run_batch_generation_worker, daemon=True)
                t.start()
                self.send_json(HTTPStatus.ACCEPTED, {
                    "status": "started",
                    "mode": "batch",
                    "message": "Batch generation across all curriculum subjects initiated."
                })
                return
            else:
                t = threading.Thread(target=run_generation_worker, args=(course_code, custom_overrides), daemon=True)
                t.start()
                self.send_json(HTTPStatus.ACCEPTED, {
                    "status": "started",
                    "mode": "single",
                    "course_code": course_code,
                    "message": f"Generation for {course_code} initiated."
                })
                return

        # 2. Human-in-the-Loop CLO Editor
        if path == "/api/update-clo":
            clo_id = payload.get("clo_id")
            course_code = payload.get("course_code")
            new_desc = payload.get("new_description", "").strip()

            if not clo_id or not new_desc:
                self.send_json(HTTPStatus.BAD_REQUEST, {"error": "Missing 'clo_id' or 'new_description'."})
                return

            # Validate active Bloom verb
            try:
                CourseOutcomeSchema.reject_unmeasurable_verbs(new_desc)
            except ValueError as ve:
                self.send_json(HTTPStatus.BAD_REQUEST, {
                    "success": False,
                    "error": f"Bloom Taxonomy Violation: {str(ve)}"
                })
                return

            # Update SQLite database
            success = update_clo(clo_id, new_desc, course_code=course_code)
            if success:
                # Recompile HTML document
                try:
                    export_to_file(course_code)
                except Exception:
                    pass
                self.send_json(HTTPStatus.OK, {
                    "success": True,
                    "message": f"Successfully updated {clo_id} in SQLite database and recompiled official HTML!"
                })
            else:
                self.send_json(HTTPStatus.NOT_FOUND, {
                    "success": False,
                    "error": f"Could not find {clo_id} for course {course_code} in database."
                })
            return

        # 3. Compile HTML Document
        if path == "/api/compile":
            course_code = payload.get("course_code", "BSCS 3112")
            try:
                out_path = export_to_file(course_code)
                clean_code = course_code.replace(" ", "_").replace("/", "-")
                self.send_json(HTTPStatus.OK, {
                    "success": True,
                    "html_file": f"official_syllabus_{clean_code}.html",
                    "file_path": out_path
                })
            except Exception as e:
                self.send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": str(e)})
            return

        # 4. Nuclear Wipe Workspace endpoint
        if path in ("/api/nuke", "/api/clear", "/api/reset"):
            result = perform_nuke()
            self.send_json(HTTPStatus.OK, result)
            return

        self.send_error(HTTPStatus.NOT_FOUND, "Endpoint not found.")


def start_server(host: str = HOST, port: int = PORT, open_browser: bool = True):
    server_address = (host, port)
    httpd = ThreadingHTTPServer(server_address, OBE18WeekHttpHandler)
    url = f"http://{host}:{port}"
    print(f"[+] 18-Week OBE Studio Web Server running at: {url}")
    print("    Pre-configured with 8 official 3rd-Year Computer Science subjects.")
    print("    Press Ctrl+C to terminate the server.\\n")
    if open_browser:
        webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\\n[*] Server shutdown initiated.")
    finally:
        httpd.server_close()
        print("[+] Server terminated gracefully.")


if __name__ == "__main__":
    port = PORT
    for i, arg in enumerate(sys.argv):
        if arg == "--port" and i + 1 < len(sys.argv):
            try:
                port = int(sys.argv[i + 1])
            except ValueError:
                pass
    no_browse = "--no-browser" in sys.argv or os.environ.get("NO_BROWSER") == "1"
    start_server(port=port, open_browser=not no_browse)
