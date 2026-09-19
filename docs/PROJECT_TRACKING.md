# PROJECT_TRACKING.md — AI-Powered OBE Syllabus Generator Microservice

## Group Members & Leadership
* **Christian Ezekiel L. Carvajal** — Lead Architect & Systems Engineer (BSCS 3112)
* **John Miko P. Sarsalijo** — Collaborative Partner & Systems Engineer (BSCS 3112)
* **Academic Institution:** College of Computer Studies (CCS), University of Perpetual Help System DALTA (Molino Campus)
* **Subject:** BSCS 3112 / Artificial Intelligence (Lesson 5 - Midterm Mini-Project)
* **Course Evaluator:** Prof. Roberto L. Malitao

---

## Authoritative Specification Note
The master assignment instructions and official milestone schedule are archived at:
`C:\Users\chris\Downloads\2. Projects\3. Reviewer\4artificialIntelligence\Midterm\lesson3and4\txtFiles\continuationInstructionWithMilestones.txt`

---

## Tech Stack & Architecture Specifications
* **Core Language:** Python 3.10+ (tested on Python 3.14 / venv)
* **Local LLM Engine:** Ollama with `qwen3.5:4b` exclusively
* **Inference Endpoint:** `http://localhost:11434/api/generate` with `format="json"`
* **Data Contract Validation:** Pydantic v2 (`pydantic>=2.0`)
* **Relational Persistence:** SQLite 3 (`database/obe_syllabus.db`) with cascading foreign keys
* **Document Compilation:** Jinja2 (`jinja2>=3.1`) generating browser-ready HTML syllabi

---

## Milestone Execution Roadmap

### Milestone 1: Structured LLM Engine & Schema Validation
* **Target Due Date:** Saturday, September 26, 2026 (11:59 PM)
* **Status:** **COMPLETED & VERIFIED**
* **Deliverables Implemented:**
  1. `obe_schemas.py`:
     - `CourseMetadataSchema`: Full catalog parameters (code, title, units, lecture/lab hours, prerequisites, description).
     - `CourseOutcomeSchema` (CLO): 3–5 outcomes with `@field_validator("description")` enforcing active Bloom's Taxonomy cognitive verbs and rejecting weak verbs (`understand`, `know`, `learn`, `study`, `familiarize`, `be exposed to`).
     - `LessonOutcomeSchema` (LLO): Tripartite domain categorization strictly constrained to `domain: Literal["K", "S", "A"]` (Knowledge, Skills, Attitude).
     - `WeeklyScheduleSchema`: 18-week semester schedule schema with topics, tripartite LLOs, TLAs, assessment tasks, and resources.
     - `FullSyllabusSchema`: Aggregating metadata, 3–5 CLOs, and strict 18 weeks with cross-term K/S/A domain validation.
     - Preserved backward-compatible schemas (`CourseOutcome`, `CourseOutcomesPayload`, `WeeklyScheduleItem`, `FullSyllabusPayload`).
  2. `llm_engine.py`:
     - Low-level POST client calling `http://localhost:11434/api/generate` with `format="json"` and `temperature=0.2`.
     - Model engine strictly locked to `qwen3.5:4b`.
     - Multi-turn self-healing retry loop (max 3 attempts) intercepting `ValidationError`, `JSONDecodeError`, and `RequestException`.
     - Formats `exc.errors()` into corrective prompts for model self-correction.
     - Exposes `generate_syllabus(course_data: dict) -> FullSyllabusSchema`.
  3. `sample_validated_output.json`:
     - Fully AI-generated, schema-validated 18-week syllabus deliverable for *CS 3110: Data Structures and Algorithms*.

---

### Milestone 2: Relational Persistence, CRUD, & Document Assembly
* **Target Due Date:** Saturday, October 3, 2026 (11:59 PM)
* **Status:** **OPERATIONAL & VERIFIED**
* **Deliverables Implemented:**
  1. `database/schema.sql`:
     - Normalized DDL with 4 relational tables: `courses`, `course_outcomes`, `weekly_schedules`, `lesson_outcomes`.
     - Foreign keys enabled with `ON DELETE CASCADE`.
     - Authors attributed in SQL comments.
  2. `db_manager.py`:
     - `init_db(db_path)`: Executes `database/schema.sql`.
     - `save_syllabus(syllabus, db_path)`: Persists metadata, CLOs, weeks, and LLOs with atomic transactions into `database/obe_syllabus.db`.
     - `get_syllabus(course_code, db_path)`: Queries tables and reconstructs `FullSyllabusSchema`.
     - `update_clo(clo_id, new_description, db_path)`: Human-in-the-loop faculty outcome editing with Bloom validation.
  3. `templates/uphsd_ccs_template.html`:
     - Official institutional layout with UPHSD CCS branding, course specification table, CLO cognitive matrix, 18-week schedule with K/S/A badges, 70/30 grading formula, and signatory blocks.
  4. `export_engine.py`:
     - `render_syllabus_html(course_code, db_path)`: Compiles Jinja2 template.
     - `export_to_file(course_code, output_path, db_path)`: Exports browser-ready HTML file into `outputs/`.

---

## Automated Verification Logs & Audit Evidence

### 1. Pydantic Bloom Verb Rejection Test
```text
PASS: Rejected banned verb: 1 validation error for CourseOutcomeSchema
description
  Value error, Banned non-measurable verb 'understand' detected in outcome statement.
PASS: Allowed valid verb: Analyze algorithmic time complexity
PASS: Allowed valid domain: K
PASS: Rejected invalid domain: 'X'
```

### 2. Live LLM Engine Execution
```text
[*] Starting AI-Powered OBE Syllabus Generation Pipeline...
[*] Target LLM Model: qwen2.5:7b on http://localhost:11434
[+] Metadata parsed: CS 3110 - Data Structures and Algorithms
[*] [Stage 1: CLOs] Querying qwen2.5:7b (Attempt 1/3)...
[+] [Stage 1: CLOs] Successfully validated 4 Course Outcomes.
[*] [Stage 2: Schedule] Querying qwen2.5:7b for 18-week matrix (Attempt 1/3)...
[+] [Stage 2: Schedule] Successfully validated 18-week schedule.
[+] Root FullSyllabusSchema validation passed successfully!
[+] Validated syllabus persisted to 'outputs/sample_validated_output.json'.
```

### 3. Relational Database Persistence Test
```text
[+] Database initialized successfully at 'database/obe_syllabus.db'.
[+] Persisted syllabus for 'CS 3110' (Course ID: 1) into SQLite.
[+] Verification: Successfully read back 'Data Structures and Algorithms' with 18 weeks.
[+] Successfully updated CLO1 in SQLite database.
[+] CLO Update status: True
```

### 4. Jinja2 Document Export Test
```text
[*] Testing export engine for course 'CS 3110'...
[+] Successfully exported official syllabus to 'outputs/official_syllabus_CS_3110.html'.
[+] Verification: File size is 29,452 bytes.
```
