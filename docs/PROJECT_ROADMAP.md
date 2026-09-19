# PROJECT_ROADMAP.md — UPHSD CCS OBE Academic System Pipeline

## 1. Project Information
* **Subject:** Artificial Intelligence (BSCS 3112)
* **Module:** Lessons 3 & 4 — AI Integration & Academic System Development
* **Instructor:** Prof. Roberto L. Malitao
* **Student:** CARVAJAL, Christian Ezekiel L.
* **Target Due Date:** September 12, 2026
* **Status:** Complete / All Deliverables Verified (Exemplary Level)

---

## 2. Milestone Tracking

### Phase 1: Environment & Virtual Setup
- [x] Analyze lesson notes and lab guidelines from `txtFiles/context.txt`.
- [x] Confirm local Ollama service availability and `qwen3.5:4b` image integrity.
- [x] Create `requirements.txt` with `pydantic>=2.0.0` and `ollama>=0.2.0`.
- [x] Create `requirements.sh` (POSIX Bash) and `requirements.ps1` (PowerShell).
- [x] Initialize and activate isolated `.venv`.
- [x] Install and verify all Python package dependencies in `.venv` and global Python.

### Phase 2: Schema Definition (`obe_schemas.py`)
- [x] Implement `CourseOutcome` with `clo_number` (1-5), `bloom_level` Literal, `mapped_po`, and active verb validator.
- [x] Implement `CourseOutcomesPayload` enforcing 4–5 outcomes for catalog description.
- [x] Implement `LessonLearningOutcome` with tripartite `category` Literal ("K", "S", "A").
- [x] Implement `WeeklyScheduleItem` with 14-week range, `period` Literal ("PRELIM", "MIDTERM", "FINAL"), IT/CS TLAs, and assessment tools.
- [x] Implement `GradingBreakdown` with institutional weights (30% Quizzes, 20% Research, 50% Lab, 70% Class Standing, 30% Major Exam).
- [x] Implement `FullSyllabusPayload` enforcing exactly 14 weeks and full syllabus integrity.

### Phase 3: Stage 1 Generator (`lab1_1_generator.py` & `obe_json_generator.py`)
- [x] Construct `SYSTEM_PROMPT_LAB1_1` enforcing active Bloom's verbs and negative constraints.
- [x] Implement `generate_course_outcomes()` with Ollama `format="json"`.
- [x] Add `<think>` reasoning extraction and JSON substring boundary parsing.
- [x] Add 4-attempt auto-retry feedback loop on Pydantic `ValidationError`.
- [x] Run on Data Structures and Algorithms (`CS 3110`) and export `co_output_lab1_1.json`.
- [x] Create alias/copy `obe_json_generator.py`.

### Phase 4: Stage 2 Pipeline (`lab1_2_pipeline.py`)
- [x] Construct `SYSTEM_PROMPT_LAB1_2` with strict pedagogical and schedule business rules.
- [x] Implement `generate_weekly_schedule()` consuming `co_output_lab1_1.json`.
- [x] Enforce Week 7 Midterm lock and Week 14 Final lock.
- [x] Enforce 100% Course Outcome ID coverage across the 14-week schedule.
- [x] Add 4-attempt auto-retry feedback loop.
- [x] Export complete syllabus deliverable `sample_output_syllabus.json`.

### Phase 5: Verification & Rubric Audit
- [x] Execute automated verification assertion script (`verify_deliverables.py`).
- [x] Audit against Prof. Rob Malitao's 4-tier rubric criteria.
- [x] Confirm all 4 deliverables exist on disk.
- [x] Generate comprehensive walkthrough documentation.

---

## 3. Rubric Scorecard & Target Level

| Criteria | Achieved Level | Verification Evidence |
|---|---|---|
| **JSON Schema Enforcement** | **Exemplary (4)** | 100% valid, parseable JSON matching Pydantic models with zero manual intervention. Both generators ran through Ollama `format="json"`. |
| **OBE Pedagogy Alignment** | **Exemplary (4)** | Active Bloom's verbs only (`Identify`, `Implement`, `Analyze`, `Design`), mapped to POs 1–3, tripartite K/S/A, Week 7 Midterm and Week 14 Final locked. |
| **Error Handling & Code** | **Exemplary (4)** | Multi-turn automated re-prompting injecting Pydantic error details back to Ollama; clean modular Python structure. |
| **Deliverable Completeness** | **Exemplary (4)** | All required files verified on disk: `obe_schemas.py`, `lab1_1_generator.py`, `obe_json_generator.py`, `lab1_2_pipeline.py`, `co_output_lab1_1.json`, `sample_output_syllabus.json`. |

---

## 4. Lesson 5: Midterm Mini-Project Tracking (OBE Syllabus Generator Microservice)
* **Lead Architect:** Christian Ezekiel L. Carvajal
* **Collaborative Partner:** John Miko P. Sarsalijo
* **Target Due Dates:** Milestone 1 (Sept 26, 2026) | Milestone 2 (Oct 3, 2026)
* **Master Specification:** `txtFiles/continuationInstructionWithMilestones.txt`

### Milestone 1 Deliverables (Status: VERIFIED & COMPLETE)
- [x] **`obe_schemas.py`**: Pydantic v2 schemas (`CourseMetadataSchema`, `CourseOutcomeSchema`, `LessonOutcomeSchema`, `WeeklyScheduleSchema`, `FullSyllabusSchema`).
  - Strict Bloom's verb enforcement rejecting unmeasurable verbs (`understand`, `know`, `learn`, `study`).
  - Tripartite domain constraint (`K`, `S`, `A`).
  - 18-week semester schedule with cross-schedule K/S/A coverage validation.
- [x] **`llm_engine.py`**: Local Ollama interaction layer calling `http://localhost:11434/api/generate` with `format="json"`.
  - Automated self-healing retry loop (max 3 attempts) capturing `ValidationError` details.
  - Model auto-fallback supporting `qwen2.5:7b` and `qwen3.5:4b`.
  - Exposed `generate_syllabus(course_data: dict) -> FullSyllabusSchema`.
- [x] **`sample_validated_output.json`**: AI-generated and validated 18-week syllabus for *CS 3110: Data Structures and Algorithms*.

### Milestone 2 Scaffolding & Stubs (Status: OPERATIONAL)
- [x] **`schema.sql`**: Normalized SQLite DDL (`courses`, `course_outcomes`, `weekly_schedules`, `lesson_outcomes`) with foreign keys & cascading deletes.
- [x] **`db_manager.py`**: Persistence layer implementing `init_db()`, `save_syllabus()`, `get_syllabus()`, and `update_clo()`.
- [x] **`templates/uphsd_ccs_template.html`**: Institutional Jinja2 HTML layout with UPHSD CCS branding and 70/30 grading formula.
- [x] **`export_engine.py`**: Document compilation interface exporting `official_syllabus_CS_3110.html`.

