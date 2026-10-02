# AGENTS.md — UPHSD CCS OBE Academic System Pipeline

## 1. Project Overview & Multi-Agent Architecture
This project implements the automated College of Computer Studies (CCS) Outcome-Based Education (OBE) AI Microservice Pipeline for the University of Perpetual Help System DALTA (UPHSD, Molino Campus), authored under the guidelines of **Prof. Roberto L. Malitao**.

The system orchestrates local LLM inference via **Ollama (`qwen3.5:4b`)**, enforcing strict Pydantic v2 data contracts, pedagogical validation guardrails, normalized SQLite persistence, institutional Jinja2 document compilation, and a modern 3-view interactive web application shell on **Port 8001**.

* **Lead Architect:** Christian Ezekiel L. Carvajal (BSCS 3112)
* **Collaborative Partner:** John Miko P. Sarsalijo (BSCS 3112)
* **Course Evaluator:** Prof. Roberto L. Malitao
* **Primary Launcher:** `run_18thweek.bat` / `python run_18thweek.py` (Port 8001)

---

## 2. Agent Roster & Role Definitions

```text
+-----------------------------------------------------------------------------------+
|                            AGENTS ORCHESTRATION ROSTER                            |
+-----------------------------------------------------------------------------------+
|  1. CurriculumDesignAgent       -> System Prompts & Bloom's Taxonomy Invariants   |
|  2. SchemaValidatorAgent        -> Pydantic v2 Runtime Data Contracts & CoT Strip |
|  3. PipelineOrchestrationAgent  -> Ollama LLM Execution, Retries & Batch Engine   |
|  4. DatabasePersistenceAgent    -> SQLite Foreign Key Relations & Human-in-Loop   |
|  5. DocumentExportAgent         -> Jinja2 HTML Compilation & Vector PDF Print Engine |
|  6. QAAuditAgent                -> CHED CMO 25 Invariant Audit & Nuclear Protocol |
+-----------------------------------------------------------------------------------+
```

### Agent 1: `CurriculumDesignAgent`
* **Role:** Expert IT/CS Curriculum Designer & Prompt Engineer
* **Responsibilities:**
  - Formulates contextual system prompts enforcing active Bloom's Revised Taxonomy cognitive action verbs (`Identify`, `Configure`, `Implement`, `Analyze`, `Design`, `Evaluate`, `Develop`).
  - Banned verb mitigation: intercepts and eliminates unmeasurable passive phrasing (`understand`, `learn`, `know`, `study`, `familiarize`, `be exposed to`).
  - Incorporates target Program Learning Outcomes (PLOs / POs 1–5), credit units, lecture/lab ratios, and prerequisites from `curriculum_catalog.py`.
  - Supports zero-typing defaults and faculty customized parameter inputs (Image 5 specification).
* **Target Artifacts:** `curriculum_catalog.py`, `llm_engine.py` prompt templates.

### Agent 2: `SchemaValidatorAgent`
* **Role:** Type Enforcement & Runtime Contract Guardrail
* **Responsibilities:**
  - Validates raw LLM outputs against strict Pydantic v2 schemas (`CourseMetadataSchema`, `CourseOutcomeSchema`, `LessonOutcomeSchema`, `WeeklyScheduleSchema`, `FullSyllabusSchema`).
  - Strips Chain-of-Thought (`<think>...</think>`) reasoning and isolates JSON boundary substrings.
  - Enforces tripartite educational domains: strictly `domain: Literal["K", "S", "A"]` (Knowledge, Skills, Attitude).
  - Generates detailed, diagnostic feedback upon `ValidationError` or `JSONDecodeError` to drive the model re-prompt loop.
* **Target Artifacts:** `obe_schemas.py`.

### Agent 3: `PipelineOrchestrationAgent`
* **Role:** Chained Workflow, Background Execution & Queue Controller
* **Responsibilities:**
  - Coordinates asynchronous LLM generation in background daemon threads (`run_generation_worker`).
  - Manages sequential single-course and 8-subject batch queues with live state reporting (`/api/generation-state`).
  - Implements multi-turn automated self-healing retry loop (maximum 3 attempts) capturing `exc.errors()` and injecting corrective instructions back to Qwen.
  - Temperature regulation: `0.2` for deterministic, schema-compliant JSON generation.
* **Target Artifacts:** `app.py`, `llm_engine.py`.

### Agent 4: `DatabasePersistenceAgent`
* **Role:** Relational Data Engineer & CRUD Persistence Manager
* **Responsibilities:**
  - Enforces normalized SQLite schema across 4 tables: `courses`, `course_outcomes`, `weekly_schedules`, `lesson_outcomes`.
  - Enforces `PRAGMA foreign_keys = ON` and `ON DELETE CASCADE` on all relational child tables.
  - Implements atomic transactions for saving and retrieving full syllabi (`save_syllabus`, `get_syllabus`).
  - Powers Human-in-the-Loop faculty CLO editing (`update_clo`), validating active Bloom verbs before writing updates to disk.
* **Target Artifacts:** `database/schema.sql`, `db_manager.py`, `database/obe_syllabus.db`.

### Agent 5: `DocumentExportAgent`
* **Role:** Institutional Layout & Vector Print Design Engineer
* **Responsibilities:**
  - Compiles structured syllabus data into official UPHSD CCS institutional HTML syllabi via Jinja2 (`templates/uphsd_ccs_template.html`).
  - Embeds institutional branding: UPHSD Maroon (`#7f1416`) and Gold (`#f59e0b`), University seal, signatory blocks, and grading formula breakdown.
  - Integrates `@media print` CSS rules for high-resolution vector PDF export (`window.print()` / browser print engine).
  - Powers standalone tab opening and direct file downloading.
* **Target Artifacts:** `templates/uphsd_ccs_template.html`, `export_engine.py`, `outputs/official_syllabus_*.html`.

### Agent 6: `QAAuditAgent`
* **Role:** Academic Accreditation & Rubric Compliance Auditor
* **Responsibilities:**
  - Executes automated program invariant tests against CHED CMO 25 s.2015 and Prof. Roberto L. Malitao's Milestone 1 & 2 rubric.
  - Asserts the 7 strict institutional invariants:
    1. Strict 18-Week Total Schedule.
    2. Week 9 Midterm Exam Milestone Lock.
    3. Week 18 Final Exam / Capstone Defense Lock.
    4. Tripartite K/S/A domain coverage across all weeks.
    5. Active Bloom's Taxonomy cognitive action verbs (0 banned verbs).
    6. Program Learning Outcomes (PLO) mapping coverage.
    7. UPHSD Institutional Grading Breakdown (70% Class Standing: 30% Quizzes, 20% Research, 50% Lab + 30% Major Exam).
  - Coordinates Nuclear Workspace Reset (`/api/nuke`) to cleanly wipe deliverables, reset database, and clear caches.
* **Target Artifacts:** `app.py` (`/api/audit`, `/api/nuke`), `index.html` audit view.

---

## 3. Tool Permissions & Operational Boundaries

| Agent | Allowed Tools / Actions | Restricted Actions |
|---|---|---|
| `CurriculumDesignAgent` | Prompt authoring, catalog metadata inspection, parameter resolution | Cannot alter Pydantic models directly |
| `SchemaValidatorAgent` | Pydantic schema declaration, `@field_validator`, regex verb checks | Cannot bypass banned verb checks or allow undefined fields |
| `PipelineOrchestrationAgent` | Background thread dispatch, Ollama REST API calls, retry budget management | Cannot accept unvalidated JSON payloads |
| `DatabasePersistenceAgent` | SQLite DDL/DML, transaction control, cascading deletes | Cannot orphan child records without valid `course_id` |
| `DocumentExportAgent` | Jinja2 template rendering, HTML file generation, print CSS | Cannot hardcode static data into institutional templates |
| `QAAuditAgent` | Invariant assertions, compliance scoring, nuclear reset execution | Cannot modify syllabus content arbitrarily |

---

## 4. Multi-Turn Self-Healing Error Recovery Protocol

```text
                     [Client Request (Web / CLI)]
                                   │
                                   ▼
                 [Ollama POST /api/generate (format="json")]
                                   │
                                   ▼
                      [CoT / <think> Parser]
                   (Extract pure JSON substring)
                                   │
                                   ▼
                     [Pydantic v2 Schema Validation]
                                   │
                 ┌─────────────────┴─────────────────┐
                 │                                   │
             (Success)                           (Failure)
                 │                                   ▼
                 │                       [Capture ValidationError]
                 │                       (Extract loc, msg, type)
                 │                                   ▼
                 │                       [Construct Feedback Prompt]
                 │                       (Enforce active verbs / KSA)
                 │                                   ▼
                 │                       [Re-query Ollama (Max 3x)]
                 │                                   │
                 │                       ┌───────────┴───────────┐
                 │                       ▼                       ▼
                 │                   (Success)           (Exhausted Retries)
                 │                       │                       ▼
                 ▼                       │               [Raise Error & Halt]
      [SQLite Relational Save] ◄─────────┘
                 │
                 ▼
      [Jinja2 Document Export]
                 │
                 ▼
      [Ready for Live Inspection / Print PDF]
```

---

## 5. Development & Execution Conventions
* **Environment:** Python 3.10+ (tested on Python 3.14) in isolated virtual environment (`.venv`).
* **Microservice Host:** `http://127.0.0.1:8001` (ThreadingHTTPServer, zero external server dependencies).
* **Local AI Model:** `qwen3.5:4b` hosted on local Ollama daemon (`http://127.0.0.1:11434`).
* **Frontend Architecture:** Modern 3-View Single-Page Application (`Curriculum Studio`, `Dedicated Syllabus Viewer & Print Studio`, `Relational Database & Audit`).
* **Launch Commands:**
  - Batch launcher: `run_18thweek.bat`
  - Python launcher: `python run_18thweek.py`
  - Direct server: `python 18thWeekOutput/app.py`

---

## 6. Mandatory Documentation Protocol: Continuous README & Docs Maintenance

> [!IMPORTANT]
> **AUTONOMOUS DOCUMENTATION DIRECTIVE FOR ALL AGENTS (Antigravity, Collaborator Agents, Claude, GPT):**
> 1. **Zero-Prompt Proactive Maintenance:** Whenever you make code modifications (frontend UI, backend API endpoints, database schemas, scripts, validation rules, or launchers), you **MUST proactively update `README.md` and the appropriate files in `docs/` in the same turn without being asked.**
> 2. **Never Leave Documentation Out of Sync:** Any new feature, button, endpoint, bug fix, or architecture change must be immediately documented in:
>    - `README.md`: System capabilities, directory structure, testing guides, and quick-start instructions.
>    - `docs/HANDOFF.md`: Status of deliverables, handoff notes, and runbook instructions.
>    - `docs/PROJECT_TRACKING.md`: Live changelog, operational runbooks, and implementation status.
>    - `docs/PROJECT_ROADMAP.md`: Phase status and completed tasks.
> 3. **Preserve Raw Professor Instructions:** The file `docs/projectInstructionByProfessor.md` contains the verbatim raw prompt and guidelines from Prof. Roberto L. Malitao. **NEVER modify or truncate `docs/projectInstructionByProfessor.md`**.
> 4. **Respect Collaborator Creative Domain:** John Miko P. Sarsalijo retains full creative ownership over UI/UX design, visual themes, and layout prompting. Document this explicitly in `docs/HANDOFF.md`.
> 5. **Atomic Commit Cleanliness:** Always ensure all docs updates are committed alongside code updates so git history remains cleanly paired and traceable.

---

## 7. Operational Upgrades & Microservice Extensions

### 7.1 Single-Subject Selective Wipe (`POST /api/subject/wipe`)
* **Database Function:** `delete_course(course_code: str) -> bool` in `18thWeekOutput/db_manager.py`.
* **API Route:** `POST /api/subject/wipe` with JSON body `{"course_code": "BSCS 3112"}` in `18thWeekOutput/app.py`.
* **Behavior:** Cascades deletions across SQLite tables (`lesson_outcomes`, `weekly_schedules`, `course_outcomes`, `courses`), deletes compiled deliverables (`outputs/official_syllabus_{code}.html` and `outputs/sample_validated_output_{code}.json`), and resets course state to pending without affecting other subjects.
* **UI Trigger:** `🗑️ Wipe Course` button in the Curriculum Studio header row, plus Command Palette (`Ctrl + K`).

### 7.2 Universal Command Palette (`Ctrl + K`) & Multi-Criteria Search
* **Shortcut:** `Ctrl + K` (or `Cmd + K` on macOS) opens the interactive Command Palette modal.
* **Multi-Criteria Search:** Searches across `course_code`, `course_title`, `category`, and `course_description`.
* **Navigation:** Allows instantaneous course selection, quick tab switching (`1: Studio`, `2: Viewer`, `3: Database`), one-click batch generation, single-course wipe, and nuclear reset.

### 7.3 PLO Alignment Matrix Pedagogy (CHED CMO 25 s.2015)
* In Outcome-Based Education, courses are specialized. Not all dots in the PLO matrix are green because each course deliberately targets only specific Program Learning Outcomes (e.g., Automata targets PLO 1 & 5; Software Engineering targets PLO 2, 3, 4).
* Claiming all green dots across all PLOs is classified as "outcome inflation" and is an accreditation violation. The matrix accurately reflects curricular scaffolding.

### 7.4 Streamlined 1-Click Launchers (Single UI & Single CLI)
* **Interactive Studio (With UI):** `run_18thweek.bat` (Port 8001). Pre-flights environment, self-heals any zombie processes holding port 8001, and launches the browser after socket binding.
* **Headless Pipeline (Without UI / CLI Only):** `run_18th_week.bat`. Sequentially runs Milestone 1 (`llm_engine.py`), Milestone 2 (`db_manager.py`), and Jinja2 compilation (`export_engine.py "BSCS 3112"`).
* **De-cluttering & Alias Removal:** Removed all redundant/confusing alias files (`run_18th_week_gui.bat`, `run_gui.bat`, `run_pipeline.bat`, `18thWeekOutput/run_gui.bat`, and `18thWeekOutput/run_gui.py`).
