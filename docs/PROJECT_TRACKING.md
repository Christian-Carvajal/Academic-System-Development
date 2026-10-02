# PROJECT_TRACKING.md — AI-Powered OBE Syllabus Generator Microservice

## 1. Project Information & Group Leadership
* **Lead Architect & Systems Engineer:** Christian Ezekiel L. Carvajal (BSCS 3112)
* **Collaborative Partner & Systems Engineer:** John Miko P. Sarsalijo (BSCS 3112)
* **Academic Institution:** College of Computer Studies (CCS), University of Perpetual Help System DALTA (Molino Campus)
* **Subject:** BSCS 3112 / Artificial Intelligence (Lesson 5 — Midterm Mini-Project)
* **Course Evaluator:** Prof. Roberto L. Malitao
* **Active Working Port:** `http://127.0.0.1:8001` (ThreadingHTTPServer)
* **Primary Launchers:** `run_18thweek.bat` | `python run_18thweek.py`

---

## 2. Tech Stack & Component Specifications
* **Core Language:** Python 3.10+ (tested on Python 3.14 / isolated `.venv`)
* **Local LLM Engine:** Ollama with `qwen3.5:4b` exclusively (`http://localhost:11434/api/generate`)
* **Data Contract Validation:** Pydantic v2 (`pydantic>=2.0`)
* **Relational Persistence:** SQLite 3 (`database/obe_syllabus.db`) with `PRAGMA foreign_keys = ON` and `ON DELETE CASCADE`
* **Document Compilation:** Jinja2 (`jinja2>=3.1`) generating browser-ready HTML syllabi
* **Vector Print Engine:** Native browser print engine (`@media print` CSS with zero dependencies)
* **Frontend Architecture:** Single-Page Application (SPA) with 3-View Tabbed App Shell

---

## 3. Directory & File Inventory

```text
submission_deliverables/
├── run_18thweek.bat               # Windows batch launcher (With UI - Port 8001)
├── run_18th_week.bat              # Windows batch runner   (Without UI - CLI Only)
├── run_18thweek.py                # Cross-platform Python launcher (Port 8001)
├── OBE_Syllabus_Generator_18th_Week_Documentation.pdf # Complete 16-page technical documentation PDF
├── 18thWeekOutput/                # Complete self-contained microservice studio package
│   ├── app.py                     # ThreadingHTTPServer backend & REST API dispatch
│   ├── index.html                 # Modern 3-view SPA frontend
│   ├── curriculum_catalog.py      # 8 3rd-year BSCS curriculum subjects catalog
│   ├── obe_schemas.py             # Pydantic v2 runtime data contracts
│   ├── llm_engine.py              # Ollama client, CoT stripper, self-healing loop
│   ├── db_manager.py              # SQLite CRUD persistence layer
│   ├── export_engine.py           # Jinja2 HTML compiler
│   ├── generate_docs_html.py      # Documentation compiler script
│   ├── compiled_documentation.html# Source HTML document with vector print styles
│   ├── documentation_assets/      # 10 full-res 1920x1080 UI screenshots
│   ├── run_18thweek.bat           # 18-Week Studio Launcher (With UI)
│   ├── run_18th_week.bat          # 18-Week Headless CLI Pipeline (Without UI)
│   ├── database/
│   │   ├── schema.sql             # Normalized DDL (courses, clos, weeks, llos)
│   │   └── obe_syllabus.db        # SQLite relational database
│   ├── templates/
│   │   └── uphsd_ccs_template.html# Official institutional Jinja2 layout
│   └── outputs/                   # Generated HTML & JSON deliverables
│       ├── official_syllabus_*.html
│       └── sample_validated_output_*.json
└── docs/                          # Comprehensive system documentation
    ├── AGENTS.md                  # Multi-agent orchestration specification
    ├── HANDOFF.md                 # Collaborator AI engineering handoff & runbook
    ├── OBE_RUBRIC_SPECIFICATION.md# CHED CMO 25 & UPHSD grading rules
    ├── PROJECT_ROADMAP.md         # Milestone execution tracking
    ├── PROJECT_TRACKING.md        # This operational tracking document
    ├── SYSTEM_ARCHITECTURE.md     # Detailed technical architecture blueprint
    └── projectInstructionByProfessor.md # Exact verbatim raw professor instructions
```

---

## 4. Live Verification Logs & Audit Evidence

### 1. Pydantic Bloom Verb Rejection Test
```text
PASS: Rejected banned verb: 1 validation error for CourseOutcomeSchema
description
  Value error, Banned non-measurable verb 'understand' detected in outcome statement.
PASS: Allowed valid active verb: Analyze algorithmic time complexity
PASS: Allowed valid domain: K
PASS: Rejected invalid domain: 'X'
```

### 2. Live LLM Engine Execution (`qwen3.5:4b`)
```text
[*] Starting AI-Powered OBE Syllabus Generation Pipeline...
[*] Target LLM Model: qwen3.5:4b on http://localhost:11434
[+] Metadata parsed: BSCS 3111 - Data Mining
[*] [Stage 1: CLOs] Querying qwen3.5:4b (Attempt 1/3)...
[+] [Stage 1: CLOs] Successfully validated 4 Course Outcomes.
[*] [Stage 2: Schedule] Querying qwen3.5:4b for 18-week matrix (Attempt 1/3)...
[+] [Stage 2: Schedule] Successfully validated 18-week schedule.
[+] Root FullSyllabusSchema validation passed successfully!
[+] Validated syllabus persisted to 'outputs/sample_validated_output_BSCS_3111.json'.
```

### 3. Relational Database Persistence & Cascading Deletes Test
```text
[+] Database initialized successfully at 'database/obe_syllabus.db'.
[+] Foreign keys verified: PRAGMA foreign_keys = 1.
[+] Persisted syllabus for 'BSCS 3111' (Course ID: 20) into SQLite.
[+] Verification: Read back 'Data Mining' with 18 weeks and 4 CLOs.
[+] Human-in-the-Loop Test: Updated CLO 1 in SQLite successfully.
```

### 4. Jinja2 Document Export & Vector Print Test
```text
[*] Testing export engine for course 'BSCS 3111'...
[+] Successfully exported official syllabus to 'outputs/official_syllabus_BSCS_3111.html'.
[+] Verification: File size is 32,409 bytes.
[+] Browser print engine invocation verified via frame.contentWindow.print().
```

### 5. Automated DOM & Server Contract Test Suite
```text
--- STARTING AUTOMATED BROWSER/DOM LOGIC SIMULATION ---
PASS: All 34 core UI DOM anchors verified in index.html!
PASS: All 10 modern UI stylesheet classes verified!
PASS: /api/subjects returned status 200 with 8 subjects.
PASS: /api/database returned status 200 with 2 courses persisted.
PASS: /outputs/official_syllabus_BSCS_3111.html returned status 200 (32,409 bytes).
PASS: /outputs/official_syllabus_BSCS_3108.html returned status 200 (31,249 bytes).
--- ALL SIMULATION AND CONTRACT TESTS COMPLETED WITH 100% SUCCESS ---
```

---

## 5. Step-by-Step Operational Runbook

### Starting the Application:
1. Ensure Ollama is running:
   ```cmd
   ollama serve
   ```
2. Launch the 18-week microservice:
   ```cmd
   run_18thweek.bat
   ```
   Or using Python:
   ```cmd
   python run_18thweek.py
   ```
3. Open `http://127.0.0.1:8001/` in any modern web browser.

### Using the 3 Primary Application Views:
1. **`🎓 Curriculum Studio` (`#view-studio`)**:
   - Click any subject card in the curriculum grid to auto-fill its OBE specification form.
   - Adjust any parameters in the textboxes (Course Title, Code, Description, Target PLOs) if desired.
   - Click **`⚡ Generate 18-Week OBE Syllabus (Qwen 3.5 4B)`** to start generation.
   - Watch real-time streaming progress in the Progress HUD.
   - Inspect Course Outcomes in the CLO tab and edit statements using the Human-in-the-Loop modal.
   - **`🗑️ Wipe Course (Selective Reset)`**: Click to reset only the currently selected course back to pending, cleanly cascading SQLite deletions and deleting that subject's deliverables without touching any other courses.
   - Inspect weekly topics, K/S/A domains, TLAs, and assessments in the 18-Week Schedule Matrix tab.
   - Review Tab 2: PLO Alignment Matrix with pedagogical guidance on why courses specialize in specific PLOs.
2. **`📄 Dedicated Syllabus Viewer & Print Studio` (`#view-viewer`)**:
   - Filter courses by `All (8)`, `✓ Generated`, or `⏳ Ready`.
   - Search courses using the real-time search box.
   - Click any generated subject (e.g., `BSCS 3108` or `BSCS 3111`) to immediately load its official institutional syllabus into the full-height document canvas.
   - Click **`🖨️ Print / Save Vector PDF`** to export a publication-ready vector PDF.
   - Click **`↗ Open Standalone Tab`** or **`⬇ Download HTML`** for local access.
3. **`🛡️ Relational Database & Accreditation Audit` (`#view-audit`)**:
   - View persisted courses in SQLite (`database/obe_syllabus.db`).
   - Click **`📄 View Official Syllabus`** on any course row — the UI instantly transitions to the Dedicated Syllabus Viewer with that document displayed.
   - Review live CHED CMO 25 invariant compliance scores (100% passing across all 7 checks).
4. **Universal Command Palette (`Ctrl + K`)**:
   - Press `Ctrl + K` (or `Cmd + K` on macOS) anywhere in the application.
   - Instantly search courses by code, title, category, or description with live keyboard filtering.
   - Run system actions: jump to views, trigger batch generation, wipe active course, or open documentation.
5. **`☢️ Nuclear Workspace Reset`**:
   - Click `☢️ NUKE WORKSPACE` in the top header or database tab to open the confirmation modal.
   - Confirms deletion of all generated HTML/JSON deliverables, wipes the SQLite database, and clears browser caches, restoring the system to a clean state.

---

## 6. Engineering Changelog & Recent Milestones

### October 2026 — Sprint 4: Operational Hardening & Usability
* **Feature (Individual Subject Wipe):** Added `delete_course(course_code)` to `18thWeekOutput/db_manager.py` with foreign key cascades; added `POST /api/subject/wipe` to `18thWeekOutput/app.py`; added `🗑️ Wipe Course` UI button in `index.html` with confirmation dialog, progress spinner, and state refresh.
* **Bug Fix (Universal Command Palette & Search):** Fixed `filterPalette()` in `index.html` where `subjectCatalog` was undefined; bound search to `subjects` catalog matching `course_code`, `course_title`, `category`, and `course_description`.
* **Pedagogical Alignment (PLO Matrix):** Added educational legend strip to Tab 2 explaining CHED CMO 25 s.2015 outcome distribution. Verified that specialized courses correctly map to subset PLOs to avoid outcome inflation.
* **Launcher & Port Fixes:** Resolved port 8001 socket conflicts by clearing orphaned processes; unified `run_18thweek.bat`, `run_gui.bat`, and `run_pipeline.bat`; updated `export_engine.py` default course parameter to `BSCS 3112`.
* **Launcher Diagnostics & Browser Race Fix:** Resolved empty log display by enforcing unbuffered output (`-u` flag in batch runners, `sys.stdout.reconfigure(line_buffering=True)`, `flush=True` on all console prints); replaced synchronous `webbrowser.open()` with `threading.Timer(1.0, ...)` eliminating `ERR_EMPTY_RESPONSE` browser race conditions before `serve_forever()` begins accepting socket connections.
* **Workspace De-cluttering (Launcher Consolidation):** Permanently deleted redundant/confusing alias scripts (`run_18th_week_gui.bat`, `run_gui.bat`, `run_pipeline.bat`, `18thWeekOutput/run_gui.bat`, and `18thWeekOutput/run_gui.py`). Streamlined to exactly two 18th-week scripts: `run_18thweek.bat` (With UI) and `run_18th_week.bat` (Without UI / CLI Only).
* **Agent Architecture Policy:** Enacted Section 6 in `docs/AGENTS.md` requiring all collaborating agents to continuously maintain `README.md` and documentation on every code change without waiting for user prompts.
* **Feature (Intelligent Batch Generation Dispatcher & Selective Synthesis):** Implemented an intelligent modal dialog dispatcher (`#batchModalOverlay`) when clicking "Batch Generate All Courses (Queue)" or triggering via Universal Command Palette (`Ctrl + K`). Dynamically inspects curriculum catalog state:
  - When $1 \le N < 8$ courses are already generated, displays an institutional modal with completed/pending pill badges, a visual catalog chip grid, and provides two distinct execution paths:
    1. **`⚡ Generate Remaining Only` (Recommended):** Skips the $N$ completed courses, preserving their SQLite records and deliverables while synthesizing only the pending courses to conserve time and local compute.
    2. **`🔄 Regenerate All 8 Courses`:** Freshly re-synthesizes all 8 courses from scratch via Qwen 2.5 4B, overwriting existing records and deliverables.
  - When $N = 0$, confirms full 8-course batch initialization.
  - When $N = 8$, informs user that 100% of courses are already complete and confirms fresh re-synthesis.
  - Backend support added in `18thWeekOutput/app.py`: `is_subject_generated(course_code)` and `run_batch_generation_worker(skip_existing=bool)` with granular progress calculation and live skip telemetry.
* **Milestone Execution (100% Curriculum Catalog Generated & Persisted):** Successfully executed batch generation across all 8 3rd-year CS curriculum subjects (`BSCS 3108`, `BSCS 3109`, `BSCS 3110`, `BSCS 3111`, `BSCS 3112`, `BSCS 3213`, `BSCS 3214`, `BSCS 3215`). All 8 subjects are now fully persisted in `database/obe_syllabus.db` (each with 4 Bloom-compliant CLOs, 18 weekly schedule items, and 54 tripartite K/S/A lesson outcomes), with complete official Jinja2 HTML and Pydantic v2 JSON deliverables available in `outputs/`.
* **Milestone Execution (BrowserOS neo 1080p Snapshots & Vector PDF Documentation):**
  - Integrated BrowserOS neo MCP to capture 10 high-resolution, uncropped 1920x1080 widescreen desktop snapshots across every view, modal, drawer, and inspector in the 18-week Interactive Studio (`http://127.0.0.1:8001`).
  - Configured Runbook Video HUD (`#demoHud`) in `18thWeekOutput/index.html` to load minimized by default, keeping full interface cards and tables unobstructed.
  - Implemented automated documentation compiler (`18thWeekOutput/generate_docs_html.py`) producing `compiled_documentation.html` with print-ready CSS (`@page A4`), tabular pipeline architecture, figure captions without AI filler/fluff, and syntax-highlighted code blocks for SQLite schema (`schema.sql`), Pydantic v2 data contracts (`obe_schemas.py`), LLM engine (`llm_engine.py`), SQLite CRUD layer (`db_manager.py`), and batch dispatcher (`app.py`).
* **Feature & Accessibility (Nuclear Course Wipe with Zero-Reload Real-Time Synchronization):**
  - Enhanced `delete_course(course_code)` in `18thWeekOutput/db_manager.py` with case-insensitive and whitespace-trimmed SQL queries, recursive foreign key cascading deletions across child tables (`lesson_outcomes`, `weekly_schedules`, `course_outcomes`) and parent `courses`, and SQLite database storage compaction (`VACUUM`).
  - Upgraded `perform_subject_wipe(course_code)` in `18thWeekOutput/app.py` to scour `outputs/` and base working directories for HTML deliverables and JSON state caches matching the subject code, resetting any in-memory generation state.
  - Implemented anti-cache HTTP response headers (`Cache-Control: no-cache, no-store, must-revalidate, max-age=0`, `Pragma: no-cache`, `Expires: 0`) on `send_json()`, preventing browser heuristic caching.
  - Rebuilt modal dialog (`#wipeSubjectModalOverlay`) adhering strictly to WCAG 2.2 Level AA accessibility standards with `role="dialog"`, `aria-modal="true"`, focus trapping, `Escape` key dismissal, and polite toast announcements (`aria-live="polite"`).
  - Engineered zero-reload optimistic UI synchronization in `18thWeekOutput/index.html` (`executeWipeSubject`): instantly updates the in-memory `subjects` catalog, resets the Hero Spotlight status badge to "Ready to Generate", clears studio tabs via `renderEmptySyllabus()`, resets the dedicated viewer iframe to standby, and re-queries `/api/subjects` and `/api/database` with `cache: "no-store"` and timestamp-based cache busters.

