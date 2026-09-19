# SYSTEM_ARCHITECTURE.md — OBE Microservice Architecture

## 1. Architectural Blueprint

The OBE Academic System Pipeline is a layered microservice architecture designed to transform unstructured curriculum parameters into strictly validated, accreditation-ready Outcome-Based Education (OBE) course syllabi.

```text
+-------------------------------------------------------------------------+
|                        Client & CLI Entry Point                         |
|      (lab1_1_generator.py / obe_json_generator.py / lab1_2_pipeline.py) |
+-------------------------------------------------------------------------+
                                    │
                                    ▼
+-------------------------------------------------------------------------+
|                       Prompt Engineering Layer                          |
|         - System Prompts with Banned-Verb Constraints                   |
|         - Role Authority (UPHSD CCS Curriculum Designer)                |
|         - Target JSON Schema Specifications                             |
+-------------------------------------------------------------------------+
                                    │
                                    ▼
+-------------------------------------------------------------------------+
|                     Local LLM Inference (Ollama)                        |
|         - Model: qwen3.5:4b                                             |
|         - Parameter: format="json" (grammar token constraint)           |
|         - Context Window: 4096 (Stage 1) / 8192 (Stage 2)               |
|         - Temperature: 0.2 (deterministic sampling)                     |
+-------------------------------------------------------------------------+
                                    │
                                    ▼
+-------------------------------------------------------------------------+
|                      Parsing & Guardrail Layer                          |
|         - CoT (<think>...</think>) Reasoning Extraction                 |
|         - JSON Substring Boundary Locating                              |
|         - Pydantic v2 Type & Field Validation (obe_schemas.py)          |
+-------------------------------------------------------------------------+
          │                                              │
      [Success]                                      [Failure]
          │                                              ▼
          │                               +-------------------------------+
          │                               |   Automated Re-prompt Loop    |
          │                               |  - Inject ValidationError     |
          │                               |  - Re-query (Max 4 attempts)  |
          │                               +-------------------------------+
          ▼
+-------------------------------------------------------------------------+
|                         Persistence & Export                            |
|         - Stage 1: outputs/co_output_lab1_1.json                        |
|         - Stage 2: outputs/sample_output_syllabus.json                  |
|         - Downstream Ready: database/obe_syllabus.db & templates/       |
+-------------------------------------------------------------------------+
```

---

## 2. Pydantic v2 Data Contract Topology

### Core Schemas & Inheritance Hierarchy

1. **`CourseOutcome`**
   - `clo_number: int` (Range: 1 to 5)
   - `bloom_level: Literal["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]`
   - `co_description: str` (Guarded by `@field_validator("co_description")`)
   - `mapped_po: List[int]` (Min items: 1)

2. **`CourseOutcomesPayload`**
   - `course_title: str`
   - `course_code: str`
   - `course_description: str`
   - `course_outcomes: List[CourseOutcome]` (Length: 4 to 5)

3. **`LessonLearningOutcome`**
   - `category: Literal["K", "S", "A"]`
   - `outcome_text: str`

4. **`WeeklyScheduleItem`**
   - `week_number: int` (Range: 1 to 14)
   - `period: Literal["PRELIM", "MIDTERM", "FINAL"]`
   - `topic: str`
   - `llos: List[LessonLearningOutcome]` (Exact length: 3, covering K, S, A)
   - `teaching_learning_activity: str`
   - `assessment_tool: str`
   - `evidence: str`
   - `aligned_co: List[int]` (Min items: 1)

5. **`GradingBreakdown`**
   - `quizzes_pct: float = 30.0`
   - `research_pct: float = 20.0`
   - `seatwork_lab_pct: float = 50.0`
   - `class_standing_weight: float = 70.0`
   - `major_exam_weight: float = 30.0`

6. **`FullSyllabusPayload`**
   - Aggregation of metadata, `course_outcomes`, `weekly_schedule` (14 items), and `grading_breakdown`.

---

## 3. Resilience & Self-Healing Loop Details
When `ollama.chat(format="json")` returns content:
1. `raw_text` is extracted and stripped.
2. Any `<think>...</think>` block is separated out to prevent token pollution.
3. The leftmost `{` and rightmost `}` are detected to isolate the JSON object.
4. If `json.loads()` fails, the raw exception is wrapped into a descriptive retry prompt.
5. If `Pydantic` raises `ValidationError` (e.g. non-measurable verb, missing field, out-of-range week), the exact message is returned to Qwen in the next turn as a user message.
6. The loop runs up to 4 attempts before escalating, ensuring deterministic completion.

---

## 4. Lesson 5 Midterm Mini-Project Architectural Extension
* **Lead Architect:** Christian Ezekiel L. Carvajal
* **Collaborative Partner:** John Miko P. Sarsalijo
* **Evaluator:** Prof. Roberto L. Malitao

### Multi-Tiered Component Topology
```text
[Layer 0: Data Contracts]       obe_schemas.py (Pydantic v2: CourseMetadata, CLO, LLO, WeeklySchedule, FullSyllabus)
                                      │
[Layer 1: LLM Engine]           llm_engine.py (Ollama API /api/generate, format="json", max 3 self-healing retries)
                                      │
[Layer 2: Deliverable Output]   sample_validated_output.json (18-week schema-compliant JSON)
                                      │
[Layer 3: Relational Storage]   schema.sql & db_manager.py (Normalized SQLite3 tables: courses, clos, weeks, llos)
                                      │
[Layer 4: Document Compiler]    export_engine.py & templates/uphsd_ccs_template.html (Jinja2 HTML syllabus export)
                                      │
[Layer 5: Microservice Web]     app.py & index.html (REST API dispatching user requests)
```

### Relational Schema Design (`obe_syllabus.db`)
* **`courses`**: Primary metadata entity with unique constraint on `course_code`.
* **`course_outcomes`**: Child records linked via `course_id` with cascading delete; stores Bloom level and mapped PLOs.
* **`weekly_schedules`**: 18-week syllabus rows linked via `course_id` with cascading delete; stores topics, TLAs, assessment tasks, resources.
* **`lesson_outcomes`**: Granular LLO statements linked via `schedule_id` with cascading delete; strictly categorized into `K`, `S`, or `A` domain.

