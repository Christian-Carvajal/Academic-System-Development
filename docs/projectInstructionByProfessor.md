# projectInstructionByProfessor.md — Lesson 5 Midterm Mini-Project Specification

> **Source Document:** `Lesson 5 - Midterm Mini-Project.pdf`  
> **Course:** Artificial Intelligence — Laboratory (BSCS 3112)  
> **Instructor / Prepared By:** Prof. Roberto L. Malitao  
> **Date Issued:** September 18, 2026  
> **Due Dates:** Milestone 1 (Sept 26, 2026) | Milestone 2 (October 3, 2026)  
> **Mode:** Collaborative Pair Programming (Groups of 2)  
> **Environment:** 100% Software-Simulated Desktop Execution (Zero-Hardware)  
> **Tech Stack:** Python 3.10+, Local Ollama (`qwen2.5` / `qwen3.5:4b`), Pydantic v2, SQLite 3, Jinja2  

---

## Part 1: Verbatim Raw Project Specification by Professor

```text
================================================================================
ARTIFICIAL INTELLIGENCE - LAB
LESSON 5 – MIDTERM MINI-PROJECT: OBE SYLLABUS GENERATOR
================================================================================

1. Project Overview & Business Scenario:
The College of Computer Studies (CCS) quality assurance committee requires a local 
microservice to automate the drafting of Outcome-Based Education (OBE) course syllabi.

You and your partner will build an end-to-end Python engine that accepts raw course 
parameters, leverages a local Qwen model to formulate Bloom-aligned outcomes and an 
18-week schedule, validates the output using Pydantic, persists the data in an SQLite 
database for human-in-the-loop edits, and exports the final syllabus into the official 
institutional HTML layout.

--------------------------------------------------------------------------------
2. Learning Objectives:
By completing this mini project, students will be able to:

• Knowledge (K) – Cognitive:
  - Analyze raw academic course parameters to identify dynamic components versus 
    static institutional syllabus metadata.
  - Explain how Pydantic data schemas enforce deterministic boundaries on 
    probabilistic LLM responses.

• Skills (S) – Psychomotor/Practical:
  - Develop a chained Python pipeline querying Ollama/Qwen in JSON mode with automatic 
    exception handling and re-prompting.
  - Design & Implement a normalized SQLite database (schema.sql) to persist multi-tiered 
    syllabus entities (courses, course_outcomes, weekly_schedules, lesson_outcomes).
  - Construct a Jinja2 export engine that injects relational database records into 
    the official CCS syllabus layout.

• Attitude (A) – Affective:
  - Value quality assurance and domain precision when handling academic curriculum standards.
  - Demonstrate persistence in debugging multi-stage software pipelines 
    (LLM → Validation → Persistence → Rendering).

--------------------------------------------------------------------------------
3. Project Milestones & Schedule (Sept 18 – Oct 3, 2026):

[Milestone 1 - Sept 26, 2026]
Submission Deadline: Friday, September 25, 2026 (11:59 PM)
Focus: Prompt Engineering, Pydantic Data Contracts, and JSON Parsing Logic.
Deliverables:
  1. obe_schemas.py: Pydantic models for CourseMetadataSchema, CourseOutcomeSchema, 
     and WeeklyScheduleSchema with K/S/A validation rules.
  2. llm_engine.py: Ollama API wrapper using system prompts and format="json" to generate 
     validated CLOs and an 18-week schedule plan. Includes an automated retry loop 
     (max 3 attempts) on ValidationError or JSONDecodeError.
  3. sample_validated_output.json: An AI-generated JSON file for a sample CS/IT course 
     (e.g., Data Structures and Algorithms or Web Development).

[Milestone 2 - Oct 03, 2026 Final System Submission & Demo]
Submission Deadline: Saturday, October 3, 2026 (11:59 PM)
Focus: Database Ingestion, Faculty Edit Interface, and Institutional Document Export.
Deliverables:
  1. schema.sql: DDL script creating normalized tables for courses, outcomes, schedule 
     weeks, and LLOs with foreign keys.
  2. db_manager.py: Python module handling database initialization, structured JSON 
     ingestion, and CRUD functions (e.g., modifying a generated CLO before saving).
  3. templates/uphsd_ccs_template.html: Jinja2 template styled according to the official 
     CCS syllabus layout.
  4. export_engine.py: Compilation script that queries SQLite by course_code and exports 
     a complete, browser-ready HTML/PDF syllabus file.
  5. 3-5 -Minute Video Demonstration: A recorded screen capture demonstrating an end-to-end 
     run: passing a course description, storing the validated output in SQLite, manually 
     editing one outcome, and rendering the final HTML file.

--------------------------------------------------------------------------------
4. Assessment Rubric (100 Points Total):

CRITERIA 1: Pydantic Schema & LLM Enforcement (25%)
  • Exemplary (4-5 pts / 100%): Strictly enforces JSON output from Ollama/Qwen. 
    Implements automated retry logic on Pydantic ValidationError.
  • Proficient (3 pts / 75%): Enforces JSON output, but lacks auto-retry on validation failure.
  • Developing (1-2 pts / 50%): JSON syntax breaks frequently; requires manual code edits to run.
  • Unacceptable (0 pts): Fails to enforce JSON output; returns raw, unstructured free text.

CRITERIA 2: OBE Domain Alignment (Bloom's KSA) (25%)
  • Exemplary (4-5 pts / 100%): CLOs use active Bloom's verbs; weekly LLOs are explicitly 
    categorized into Knowledge (K), Skills (S), and Attitude (A).
  • Proficient (3 pts / 75%): CLOs use active verbs, but weekly LLOs miss one or two K/S/A categories.
  • Developing (1-2 pts / 50%): Uses vague verbs (e.g., "understand", "know"); fails Bloom's standards.
  • Unacceptable (0 pts): Generated content does not reflect Outcome-Based Education principles.

CRITERIA 3: Database Design & CRUD Logic (25%)
  • Exemplary (4-5 pts / 100%): SQLite DB is normalized with foreign keys and cascading 
    deletes; CRUD operations update relational tables cleanly.
  • Proficient (3 pts / 75%): SQLite DB stores data across tables, but has minor schema 
    redundancies or missing foreign keys.
  • Developing (1-2 pts / 50%): Stores the entire syllabus as an unnormalized flat text or 
    raw JSON string in SQLite.
  • Unacceptable (0 pts): Database script fails to execute or crashes on insertion.

CRITERIA 4: Jinja2 Templating & Document Export (25%)
  • Exemplary (4-5 pts / 100%): Output accurately matches institutional CCS layout (PVM, 
    tables, grading matrix). Clean HTML rendering without missing fields.
  • Proficient (3 pts / 75%): Renders HTML successfully, but has minor styling or alignment 
    defects relative to the official syllabus.
  • Developing (1-2 pts / 50%): Generated HTML displays unformatted or unaligned database fields.
  • Unacceptable (0 pts): Export engine fails to compile or render the Jinja2 template.

--------------------------------------------------------------------------------
5. List of Tools & Libraries:

1. Core Execution Environment & Local AI Engine:
  • Python: 3.10+ (System Installer) — Core programming language for backend pipeline, 
    data validation, and database operations.
  • Ollama: Latest (System Application) — Local background service running on localhost:11434.
  • Qwen: qwen2.5 / qwen3.5:4b (`ollama pull qwen2.5`) — Local Large Language Model.

2. Third-Party Python Libraries (pip Packages):
  Command: pip install pydantic jinja2 requests
  • pydantic: Data Contract & Schema Enforcement.
  • jinja2: Templating & Document Assembly Engine.
  • requests: HTTP Client sending POST requests to http://localhost:11434/api/generate.

3. Standard Python Built-in Libraries (No pip install Required):
  • sqlite3 (import sqlite3): Relational database engine for obe_syllabus.db.
  • json (import json): Serializing and parsing JSON strings.
  • typing (from typing import List, Literal): Explicit type hints.
  • time (import time): Benchmarking execution performance.

4. Developer Tools & Interfaces:
  • Code Editor: VS Code (Visual Studio Code).
  • Database Inspector: SQLite CLI or DB Browser for SQLite.
  • Document Viewer: Any Web Browser (Chrome, Edge, Firefox) for HTML & PDF preview.
  • Terminal: PowerShell (Windows) or Terminal (macOS/Linux).

5. Summary Cheat Sheet for Student Setup:
  # 1. Verify Python Installation
  python --version

  # 2. Verify Ollama and Pull Qwen Model
  ollama list
  ollama pull qwen2.5

  # 3. Install All Required Python Libraries (Single Command)
  pip install pydantic jinja2 requests

Note:
Each member of the group must submit their own output.
================================================================================
```

---

## Part 2: AI Verification & Implementation Audit Guide for Milestone 2

> [!IMPORTANT]
> **Collaborator AI Attention Notice**: This section defines the precise technical mappings, file locations, verification assertions, and video demonstration requirements to guarantee **100% Exemplary (100/100 points)** compliance on Milestone 2.

```text
+-----------------------------------------------------------------------------------------+
|                         MILESTONE 2 DELIVERABLES MAPPING TABLE                          |
+-----------------------------------------------------------------------------------------+
| Professor's Requirement         | Repository Implementation & File Path                 |
+---------------------------------+-------------------------------------------------------+
| 1. schema.sql                   | 18thWeekOutput/database/schema.sql                    |
| 2. db_manager.py                | 18thWeekOutput/db_manager.py                          |
| 3. uphsd_ccs_template.html      | 18thWeekOutput/templates/uphsd_ccs_template.html      |
| 4. export_engine.py             | 18thWeekOutput/export_engine.py                       |
| 5. 3-5 Min Video Demonstration  | See Section 2.5 below for step-by-step recording plan |
+-----------------------------------------------------------------------------------------+
```

### 2.1 Deliverable 1: `schema.sql` (Normalized SQLite DDL)
* **Location:** [`18thWeekOutput/database/schema.sql`](file:///C:/Users/chris/Downloads/2.%20Projects/3.%20Reviewer/4artificialIntelligence/Midterm/lesson3and4/submission_deliverables/18thWeekOutput/database/schema.sql)
* **Status:** **VERIFIED & OPERATIONAL**
* **Rubric Requirement:** SQLite DB normalized with foreign keys and cascading deletes (`ON DELETE CASCADE`). No flat unnormalized JSON tables.
* **Schema Topology:**
  1. `courses`: Stores `id`, `course_code` (UNIQUE), `course_title`, `credit_units`, `lecture_hours`, `lab_hours`, `prerequisites`, `course_description`, `created_at`.
  2. `course_outcomes`: Child table linked via `course_id REFERENCES courses(id) ON DELETE CASCADE`. Stores `clo_id`, `bloom_level`, `description`, `program_outcomes_mapped`.
  3. `weekly_schedules`: Child table linked via `course_id REFERENCES courses(id) ON DELETE CASCADE`. Stores `week_number` (1..18), `period`, `topics`, `teaching_learning_activities`, `assessment_tasks`, `resources`.
  4. `lesson_outcomes`: Granular child table linked via `schedule_id REFERENCES weekly_schedules(id) ON DELETE CASCADE`. Stores `llo_id`, `domain` (CHECK constraint: `'K'`, `'S'`, `'A'`), `description`.

### 2.2 Deliverable 2: `db_manager.py` (Persistence & CRUD Layer)
* **Location:** [`18thWeekOutput/db_manager.py`](file:///C:/Users/chris/Downloads/2.%20Projects/3.%20Reviewer/4artificialIntelligence/Midterm/lesson3and4/submission_deliverables/18thWeekOutput/db_manager.py)
* **Status:** **VERIFIED & OPERATIONAL**
* **Rubric Requirement:** Database initialization, structured JSON ingestion, and CRUD operations (specifically updating a generated CLO before saving/rendering).
* **Key Functions Implemented:**
  - `init_db(db_path)`: Connects with `PRAGMA foreign_keys = ON` and executes `schema.sql`.
  - `save_syllabus(syllabus: FullSyllabusSchema, db_path)`: Atomically persists metadata, CLOs, weeks, and LLOs with transactions.
  - `get_syllabus(course_code: str, db_path) -> Optional[FullSyllabusSchema]`: Reconstructs the complete Pydantic model from relational tables.
  - `update_clo(clo_id: str, new_description: str, db_path, course_code)`: **Faculty Human-in-the-Loop editor**. Validates that the new statement begins with an active Bloom's verb and updates the relational record in SQLite.
  - `list_courses(db_path)`: Summarizes all courses with CLO count and weekly schedule length.

### 2.3 Deliverable 3: `templates/uphsd_ccs_template.html` (Institutional Layout)
* **Location:** [`18thWeekOutput/templates/uphsd_ccs_template.html`](file:///C:/Users/chris/Downloads/2.%20Projects/3.%20Reviewer/4artificialIntelligence/Midterm/lesson3and4/submission_deliverables/18thWeekOutput/templates/uphsd_ccs_template.html)
* **Status:** **VERIFIED & OPERATIONAL**
* **Rubric Requirement:** Accurately matches institutional CCS layout (Philosophy, Vision, Mission, tables, grading matrix). Clean rendering without missing fields.
* **Layout Structure:**
  - Official UPHSD DALTA Institutional Header & College of Computer Studies Banner.
  - University Philosophy, Vision, Mission, and Core Values.
  - Course Specification Table (Course Code, Title, Units, Hours, Prerequisite).
  - Course Learning Outcomes (CLOs) Cognitive Matrix with Bloom Taxonomy levels.
  - 18-Week Detailed Instructional Schedule with Knowledge (K), Skills (S), and Attitude (A) color badges.
  - Institutional Grading Formula: 70% Class Standing (30% Quizzes, 20% Research, 50% Lab) + 30% Major Exam.
  - Academic Policies, Textbook References, and Institutional Signatory Blocks (Faculty, Department Chair, Dean).
  - High-resolution vector `@media print` CSS engine for native browser printing to PDF without layout clipping.

### 2.4 Deliverable 4: `export_engine.py` (Jinja2 Document Assembly)
* **Location:** [`18thWeekOutput/export_engine.py`](file:///C:/Users/chris/Downloads/2.%20Projects/3.%20Reviewer/4artificialIntelligence/Midterm/lesson3and4/submission_deliverables/18thWeekOutput/export_engine.py)
* **Status:** **VERIFIED & OPERATIONAL**
* **Rubric Requirement:** Compilation script that queries SQLite by `course_code` and exports a complete, browser-ready HTML/PDF syllabus file.
* **Key Functions Implemented:**
  - `render_syllabus_html(course_code, db_path)`: Queries SQLite, reconstructs `FullSyllabusSchema`, and renders the Jinja2 template.
  - `export_to_file(course_code, output_path, db_path)`: Compiles and writes the browser-ready document to `outputs/official_syllabus_{course_code}.html`.

### 2.5 Deliverable 5: 3–5 Minute Video Demonstration Runbook
* **Format:** Recorded Screen Capture with Voiceover or Clear Annotations (3 to 5 minutes).
* **Demonstration Step-by-Step Script:**
  1. **Step 1: Launch Application (0:00 - 0:45)**:
     - Run `run_18thweek.bat` in terminal. Show local Ollama connection (`qwen3.5:4b` online) and web server start on Port 8001.
     - Open browser to `http://127.0.0.1:8001/`. Introduce the 3-view application shell (`Curriculum Studio`, `Dedicated Syllabus Viewer`, `Database & Audit`).
  2. **Step 2: Subject Selection & Generation (0:45 - 2:00)**:
     - Select a curriculum subject (e.g., `BSCS 3112: Artificial Intelligence` or `BSCS 3111: Data Mining`).
     - Point out the auto-filled Course Specification form (Image 5 specification: Course Code, Title, Catalog Description, Target PLOs).
     - Click **`⚡ Generate 18-Week OBE Syllabus (Qwen 3.5 4B)`**.
     - Show the real-time Progress HUD streaming logs and validating Bloom-compliant outcomes.
  3. **Step 3: Relational Database Persistence & Human-in-the-Loop Edit (2:00 - 3:15)**:
     - Switch to **`🛡️ Relational Database & Audit`**.
     - Show the course persisted in SQLite with relational foreign keys.
     - Click **`✏️ Edit in Studio`** or use the **`✏️ Edit CLO`** button in the CLO tab.
     - Demonstrate editing an outcome statement (e.g., updating with a strong Bloom verb like *Analyze* or *Design*).
     - Show that the update immediately commits to SQLite database (`database/obe_syllabus.db`).
  4. **Step 4: Dedicated Syllabus Viewer & Vector PDF Export (3:15 - 4:30)**:
     - Switch to **`📄 Dedicated Syllabus Viewer & Print Studio`** (or click **`📄 View Official Syllabus`** directly from the database table).
     - Demonstrate the master-detail split layout, instant course search, and filter pills (`All`, `✓ Generated`, `⏳ Ready`).
     - Inspect the rendered Jinja2 document: UPHSD header, PVM, 18-week schedule with K/S/A badges, 70/30 grading formula, and signatory blocks.
     - Click **`🖨️ Print / Save Vector PDF`** to show the browser print dialog exporting a publication-grade vector PDF.

---

## Part 3: Automated Verification Checkpoints

The following tests verify that all Milestone 2 rubric requirements are completely satisfied in the repository:

1. **Database Relational Check**:
   ```powershell
   python -c "from db_manager import list_courses; print('Persisted:', list_courses())"
   ```
2. **Jinja2 Export Check**:
   ```powershell
   python -c "from export_engine import export_to_file; export_to_file('BSCS 3111')"
   ```
3. **Automated DOM & Contract Simulation**:
   ```powershell
   node scratch/test_sim.js
   ```
4. **CHED CMO 25 Invariant Compliance**:
   Open `http://127.0.0.1:8001/` and inspect **`🛡️ Database & Audit`** to verify all 7 invariant checks pass with 100% compliance.
