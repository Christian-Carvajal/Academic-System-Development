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
├── run_18thweek.bat               # Windows batch launcher (Port 8001)
├── run_18thweek.py                # Cross-platform Python launcher (Port 8001)
├── 18thWeekOutput/                # Complete self-contained microservice studio package
│   ├── app.py                     # ThreadingHTTPServer backend & REST API dispatch
│   ├── index.html                 # Modern 3-view SPA frontend
│   ├── curriculum_catalog.py      # 8 3rd-year BSCS curriculum subjects catalog
│   ├── obe_schemas.py             # Pydantic v2 runtime data contracts
│   ├── llm_engine.py              # Ollama client, CoT stripper, self-healing loop
│   ├── db_manager.py              # SQLite CRUD persistence layer
│   ├── export_engine.py           # Jinja2 HTML compiler
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
   - Inspect weekly topics, K/S/A domains, TLAs, and assessments in the 18-Week Schedule Matrix tab.
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
4. **`☢️ Nuclear Workspace Reset`**:
   - Click `☢️ NUKE WORKSPACE` in the top header or database tab to open the confirmation modal.
   - Confirms deletion of all generated HTML/JSON deliverables, wipes the SQLite database, and clears browser caches, restoring the system to a clean state.
