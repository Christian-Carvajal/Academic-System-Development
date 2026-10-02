# HANDOFF.md — Collaborator AI & Team Engineering Hand-off

> **Project:** UPHSD CCS 18-Week Automated OBE Syllabus Studio & Repository (Lesson 5)  
> **Course:** BSCS 3112 — Artificial Intelligence (Laboratory)  
> **Course Evaluator:** Prof. Roberto L. Malitao  
> **Lead Architect:** Christian Ezekiel L. Carvajal  
> **Collaborative Partner:** John Miko P. Sarsalijo  
> **Target Deadline:** Saturday, October 3, 2026 (11:59 PM)  
> **Master Requirements:** [`docs/projectInstructionByProfessor.md`](file:///C:/Users/chris/Downloads/2.%20Projects/3.%20Reviewer/4artificialIntelligence/Midterm/lesson3and4/submission_deliverables/docs/projectInstructionByProfessor.md)  

---

## 1. Executive Summary & Purpose of this Hand-off

This document is specifically prepared for **John Miko P. Sarsalijo** and his **collaborating AI assistant (Antigravity / Claude / GPT / etc.)**.

It outlines:
1. **What has already been fully built, verified, and locked in** (Milestone 1 & Milestone 2 backend/database/export engine).
2. **The Collaborator's primary creative domain**: John Miko will **design and prompt the UI himself**, giving him full creative freedom over styling, layout, theme, and component structure.
3. **The remaining tasks for Milestone 2**: specifically the **3–5 minute video demonstration recording** and final individual submission packaging.
4. **Strict rubric verification criteria**: purely based on Prof. Roberto L. Malitao's 100-point assessment rubric.

---

## 2. Status of Milestone Deliverables

```text
+-----------------------------------------------------------------------------------------+
|                               DELIVERABLES STATUS SUMMARY                               |
+-----------------------------------------------------------------------------------------+
| MILESTONE 1 (Due Sept 26, 2026)                                                         |
|  [x] 1. obe_schemas.py (Pydantic v2 data contracts, Bloom validator, K/S/A)   -> DONE    |
|  [x] 2. llm_engine.py (Ollama client, format="json", 3-attempt retry loop)   -> DONE    |
|  [x] 3. sample_validated_output.json (AI-generated 18-week syllabus JSON)     -> DONE    |
|                                                                                         |
| MILESTONE 2 (Due Oct 03, 2026)                                                          |
|  [x] 1. schema.sql (Normalized SQLite DDL with cascading foreign keys)        -> DONE    |
|  [x] 2. db_manager.py (Persistence, ingestion, atomic transactions, CRUD)     -> DONE    |
|  [x] 3. templates/uphsd_ccs_template.html (Jinja2 institutional layout, PVM)   -> DONE    |
|  [x] 4. export_engine.py (SQLite-to-HTML/PDF compiler with print engine)      -> DONE    |
|  [ ] 5. 3-5 Minute Video Demonstration (Recorded screen capture walkthrough)  -> TO DO   |
+-----------------------------------------------------------------------------------------+
```

---

## 3. Collaborator's Creative Domain: UI/UX Design & Frontend Prompting

> [!IMPORTANT]
> **Directive from Christian to John Miko**:
> **You have full ownership to design, prompt, and customize the UI/UX frontend yourself!**  
> All backend logic, AI pipelines, database persistence, and Jinja2 compilers are completely decoupled and running via a clean REST API on **Port 8001**. You can freely prompt your AI assistant to style, reshape, or completely overhaul the user interface to match your personal vision and aesthetic preferences.

### What is Already Available on the Backend (Port 8001):
The backend server (`18thWeekOutput/app.py`) exposes simple JSON endpoints that your frontend can call via standard `fetch()`:

| Endpoint | Method | Purpose for Frontend |
|---|---|---|
| `GET /api/status` | `GET` | Health check for Ollama daemon and `qwen3.5:4b` |
| `GET /api/subjects` | `GET` | Returns 8 curriculum subjects with `is_persisted`, `has_json`, `has_html` flags |
| `GET /api/syllabus?code={code}` | `GET` | Returns full 18-week syllabus JSON (Course metadata, CLOs, 18 weekly schedule items with K/S/A) |
| `GET /api/database` | `GET` | Returns persisted courses list from SQLite (`obe_syllabus.db`) |
| `GET /api/audit?code={code}` | `GET` | Evaluates syllabus against the 7 CHED CMO 25 invariants (returns compliance score and checklist) |
| `GET /api/generation-state` | `GET` | Polls real-time progress percentage (`0..100%`), current stage, and terminal logs |
| `POST /api/generate` | `POST` | Starts background AI generation for a single subject or all 8 subjects in batch |
| `POST /api/update-clo` | `POST` | Updates a CLO statement in SQLite after validating active Bloom's verbs |
| `POST /api/subject/wipe` | `POST` | Selectively deletes a single course from SQLite and deletes its output artifacts without touching others |
| `POST /api/nuke` | `POST` | Wipes ALL generated files, resets SQLite database, and clears caches |
| `GET /outputs/{filename}` | `GET` | Serves official Jinja2 HTML syllabus files (`official_syllabus_{course_code}.html`) |

### Working Reference Frontend:
A fully functional reference implementation is already running in `18thWeekOutput/index.html`:
* **View 1 (`#view-studio`)**: Curriculum cards, Image 5 specification form with zero-typing autofill and faculty editing, generation HUD, selective **`🗑️ Wipe Course`** reset button, and CLO/Schedule inspection tabs.
* **View 2 (`#view-viewer`)**: Dedicated master-detail syllabus viewer with instant search, filter pills, and a one-click **`🖨️ Print / Save Vector PDF`** button.
* **View 3 (`#view-audit`)**: SQLite database table with active **`📄 View Official Syllabus`** CTA and live CHED CMO 25 accreditation badges.
* **Universal Command Palette (`Ctrl + K`)**: Instant keyboard navigation searching across course codes, titles, descriptions, categories, and direct action shortcuts.
* **Tab 2: PLO Alignment Matrix**: Displays pedagogical mapping against CHED CMO 25 s.2015 Program Outcomes. Not all dots are green by design — courses specialize in targeted outcomes to prevent academic outcome inflation.

**Your AI can modify `18thWeekOutput/index.html` directly**: change color themes, adjust component hierarchy, build custom visual cards, add animations, or rearrange the layout however you wish!

---

## 4. Remaining Milestone 2 Deliverables: Video Demonstration Runbook

The primary remaining item for Milestone 2 is **Deliverable 5: 3–5 Minute Video Demonstration**.

### Professor's Exact Requirement:
> *"5. 3-5 -Minute Video Demonstration: A recorded screen capture demonstrating an end-to-end run: passing a course description, storing the validated output in SQLite, manually editing one outcome, and rendering the final HTML file."*

### Minute-by-Minute Recording Storyboard:

| Time | Scene | Action to Perform on Screen | Talking Points / Explanation |
|---|---|---|---|
| **0:00 – 0:45** | **Launch & Architecture Overview** | 1. Open terminal and run `run_18thweek.bat` (or `python run_18thweek.py`).<br>2. Show server online at `http://127.0.0.1:8001`.<br>3. Open browser. | *"Hello Prof. Malitao, this is our Lesson 5 Midterm Mini-Project demonstration for the AI-Powered OBE Syllabus Generator. Our architecture runs locally with Ollama qwen3.5:4b, Pydantic v2 validation, SQLite persistence, and Jinja2 institutional compilation."* |
| **0:45 – 2:00** | **Course Specification & AI Generation** | 1. Select a subject (e.g., `BSCS 3112: Artificial Intelligence` or `BSCS 3111: Data Mining`).<br>2. Show auto-filled parameters (Course Title, Code, Catalogue Description, Target PLOs).<br>3. Click **Generate 18-Week OBE Syllabus**.<br>4. Show live progress HUD. | *"When a subject is selected, our system auto-fills the course parameters based on our BSCS curriculum catalog. We trigger local generation with Qwen, which formulates Bloom-compliant CLOs and an 18-week schedule strictly adhering to CHED CMO 25 s.2015."* |
| **2:00 – 3:15** | **SQLite Storage & Human-in-the-Loop CRUD** | 1. Navigate to the **Database view**.<br>2. Show the course persisted in SQLite tables.<br>3. Open the **Edit CLO** modal.<br>4. Modify an outcome statement with an active Bloom verb (e.g., *Analyze* or *Design*).<br>5. Click Save. | *"The validated syllabus is atomically stored across 4 normalized SQLite tables with cascading foreign keys. As required for human-in-the-loop oversight, faculty can modify any generated outcome. Our system validates the active Bloom verb before committing the update to SQLite."* |
| **3:15 – 4:30** | **Dedicated Viewer & Vector PDF Export** | 1. Switch to the **Dedicated Syllabus Viewer**.<br>2. Show the rendered Jinja2 syllabus.<br>3. Scroll through UPHSD header, PVM, 18-week table with K/S/A badges, and 70/30 grading formula.<br>4. Click **Print / Save Vector PDF** to show the browser print dialog. | *"Finally, our export engine queries SQLite by course code and renders the official institutional CCS syllabus via Jinja2, complete with tripartite K/S/A badges and the 70/30 grading formula. The user can export a clean, publication-ready vector PDF with one click."* |

---

## 5. Strict Verification Checklist (Based on Professor's Rubric)

Your collaborating AI should run these verification steps to prove **100% Exemplary (4-5 pts / 100%)** standing across all 4 rubric criteria:

### Criteria 1: Pydantic Schema & LLM Enforcement (25%)
* [x] **Strict JSON enforcement**: `llm_engine.py` calls Ollama with `format="json"` and `temperature=0.2`.
* [x] **CoT stripping**: Regex isolates JSON substring boundaries and strips `<think>...</think>` tokens.
* [x] **Automated retry loop**: Intercepts `ValidationError` or `JSONDecodeError` and re-prompts Qwen up to 3 times with specific feedback.

### Criteria 2: OBE Domain Alignment — Bloom's K/S/A (25%)
* [x] **Active Bloom's verbs**: `CourseOutcomeSchema` uses `@field_validator("description")` to reject unmeasurable verbs (`understand`, `know`, `learn`, `study`, `familiarize`, `be exposed to`).
* [x] **Tripartite K/S/A domains**: `LessonOutcomeSchema` strictly restricts `domain: Literal["K", "S", "A"]`.
* [x] **18-week schedule**: Exactly 18 weeks with Week 9 locked to Midterm Exam and Week 18 locked to Final Exam / Capstone Defense.

### Criteria 3: Database Design & CRUD Logic (25%)
* [x] **Normalized SQLite DDL**: `database/schema.sql` defines 4 tables: `courses`, `course_outcomes`, `weekly_schedules`, `lesson_outcomes`.
* [x] **Foreign keys & cascades**: `PRAGMA foreign_keys = ON` with `ON DELETE CASCADE` on all child tables.
* [x] **Clean CRUD operations**: `db_manager.py` implements `save_syllabus()`, `get_syllabus()`, `update_clo()`, and `list_courses()`.

### Criteria 4: Jinja2 Templating & Document Export (25%)
* [x] **Institutional layout**: `templates/uphsd_ccs_template.html` renders UPHSD Philosophy, Vision, Mission, Course Specification, CLO matrix, 18-week schedule, and signatories.
* [x] **Institutional grading formula**: Reflects 70% Class Standing (30% Quizzes, 20% Research, 50% Lab) + 30% Major Exam.
* [x] **Export engine**: `export_engine.py` exports browser-ready HTML and supports native vector PDF printing via `window.print()`.

---

## 6. How to Run and Test the System

### 1. Launch Ollama:
```bash
ollama serve
ollama pull qwen2.5
```

### 2. Launch the Web Studio (With UI):
```cmd
run_18thweek.bat
```
Or with Python:
```bash
python run_18thweek.py
```
Open **`http://127.0.0.1:8001/`** in your browser.

### 3. Run Headless CLI Pipeline (Without UI / CLI Only):
```cmd
run_18th_week.bat
```
*(Runs Milestone 1 generation, Milestone 2 SQLite persistence, CRUD test, and Jinja2 HTML syllabus export).*

### 3. Run Automated Validation Scripts:
```bash
# Test server endpoints and SQLite persistence
python scratch/test_endpoints.py

# Test DOM anchors and UI stylesheet contracts
node scratch/test_sim.js
```

---

## 7. Submission Checklist for Both Team Members
* [ ] Both Christian and John Miko maintain clean, up-to-date local copies of the repository.
* [ ] All deliverables are tested against `qwen2.5` / `qwen3.5:4b`.
* [ ] Record and submit the 3–5 minute video demonstration before the October 3, 2026 deadline.
* [ ] Submit your individual outputs as noted in the professor's guidelines: *"Each member of the group must submit their own output."*
