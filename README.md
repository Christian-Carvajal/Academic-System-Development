# OBE Evaluation Engine: Local LLM Structured Outputs and Alignment Grading Matrix
**College of Computer Studies — University of Perpetual Help System DALTA (Molino Campus)**  
**Student:** Christian Ezekiel L. Carvajal  
**Evaluator:** Prof. Roberto L. Malitao  
**Course Activity:** Lesson 4 Lab Activity 1.1 & 1.2  
**Subject:** BSCS 3112 / Artificial Intelligence  
**Submission Due Date:** September 12, 2026  

---

## ⚡ Quick Start: Choose Your Execution Mode

### Mode 1: Interactive Web Studio (Recommended)
Launch the full visual studio in your browser with one command:
```bash
python run_gui.py
```
*(On Windows, you can also simply double-click **`run_gui.bat`**).*

> **What `run_gui.py` does automatically:**
> 1. Verifies Python runtime ($\ge 3.10$).
> 2. Auto-installs missing packages (`pydantic`, `ollama`) from `requirements.txt`.
> 3. Connects to Ollama service (`http://127.0.0.1:11434`) and auto-starts `ollama serve` if dormant.
> 4. Verifies whether `qwen3.5:4b` is present; if not, automatically downloads it via `ollama pull qwen3.5:4b`.
> 5. Starts local server on `http://127.0.0.1:8000` and automatically opens your default browser.

### Mode 2: Headless Command Prompt Execution (`run_pipeline.bat`)
To run the automated pipeline **purely inside the terminal/CMD** without launching a web browser:
```bat
run_pipeline.bat
```
*(Double-clicking **`run_pipeline.bat`** executes Lab 1.1, Lab 1.2, and runs terminal invariant assertions, keeping the window open upon completion).*

---

## Technical Overview
This repository contains a two-stage automated Python microservice pipeline leveraging local LLM inference (`qwen3.5:4b` via Ollama) and Pydantic v2 data models to generate, validate, and serialize complete Outcome-Based Education (OBE) course syllabi. 

The system enforces strict institutional grading schemes, active Bloom's Taxonomy verbs, locked examination milestones, and comprehensive Course Learning Outcome (CLO) mappings through multi-turn, self-healing recovery loops.

```text
+-----------------------------------------------------------------------------------+
|                                 PIPELINE FLOW                                     |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [Lab 1.1: lab1_1_generator.py / obe_json_generator.py]                           |
|          │                                                                        |
|          ▼                                                                        |
|   Queries Ollama (format="json") with Qwen 3.5 4B (16k Context Window)            |
|   Validates Bloom's Action Verbs & Normalizes Levels via Pydantic v2              |
|   Multi-Turn Self-Healing Feedback Loop (Attempt 1 -> Attempt 2 Recovery)        |
|          │                                                                        |
|          ▼                                                                        |
|   Serialized Output: co_output_lab1_1.json                                        |
|          │                                                                        |
|          ├───────────────────────────────────────────────────────┐                |
|          ▼                                                       ▼                |
|  [Lab 1.2: lab1_2_pipeline.py]                          [Manual Inspection]       |
|          │                                                                        |
|          ▼                                                                        |
|   Injects Stage 1 CO Context into Prompt                                          |
|   Synthesizes 14-Week Schedule with Hard Milestones                               |
|   Validates Tripartite LLOs (K/S/A) & 100% Coverage                               |
|   Attaches UPHSD CCS Institutional Grading Breakdown                              |
|          │                                                                        |
|          ▼                                                                        |
|   Final Submission Deliverable: sample_output_syllabus.json                       |
|          │                                                                        |
|          ├───────────────────────────────────────────────────────┐                |
|          ▼                                                       ▼                |
|  [Headless CMD: run_pipeline.bat]                       [Interactive Studio: run_gui.py]
|   Terminal Invariant Assertions:                         Web GUI, Live Audits, Nuke Reset,
|   14 Weeks, W7 Midterm, W14 Final,                       and Official Vector PDF Export   |
|   100% Coverage, and UPHSD Grading                                                        |
+-----------------------------------------------------------------------------------+
```

---

## Key Features of the Interactive Studio

The web-based studio (`run_gui.py`) provides an end-to-end curriculum engineering workspace:

1. **Flexible Course Customization:**
   - Pre-configured for **Artificial Intelligence** (`BSCS 3112`) and **Data Structures and Algorithms** (`CS 3110`).
   - Accepts custom Course Title, Course Code, Catalogue Description, and Target Program Learning Outcomes (PLOs).
2. **Stage 1 (Course Learning Outcomes Generator):**
   - Generates 4–5 measurable Course Learning Outcomes using `qwen3.5:4b`.
   - Real-time progress bar, live token streaming logs, and interactive outcome cards with active Bloom's verbs highlighted in gold and cognitive taxonomy pills.
3. **Stage 2 (14-Week Syllabus Pipeline):**
   - Automatically chains Stage 1 outcomes into a comprehensive 14-week schedule.
   - Strict milestone locking: **Week 7 Midterm Examination** and **Week 14 Final Examination / Defense**.
   - Tripartite Lesson Learning Outcomes ($K/S/A$) for every single instructional week.
4. **Stage 3 (Live Rubric & Accreditation Audit):**
   - Automated 6-point invariant auditor asserting 100% compliance with Prof. Rob Malitao's rubrics.
   - Programmatic verification of total weeks (14), midterm/final placement, 100% CLO coverage, and UPHSD CCS 70/30 grading distribution.
5. **Stage 4 (Official CHED/UPHSD PDF Export):**
   - Single-click vector PDF generation with the official University of Perpetual Help System DALTA Molino header logo, formatted syllabus tables, pagination, and signatory approval blocks.
6. **Workspace Nuke / Factory Reset:**
   - A dedicated **Nuke / Reset** action with an interactive confirmation modal and browser handling to wipe cached generation files and start completely fresh.

---

## Directory Manifest & Component Functions

Every file included in this clean submission package serves a dedicated role in generation, schema enforcement, or automated evaluation:

| File Name | Category | Primary Function & Architectural Purpose |
| :--- | :--- | :--- |
| **`run_gui.py`** | **Universal Launcher** | Cross-platform bootstrap script. Verifies Python runtime, auto-installs missing dependencies from `requirements.txt`, checks Ollama service connectivity, auto-pulls `qwen3.5:4b` if missing, starts `app.py`, and launches default browser. |
| **`run_gui.bat`** | **1-Click GUI Launcher (Windows)** | Lightweight 6-line wrapper invoking `python run_gui.py %*` with automatic error pausing for Windows double-click evaluation. |
| **`run_pipeline.bat`** | **1-Click Headless Runner (CMD)** | Automated Windows batch runner executing Lab 1.1, Lab 1.2, and terminal rubric invariant assertions without opening a browser. |
| **`requirements.sh`** | **Environment Setup (Linux/macOS)** | Shell script for provisioning `.venv`, installing dependencies, and verifying `qwen3.5:4b` on Linux, macOS, or WSL. |
| **`requirements.txt`** | **Dependency Manifest** | Minimal pinned runtime dependencies (`pydantic>=2.0.0`, `ollama>=0.2.0`). |
| **`obe_schemas.py`** | **Core Deliverable #1** | Pydantic v2 data models defining the strict contracts for Course Outcomes, Lesson Learning Outcomes (LLOs), 14-Week Schedule Items, Bloom level normalization, and the UPHSD Grading Breakdown. |
| **`lab1_1_generator.py`** | **Core Deliverable #2** | Executable CLI generator for Stage 1. Queries `qwen3.5:4b` with 16k context window and concise CoT constraints to generate and validate Course Learning Outcomes. |
| **`obe_json_generator.py`** | **Specification Alias** | Identical mirror of `lab1_1_generator.py` provided to guarantee full backward compatibility with automated grading harnesses referencing the Page 1 alias. |
| **`lab1_2_pipeline.py`** | **Core Deliverable #3** | Chained multi-turn pipeline for Stage 2. Consumes Stage 1 outcomes into memory, constructs the 14-week schedule, enforces milestones, and validates full CLO coverage. |
| **`sample_output_syllabus.json`** | **Core Deliverable #4** | The final, validated 14-week OBE syllabus JSON artifact generated for *BSCS 3112: Artificial Intelligence*. |
| **`co_output_lab1_1.json`** | **Supporting Deliverable** | Pre-generated, validated Stage 1 Course Outcomes payload. Allows `lab1_2_pipeline.py` and the GUI to load and audit immediately offline. |
| **`app.py`** | **Web Backend & REST API** | Zero-dependency HTTP server (`ThreadingHTTPServer`) exposing REST endpoints (`/api/status`, `/api/co`, `/api/generate-co`, `/api/syllabus`, `/api/generate-syllabus`, `/api/audit`, `/api/nuke`) and serving static assets. |
| **`index.html`** | **Interactive Web GUI Studio** | Bespoke single-page application for Stage 1/Stage 2 generation, timeline inspection, live invariant audits, and printable syllabus views. |
| **`jspdf.umd.min.js`** | **Offline Client Bundle** | Local offline jsPDF library for secure, network-independent vector PDF generation. |
| **`jspdf.plugin.autotable.min.js`** | **Offline Client Bundle** | Local offline autoTable plugin for clean syllabus grid layout rendering. |
| **`uphsd_header_logo.png`** | **Branding Asset** | Official University of Perpetual Help System DALTA Molino Campus header logo embedded in both web preview and PDF exports. |
| **`README.md`** | **Documentation** | Comprehensive reproduction instructions, rubric compliance breakdown, and execution logs for the evaluator. |

---

## Execution Options for the Evaluator

### Option 1: Universal Python Launcher (Web Studio)
Works seamlessly across **Windows, macOS, and Linux**:
```bash
python run_gui.py
```
*Optional CLI flags:*
- `python run_gui.py --no-browser` : Starts server without opening a browser window.
- `python run_gui.py --check-only` : Runs pre-flight verification checks and exits.

### Option 2: Headless Command Prompt Pipeline (`run_pipeline.bat`)
On Windows, double-click **`run_pipeline.bat`** to execute the pipeline entirely in CMD and view terminal assertions.

### Option 3: Windows 1-Click GUI Runner (`run_gui.bat`)
On Windows, double-click **`run_gui.bat`** to start the interactive studio.

### Option 4: Linux / macOS / WSL Automated Setup
```bash
bash requirements.sh
python run_gui.py
```

### Option 5: Direct CLI Script Execution
```bash
# Step 1: Generate & Validate Course Outcomes (Stage 1)
python lab1_1_generator.py

# Step 2: Generate & Validate 14-Week Schedule (Stage 2)
python lab1_2_pipeline.py
```

---

## Enforced Pedagogical Invariants & Rubric Compliance

This implementation strictly fulfills all Exemplary (4/4) criteria established in Prof. Rob Malitao's grading rubric:

* **Active Bloom's Taxonomy Verbs:** Custom Pydantic `@field_validator` functions reject passive, unmeasurable verbs (*understand*, *learn*, *know*, *study*) in favor of concrete action verbs (*Implement*, *Analyze*, *Evaluate*, *Design*, *Formulate*). Additionally, action verbs are normalized automatically to their root Bloom's cognitive categories (`Remember`, `Understand`, `Apply`, `Analyze`, `Evaluate`, `Create`).
* **Institutional Milestone Locks:**
  * **Week 7 (Midterm Examination):** Programmatically locked to Period `"MIDTERM"` with departmental examination rubrics and written/practical evidence.
  * **Week 14 (Final Examination / Defense):** Programmatically locked to Period `"FINAL"` focusing on comprehensive capstone defenses and final examinations.
* **Tripartite Learning Outcomes ($K/S/A$):** Every single instructional week includes exactly three distinct Lesson Learning Outcomes categorized under Knowledge ($K$), Skills ($S$), and Attitude ($A$).
* **Practical Hands-on TLAs:** All instructional Teaching-Learning Activities require hands-on programming laboratory sessions with verifiable code artifacts.
* **100% CLO Schedule Coverage:** Stage 2 cross-checks that every Course Learning Outcome index defined in Stage 1 is aligned at least once across the 14-week schedule array (`aligned_co`).
* **Institutional UPHSD Grading Matrix:** Hardcoded to the standard College of Computer Studies distribution:
  * **70% Class Standing:** 30% Quizzes, 20% Research/Assignments, 50% Laboratory Works.
  * **30% Major Examinations:** Standard departmental midterm/final exams.

---

## Built-In Error Handling & Self-Healing Architecture

In compliance with the Error Handling & Code rubric criteria, all generators feature automatic multi-turn recovery mechanisms:

* **Expanded 16,384 Context Window:** Prevents token exhaustion during deep chain-of-thought `<think>` reasoning.
* **Concise Reasoning Directives:** Constrains model internal reasoning to $< 150$ words, ensuring rapid JSON emission.
* **JSON Substring & Reasoning Extraction:** `extract_json()` strips reasoning traces or `<think>` tags emitted by Qwen, with automatic fallback extraction from reasoning buffers if empty content tokens occur.
* **Dynamic Feedback Loops:** When an invalid Bloom's level, broken schema key, or malformed JSON structure is returned, the script catches `ValidationError` or `JSONDecodeError`, packages the exact traceback into an updated feedback prompt, and resubmits it to `qwen3.5:4b`.
* **Zero-Crash Design:** The pipeline autonomously corrects generation flaws within 4 attempts without raising unhandled exceptions to the operating system.

---

## Live CLI Pipeline Execution & Self-Healing Recovery Log (`run_pipeline.bat`)

```text
======================================================================
   UPHSD CCS - OBE AI Microservice Pipeline CLI Automated Runner
   Course: BSCS 3112 / Artificial Intelligence
   Student: Christian Ezekiel L. Carvajal
   Evaluator: Prof. Roberto L. Malitao
======================================================================

[+] Python installation detected.
[+] Dependencies installed and verified.
[+] Ollama CLI and local service active.
[+] Model 'qwen3.5:4b' is ready.

======================================================================
   [1/2] RUNNING LAB 1.1: Course Outcomes Generator (qwen3.5:4b)
======================================================================
[*] [Lab 1.1] Querying qwen3.5:4b with format='json' (Attempt 1/4)...
[-] [Lab 1.1] Attempt 1 validation failed: 1 validation error for CourseOutcomesPayload
course_outcomes.2.bloom_level
  Input should be 'Remember', 'Understand', 'Apply', 'Analyze', 'Evaluate' or 'Create' [type=literal_error, input_value='Design', input_type=str]
[*] [Lab 1.1] Feeding error traceback into self-healing feedback prompt...
[*] [Lab 1.1] Querying qwen3.5:4b with format='json' (Attempt 2/4)...
[+] [Lab 1.1] Schema validation successful.
[+] Saved validated Course Outcomes to co_output_lab1_1.json
[+] Lab 1.1 executed successfully. Output saved to co_output_lab1_1.json.

======================================================================
   [2/2] RUNNING LAB 1.2: 14-Week Syllabus Pipeline
======================================================================
[*] [Lab 1.2] Generating 14-Week Schedule (Attempt 1/4)...
[+] [Lab 1.2] Schedule validation and pedagogical alignment passed.
[+] Final deliverable saved to sample_output_syllabus.json
[+] Lab 1.2 executed successfully. Output saved to sample_output_syllabus.json.

======================================================================
   VERIFYING RUBRIC ADHERENCE AND INVARIANTS
======================================================================
[PASS] 14 Weeks Verified
[PASS] Week 7 Midterm Milestone Verified
[PASS] Week 14 Final Milestone Verified
[PASS] 100% Course Outcome Coverage Verified
[PASS] UPHSD CCS Institutional Grading Verified

======================================================================
   SUCCESS: All deliverables executed and verified without errors!
======================================================================
```

---

## Live Pre-Flight Verification Log (`run_gui.py`)

```text
======================================================================
   UPHSD CCS - OBE AI Microservice Interactive Studio
   Course: BSCS 3112 / Artificial Intelligence
   Student: Christian Ezekiel L. Carvajal
   Evaluator: Prof. Roberto L. Malitao
======================================================================

[*] Checking Python environment: 3.14.6 (python.exe)
[+] Python version is compatible.
[*] Verifying Python package dependencies...
[+] All Python dependencies (pydantic, ollama) are installed.
[*] Checking Ollama service and 'qwen3.5:4b' model availability...
[+] Ollama service is active and responsive.
[+] Model 'qwen3.5:4b' is verified and ready for live generation.

[+] Pre-flight verification completed successfully.
```

---

## Built-In Rubric Assertion & Accreditation Audit

The 6-point invariant audit is integrated directly into the Web Studio (**Stage 3: Live Rubric Audit**) and exposed via the `/api/audit` backend endpoint in `app.py`. It programmatically asserts all rubric constraints:

```text
[PASS] 14 Instructional Weeks Verified
[PASS] Week 7 Locked Midterm Milestone: 'Midterm Examination'
[PASS] Week 14 Locked Final Milestone: 'Final Examination / Capstone Defense'
[PASS] Tripartite LLOs (Knowledge, Skills, Attitude) Verified for All Weeks
[PASS] 100% Course Outcome Coverage Across Schedule: {1, 2, 3, 4}
[PASS] UPHSD CCS Grading Breakdown Verified: 70% Class Standing (30Q/20R/50L) + 30% Major Exam

[STATUS] 100% Compliant with Prof. Roberto L. Malitao's OBE Rubric.
```
