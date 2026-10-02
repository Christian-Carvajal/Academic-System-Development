# SYSTEM_ARCHITECTURE.md — OBE Microservice Architecture

## 1. Architectural Blueprint

The UPHSD CCS OBE Academic System Pipeline is a layered microservice architecture designed to transform curriculum parameters into strictly validated, accreditation-ready Outcome-Based Education (OBE) course syllabi conforming to **CHED CMO 25 s.2015**.

```text
+-----------------------------------------------------------------------------------------+
|                                    CLIENT VIEWPORT                                      |
|             Modern 3-View Single-Page Application (SPA) on Port 8001                    |
|   [🎓 Curriculum Studio]  [📄 Dedicated Syllabus Viewer]  [🛡️ Database & Audit]         |
+-----------------------------------------------------------------------------------------+
                                             │
                                             ▼
+-----------------------------------------------------------------------------------------+
|                              REST API & ROUTING ENGINE                                  |
|                 ThreadingHTTPServer (18thWeekOutput/app.py on Port 8001)                 |
|   /api/subjects, /api/syllabus, /api/database, /api/audit, /api/generate, /api/nuke     |
+-----------------------------------------------------------------------------------------+
                                             │
                                             ▼
+-----------------------------------------------------------------------------------------+
|                               LOCAL AI INFERENCE LAYER                                  |
|                       Ollama Daemon (http://localhost:11434)                            |
|             - Model: qwen3.5:4b                                                         |
|             - Parameter: format="json" (grammar token constraint)                       |
|             - Sampling: temperature=0.2 (deterministic output)                          |
+-----------------------------------------------------------------------------------------+
                                             │
                                             ▼
+-----------------------------------------------------------------------------------------+
|                              PARSING & GUARDRAIL LAYER                                  |
|         - CoT (<think>...</think>) Reasoning Extraction                                 |
|         - JSON Substring Boundary Locating                                              |
|         - Pydantic v2 Type & Field Validation (obe_schemas.py)                          |
+-----------------------------------------------------------------------------------------+
          │                                              │
      [Success]                                      [Failure]
          │                                              ▼
          │                               +-------------------------------+
          │                               |   Automated Re-prompt Loop    |
          │                               |  - Inject ValidationError     |
          │                               |  - Re-query (Max 3 attempts)  |
          │                               +-------------------------------+
          ▼
+-----------------------------------------------------------------------------------------+
|                           RELATIONAL PERSISTENCE (SQLite 3)                             |
|                           database/obe_syllabus.db                                      |
|      - Normalized Tables: courses, course_outcomes, weekly_schedules, lesson_outcomes   |
|      - Relational Constraints: PRAGMA foreign_keys = ON & ON DELETE CASCADE             |
|      - Human-in-the-Loop CRUD: update_clo with Bloom's Taxonomy validation              |
+-----------------------------------------------------------------------------------------+
          │
          ▼
+-----------------------------------------------------------------------------------------+
|                        INSTITUTIONAL DOCUMENT ASSEMBLY & PRINT                          |
|                 templates/uphsd_ccs_template.html & export_engine.py                    |
|      - Jinja2 Compilation into outputs/official_syllabus_*.html                         |
|      - Institutional Branding: UPHSD Maroon (#7f1416) & Academic Gold (#f59e0b)         |
|      - Vector PDF Print Engine: @media print CSS invoked via window.print()             |
+-----------------------------------------------------------------------------------------+
```

---

## 2. 3-View Single-Page Application (SPA) Layout

```text
+-----------------------------------------------------------------------------------------+
| APP HEADER: Brand Seal | UPHSD CCS 18-Week OBE Studio | View Navigation | Status Badges |
+-----------------------------------------------------------------------------------------+
|                                                                                         |
|  VIEW 1: [🎓 Curriculum Studio]                                                         |
|  ├── 1. Curriculum Subjects Grid (8 BSCS Courses) [All | ✓ Generated | ⏳ Ready]        |
|  ├── 2. Auto-Filled & Editable Parameter Form (Course Title, Code, Description, PLOs)  |
|  ├── 3. Asynchronous Generation HUD (Live Progress Bar & Log Window)                  |
|  └── 4. Studio Inspection Tabs (🎯 Course Outcomes with Editor | 🗓️ 18-Week Matrix)   |
|                                                                                         |
|  VIEW 2: [📄 Dedicated Syllabus Viewer & Print Studio]                                  |
|  ├── Left Sidebar (Master Drawer): Instant Search Box, Filter Pills, Subject List       |
|  └── Right Stage: Sticky Action Toolbar (🖨️ Print / Save Vector PDF, ↗ Tab, ⬇ HTML)    |
|       └── Full-Height Official Syllabus Document Canvas (Jinja2 HTML Preview)           |
|                                                                                         |
|  VIEW 3: [🛡️ Relational Database & Accreditation Audit]                                  |
|  ├── 1. SQLite Relational Table Inspector (with "📄 View Official Syllabus" CTA)        |
|  ├── 2. CHED CMO 25 Invariant Compliance Engine (7 Live Automated Tests)               |
|  └── 3. UPHSD CCS Institutional Grading Framework (70% Class Standing / 30% Major Exam) |
|                                                                                         |
+-----------------------------------------------------------------------------------------+
| NUKE MODAL: Permanent Workspace Reset Dialog (Clears Deliverables, DB, Caches)          |
+-----------------------------------------------------------------------------------------+
```

---

## 3. REST API Endpoint Specification

The microservice backend in `18thWeekOutput/app.py` exposes the following endpoints on `http://127.0.0.1:8001`:

| Method | Endpoint | Description | Payload / Query Parameters | Response |
|---|---|---|---|---|
| `GET` | `/` | Serves the 3-view SPA frontend | None | `200 OK` (`text/html`) |
| `GET` | `/api/status` | Health check for Ollama daemon & model | None | `200 OK`: `{"ollama": {"running": true}, "model": "qwen3.5:4b"}` |
| `GET` | `/api/subjects` | Lists all 8 curriculum subjects with persistence flags | None | `200 OK`: `{"subjects": [...]}` |
| `GET` | `/api/syllabus` | Retrieves syllabus from SQLite or output JSON | `?code=BSCS+3111` | `200 OK`: `{"source": "sqlite", "data": {...}}` |
| `GET` | `/api/database` | Lists all persisted courses in SQLite | None | `200 OK`: `{"courses": [...]}` |
| `GET` | `/api/audit` | Evaluates syllabus against 7 CHED CMO 25 invariants | `?code=BSCS+3111` | `200 OK`: `{"compliance_score": "100%", "all_passed": true, "checks": [...]}` |
| `GET` | `/api/generation-state`| Polls active background generation progress & logs | None | `200 OK`: `{"status": "running", "progress_pct": 50, "logs": [...]}` |
| `POST` | `/api/generate` | Starts background worker thread for single or batch | `{"course_code": "BSCS 3111", ...}` or `{"batch": true}` | `200 OK`: `{"status": "started"}` |
| `POST` | `/api/update-clo` | Human-in-the-Loop CLO statement update | `{"clo_id": "CLO 1", "course_code": "...", "new_description": "..."}` | `200 OK`: `{"success": true, "message": "..."}` |
| `POST` | `/api/subject/wipe`| Selectively deletes single course from DB and removes its files | `{"course_code": "BSCS 3112"}` | `200 OK`: `{"success": true, "message": "Wiped..."}` |
| `POST` | `/api/nuke` | Permanently deletes outputs, drops tables, clears state | None | `200 OK`: `{"success": true, "message": "Nuked"}` |
| `GET` | `/outputs/*` | Serves static HTML and JSON deliverables | `official_syllabus_BSCS_3111.html` | `200 OK` (Static File) |

---

## 4. Pydantic v2 Data Contract Topology (`obe_schemas.py`)

### 1. `CourseMetadataSchema`
* `course_code: str` — e.g., `"BSCS 3112"`
* `course_title: str` — e.g., `"Artificial Intelligence"`
* `credit_units: int` — e.g., `3`
* `lecture_hours: int` — e.g., `2`
* `lab_hours: int` — e.g., `3`
* `prerequisites: str` — e.g., `"BSCS 3108"`
* `course_description: str` — Official catalog summary

### 2. `CourseOutcomeSchema`
* `clo_id: str` — e.g., `"CLO 1"`, `"CLO 2"`
* `bloom_level: Literal["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]`
* `description: str` — Guarded by `@field_validator("description")` enforcing active cognitive action verbs and rejecting banned verbs (`understand`, `know`, `learn`, `study`, `familiarize`, `be exposed to`)
* `program_outcomes_mapped: List[str]` — e.g., `["PLO 1", "PLO 2"]`

### 3. `LessonOutcomeSchema`
* `llo_id: str` — e.g., `"LLO 1.1"`
* `domain: Literal["K", "S", "A"]` — Strictly constrained to Knowledge (Cognitive), Skills (Psychomotor), or Attitude (Affective)
* `description: str` — Granular instructional outcome

### 4. `WeeklyScheduleSchema`
* `week_number: int` — Range: `1` to `18`
* `period: str` — `"MIDTERM"`, `"MIDTERM EXAM"`, `"FINAL"`, `"FINAL EXAM"`
* `topics: Union[List[str], str]` — Topic statements
* `lesson_outcomes: List[LessonOutcomeSchema]` — Tripartite domain scaffolding
* `teaching_learning_activities: List[str]` — Active learning modalities (Lectures, Machine Problems)
* `assessment_tasks: List[str]` — Formative and summative assessment tools
* `resources: Optional[List[str]]` — Reference texts, lab tools, frameworks

### 5. `FullSyllabusSchema`
* Aggregates `course_metadata`, `course_outcomes` (3 to 5), and `weekly_schedule` (strictly 18 weeks)
* Cross-schedule validator asserts complete term-wide K/S/A domain presence

---

## 5. SQLite Normalized Relational Schema (`database/schema.sql`)

```sql
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_code TEXT NOT NULL UNIQUE,
    course_title TEXT NOT NULL,
    credit_units INTEGER NOT NULL DEFAULT 3,
    lecture_hours INTEGER NOT NULL DEFAULT 2,
    lab_hours INTEGER NOT NULL DEFAULT 3,
    prerequisites TEXT DEFAULT 'None',
    course_description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS course_outcomes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    clo_id TEXT NOT NULL,
    bloom_level TEXT NOT NULL,
    description TEXT NOT NULL,
    program_outcomes_mapped TEXT,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS weekly_schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    week_number INTEGER NOT NULL,
    period TEXT NOT NULL,
    topics TEXT NOT NULL,
    teaching_learning_activities TEXT,
    assessment_tasks TEXT,
    resources TEXT,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS lesson_outcomes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    schedule_id INTEGER NOT NULL,
    llo_id TEXT NOT NULL,
    domain TEXT NOT NULL CHECK(domain IN ('K', 'S', 'A')),
    description TEXT NOT NULL,
    FOREIGN KEY (schedule_id) REFERENCES weekly_schedules(id) ON DELETE CASCADE
);
```

---

## 6. Institutional Document Assembly & Vector Print Engine

The document compilation pipeline bridges structured relational data to publication-grade institutional artifacts:
1. **Jinja2 Compilation:** `export_engine.py` injects reconstructed `FullSyllabusSchema` instances into `templates/uphsd_ccs_template.html`.
2. **Institutional Layout:** Renders official UPHSD seal, course specification table, CLO cognitive mapping matrix, 18-week schedule with K/S/A color badges, 70/30 grading formula, and faculty/dean signature blocks.
3. **Vector PDF Printing:** Built-in `@media print` CSS engine strips unnecessary web chrome, locks paper margins (`margin: 15mm 12mm`), preserves table borders, prevents mid-row page splits (`page-break-inside: avoid`), and produces high-resolution vector PDF outputs via `window.print()`.

---

## 7. Resilience & Nuclear Reset Protocols

1. **Reasoning Extraction:** The CoT stripper regex isolates JSON substrings from raw LLM outputs, removing `<think>...</think>` tokens.
2. **Multi-Turn Self-Healing Loop:** If Qwen outputs invalid JSON or triggers a Pydantic `ValidationError`, the error traceback is extracted and sent back as a diagnostic user prompt. The loop runs up to 3 attempts with temperature `0.2`.
3. **Nuclear Workspace Reset:** When triggered, `/api/nuke`:
   - Deletes all `outputs/official_syllabus_*.html` and `sample_validated_output_*.json` files.
   - Drops all 4 SQLite tables and re-executes `schema.sql`.
   - Clears in-memory generation queues, active courses, and background states.
   - Instructs the frontend to clear `localStorage` and `sessionStorage`, restoring the workspace to a pristine state.
