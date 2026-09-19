# AGENTS.md — UPHSD CCS OBE Academic System Pipeline

## 1. Project Overview & Multi-Agent Architecture
This project implements the automated College of Computer Studies (CCS) Outcome-Based Education (OBE) AI Microservice Pipeline for the University of Perpetual Help System DALTA (UPHSD), authored under the guidelines of **Prof. Rob Malitao**.

The system orchestrates local LLM inference via **Ollama (`qwen3.5:4b`)**, enforcing strict Pydantic v2 data contracts, pedagogical validation guardrails, and automated multi-turn error correction.

---

## 2. Agent Roster & Role Definitions

### Agent 1: `CurriculumDesignAgent`
* **Role:** Expert IT/CS Curriculum Designer & Prompt Engineer
* **Responsibilities:**
  - Formulates contextual system prompts enforcing active Bloom's Taxonomy verbs (Identify, Configure, Implement, Design, etc.).
  - Banned verb mitigation: intercepts and eliminates passive phrasing (`understand`, `learn`, `know`, `study`).
  - Constructs multi-turn user prompts incorporating target Program Learning Outcomes (PLO 1–3) and subject prerequisites.
* **Target Artifacts:** System prompts for Lab 1.1 (`SYSTEM_PROMPT_LAB1_1`) and Lab 1.2 (`SYSTEM_PROMPT_LAB1_2`).

### Agent 2: `SchemaValidatorAgent`
* **Role:** Type Enforcement & Runtime Contract Guardrail
* **Responsibilities:**
  - Validates raw LLM outputs against strict Pydantic v2 schemas (`CourseOutcomesPayload`, `WeeklyScheduleItem`, `FullSyllabusPayload`).
  - Handles Ollama `format="json"` constraint monitoring and `<think>` reasoning extraction.
  - Generates detailed, diagnostic feedback upon `ValidationError` or `JSONDecodeError` for the model re-prompt loop.
* **Target Artifacts:** `obe_schemas.py`, validator routines.

### Agent 3: `PipelineOrchestrationAgent`
* **Role:** Chained Workflow & Data Pipeline Controller
* **Responsibilities:**
  - Manages sequential execution across Lab 1.1 (Course Learning Outcomes) and Lab 1.2 (14-Week Schedule Generation).
  - Maintains state persistence across generation stages (`outputs/co_output_lab1_1.json` -> `outputs/sample_output_syllabus.json`).
  - Handles retry budget allocation (maximum 4 retries per stage) with temperature regulation.
* **Target Artifacts:** `lab1_1_generator.py`, `obe_json_generator.py`, `lab1_2_pipeline.py`.

### Agent 4: `QAAuditAgent`
* **Role:** Academic Accreditation & Rubric Compliance Auditor
* **Responsibilities:**
  - Verifies 100% adherence to Prof. Rob Malitao's OBE Assessment Rubric.
  - Asserts structural business rules: exactly 14 weeks, Week 7 locked to Midterm, Week 14 locked to Final, 100% CLO coverage, tripartite K/S/A LLOs.
  - Validates institutional grading formula: Class Standing 70% (Quizzes 30%, Research 20%, Lab 50%) + Major Exam 30%.
* **Target Artifacts:** Automated test scripts, audit logs, `outputs/sample_output_syllabus.json`.

---

## 3. Tool Permissions & Operational Boundaries

| Agent | Allowed Tools / Commands | Restricted Actions |
|---|---|---|
| `CurriculumDesignAgent` | Prompt design, LLM chat invocation | Cannot alter Pydantic models directly |
| `SchemaValidatorAgent` | Pydantic schema declaration, field validators | Cannot bypass banned verb checks |
| `PipelineOrchestrationAgent` | CLI execution, JSON file I/O, retry loop | Cannot accept unvalidated JSON payloads |
| `QAAuditAgent` | Assertion test suite, schema verification | Cannot modify syllabus content arbitrarily |

---

## 4. Error Handling & Recovery Protocols

```text
[Ollama /api/chat (format="json")]
               │
               ▼
   [Reasoning / CoT Stripper]
  (Extract pure JSON substring)
               │
               ▼
   [Pydantic v2 Schema Validation]
         │               │
      (Success)       (Failure)
         │               ▼
         │       [Construct Feedback Message]
         │       (Include exact ValidationError trace)
         │               ▼
         │       [Append to Message History]
         │               ▼
         │       [Re-prompt Ollama (Max 4 Attempts)]
         ▼
[Relational / Template Export Ready]
```

---

## 5. Development Conventions
* **Environment:** Isolated virtual environment (`.venv`).
* **Model:** Local `qwen3.5:4b` running via Ollama daemon (`http://localhost:11434`).
* **Python Target:** Python 3.10+ (tested on Python 3.14).
* **Naming Standards:** camelCase for configuration files and JSON keys, snake_case for Python scripts.
