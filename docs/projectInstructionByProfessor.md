# Project Instruction by Professor — Lesson 5 Midterm Mini-Project

Date: September 18, 2026

Artificial Intelligence - Lab  
Lesson 5 – Midterm Mini - Project  

## MIDTERM MINI-PROJECT: OBE SYLLABUS GENERATOR

* **Mode:** Collaborative Pair Programming (Groups of 2)
* **Due Date:** September 26 and October 3, 2026
* **Environment:** 100% Software-Simulated Desktop Execution (Zero-Hardware)

### Project Specification:
AI-Powered OBE Syllabus Generator microservice
* **Execution Window:** September 18 – October 3, 2026
* **Stack:** Python 3.10+, Local Ollama (Qwen 2.5), Pydantic, SQLite, Jinja2

---

### 1. Project Overview & Business Scenario:

The College of Computer Studies (CCS) quality assurance committee requires a local microservice to automate the drafting of Outcome-Based Education (OBE) course syllabi.

You and your partner will build an end-to-end Python engine that accepts raw course parameters, leverages a local Qwen model to formulate Bloom-aligned outcomes and an 18-week schedule, validates the output using Pydantic, persists the data in an SQLite database for human-in-the-loop edits, and exports the final syllabus into the official institutional HTML layout.

---

### 2. Learning Objectives:

By completing this mini project, students will be able to:

* **Knowledge (K) – Cognitive:**
  * Analyze raw academic course parameters to identify dynamic components versus static institutional syllabus metadata.
  * Explain how Pydantic data schemas enforce deterministic boundaries on probabilistic LLM responses.

* **Skills (S) – Psychomotor/Practical:**
  * Develop a chained Python pipeline querying Ollama/Qwen in JSON mode with automatic exception handling and re-prompting.
  * Design & Implement a normalized SQLite database (schema.sql) to persist multi-tiered syllabus entities (courses, course_outcomes, weekly_schedules, lesson_outcomes).
  * Construct a Jinja2 export engine that injects relational database records into the official CCS syllabus layout.

* **Attitude (A) – Affective:**
  * Value quality assurance and domain precision when handling academic curriculum standards.
  * Demonstrate persistence in debugging multi-stage software pipelines (LLM → Validation → Persistence → Rendering).

---

### 3. Project Milestones & Schedule (Sept 18 – Oct 3, 2026)

* **Milestone 1** - Sept 26, 2026
* **Milestone 2** - Oct 03, 2026 Final System Submission & Demo

#### Milestone 1: Structured LLM Engine & Schema Validation
* **Submission Deadline:** Friday, September 25, 2026 (11:59 PM)
* **Focus:** Prompt Engineering, Pydantic Data Contracts, and JSON Parsing Logic.
* **Deliverables:**
  1. `obe_schemas.py`: Pydantic models for CourseMetadataSchema, CourseOutcomeSchema, and WeeklyScheduleSchema with K/S/A validation rules.
  2. `llm_engine.py`: Ollama API wrapper using system prompts and format="json" to generate validated CLOs and an 18-week schedule plan. Includes an automated retry loop (max 3 attempts) on ValidationError or JSONDecodeError.
  3. `sample_validated_output.json`: An AI-generated JSON file for a sample CS/IT course (e.g., Data Structures and Algorithms or Web Development).

#### Milestone 2: Relational Persistence, CRUD, & Jinja2 Document Assembly
* **Submission Deadline:** Saturday, October 3, 2026 (11:59 PM)
* **Focus:** Database Ingestion, Faculty Edit Interface, and Institutional Document Export.
* **Deliverables:**
  1. `schema.sql`: DDL script creating normalized tables for courses, outcomes, schedule weeks, and LLOs with foreign keys.
  2. `db_manager.py`: Python module handling database initialization, structured JSON ingestion, and CRUD functions (e.g., modifying a generated CLO before saving).
  3. `templates/uphsd_ccs_template.html`: Jinja2 template styled according to the official CCS syllabus layout.
  4. `export_engine.py`: Compilation script that queries SQLite by course_code and exports a complete, browser-ready HTML/PDF syllabus file.
  5. **3-5 -Minute Video Demonstration:** A recorded screen capture demonstrating an end-to-end run: passing a course description, storing the validated output in SQLite, manually editing one outcome, and rendering the final HTML file.

---

### 4. Assessment Rubric (100 Points Total)

| Evaluation Criteria | Exemplary (4-5 pts / 100%) | Proficient (3 pts / 75%) | Developing (1-2 pts / 50%) | Unacceptable (0 pts) | Weight |
|---|---|---|---|---|---|
| **Pydantic Schema & LLM Enforcement** | Strictly enforces JSON output from Ollama/Qwen. Implements automated retry logic on Pydantic ValidationError. | Enforces JSON output, but lacks auto-retry on validation failure. | JSON syntax breaks frequently; requires manual code edits to run. | Fails to enforce JSON output; returns raw, unstructured free text. | 25% |
| **OBE Domain Alignment (Bloom's KSA)** | CLOs use active Bloom's verbs; weekly LLOs are explicitly categorized into Knowledge (K), Skills (S), and Attitude (A). | CLOs use active verbs, but weekly LLOs miss one or two K/S/A categories. | Uses vague verbs (e.g., "understand", "know"); fails Bloom's standards. | Generated content does not reflect Outcome-Based Education principles. | 25% |
| **Database Design & CRUD Logic** | SQLite DB is normalized with foreign keys and cascading deletes; CRUD operations update relational tables cleanly. | SQLite DB stores data across tables, but has minor schema redundancies or missing foreign keys. | Stores the entire syllabus as an unnormalized flat text or raw JSON string in SQLite. | Database script fails to execute or crashes on insertion. | 25% |
| **Jinja2 Templating & Document Export** | Output accurately matches institutional CCS layout (PVM, tables, grading matrix). Clean HTML rendering without missing fields. | Renders HTML successfully, but has minor styling or alignment defects relative to the official syllabus. | Generated HTML displays unformatted or unaligned database fields. | Export engine fails to compile or render the Jinja2 template. | 25% |

---

### 5. List of Tools & Libraries

#### 1. Core Execution Environment & Local AI Engine
* **Python (3.10+):** System Installer — Core programming language for backend pipeline, data validation, and database operations.
* **Ollama (Latest):** System Application — Local background service that hosts and runs the Large Language Model on `localhost:11434`.
* **Qwen (`qwen2.5` or `qwen2.5:7b` / `qwen2.5:3b`):** `ollama pull qwen2.5` — The local Large Language Model responsible for generating Bloom-aligned Course Outcomes (CLOs) and 18-week schedules.

#### 2. Third-Party Python Libraries (pip Packages)
Install command:
```bash
pip install pydantic jinja2 requests
```
* **Pydantic (`pydantic`):** Data Contract & Schema Enforcement: Validates JSON outputs from Ollama/Qwen, enforcing data types, non-null rules, and Bloom's Taxonomy constraints before database insertion.
* **Jinja2 (`jinja2`):** Templating & Document Assembly Engine: Injects stored database records into the official institutional HTML layout without mixing HTML and Python code.
* **Requests (`requests`):** HTTP Client: Sends API requests (POST) to the local Ollama REST endpoint (`http://localhost:11434/api/generate`).

#### 3. Standard Python Built-in Libraries (No pip install Required)
* **`sqlite3` (`import sqlite3`):** Relational database engine for persisting course metadata, outcomes, mapping matrices, and weekly schedules into `obe_syllabus.db`.
* **`json` (`import json`):** Serializing Python dictionaries into JSON strings for Ollama prompts and parsing incoming raw LLM strings.
* **`typing` (`from typing import List, Literal`):** Providing explicit type hints for Pydantic models (e.g., restricted choices like `Literal["K", "S", "A"]`).
* **`time` (`import time`):** Benchmarking batch generation performance across the 3rd Year subjects.

#### 4. Developer Tools & Interfaces
* **Code Editor / IDE:** VS Code (Visual Studio Code) — Primary development environment for writing Python scripts, HTML templates, and SQL schemas.
* **Database Inspector:** SQLite CLI or DB Browser for SQLite — Visual GUI or command-line tool for inspecting, querying, and verifying relational tables inside `obe_syllabus.db`.
* **Document Viewer:** Any Web Browser (Chrome, Edge, Firefox) — Previewing and printing the generated Jinja2 HTML syllabus files to PDF format.
* **Terminal / Shell:** PowerShell (Windows) or Terminal (macOS/Linux) — Executing batch Python scripts and managing the local Ollama background process.

#### 5. Summary Cheat Sheet for Student Setup
```bash
# 1. Verify Python Installation
python --version

# 2. Verify Ollama and Pull Qwen Model
ollama list
ollama pull qwen2.5

# 3. Install All Required Python Libraries (Single Command)
pip install pydantic jinja2 requests
```

> **Note:** Each member of the group must submit their own output.
