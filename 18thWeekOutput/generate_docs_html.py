import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>UPHSD CCS — 18-Week OBE Syllabus Microservice Documentation</title>
  <style>
    @page {
      size: A4;
      margin: 18mm 16mm 18mm 16mm;
    }
    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 10.5pt;
      line-height: 1.5;
      color: #1e293b;
      background: #ffffff;
      padding: 20px;
    }
    @media print {
      body { padding: 0; background: transparent; }
      .page-break { page-break-before: always; }
      .no-break { break-inside: avoid; page-break-inside: avoid; }
      pre { white-space: pre-wrap !important; word-break: break-all; }
    }
    .header-table {
      width: 100%;
      border-bottom: 2px solid #8f1719;
      padding-bottom: 12px;
      margin-bottom: 20px;
    }
    .header-title {
      font-size: 16pt;
      font-weight: 800;
      color: #8f1719;
      text-transform: uppercase;
      letter-spacing: -0.02em;
    }
    .header-subtitle {
      font-size: 10.5pt;
      color: #475569;
      font-weight: 600;
      margin-top: 2px;
    }
    .metadata-bar {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 10px 14px;
      margin-bottom: 24px;
      font-size: 9pt;
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 6px;
    }
    .metadata-bar div { display: flex; gap: 6px; }
    .metadata-bar strong { color: #0f172a; min-width: 120px; }
    
    h2 {
      font-size: 13pt;
      font-weight: 700;
      color: #8f1719;
      border-bottom: 1.5px solid #cbd5e1;
      padding-bottom: 4px;
      margin-top: 24px;
      margin-bottom: 12px;
    }
    h3 {
      font-size: 11pt;
      font-weight: 700;
      color: #0f172a;
      margin-top: 16px;
      margin-bottom: 6px;
    }
    p {
      margin-bottom: 8px;
      color: #334155;
    }
    .figure-card {
      background: #ffffff;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      padding: 12px;
      margin: 14px 0 20px 0;
      page-break-inside: avoid;
    }
    .figure-card img {
      width: 100%;
      height: auto;
      border-radius: 4px;
      border: 1px solid #e2e8f0;
      display: block;
    }
    .figure-caption {
      margin-top: 8px;
      font-size: 9.5pt;
      color: #1e293b;
    }
    .figure-caption strong {
      color: #8f1719;
    }
    .code-container {
      background: #0f172a;
      color: #f8fafc;
      border-radius: 6px;
      padding: 12px;
      font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
      font-size: 8.5pt;
      line-height: 1.45;
      overflow-x: auto;
      margin: 10px 0 16px 0;
      border: 1px solid #334155;
      page-break-inside: avoid;
    }
    .code-container pre {
      margin: 0;
    }
    .badge {
      display: inline-block;
      font-size: 7.5pt;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 4px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }
    .badge-primary { background: #fee2e2; color: #991b1b; }
    .badge-success { background: #dcfce7; color: #166534; }
    .badge-gold { background: #fef3c7; color: #92400e; }
    
    table.data-table {
      width: 100%;
      border-collapse: collapse;
      margin: 12px 0 18px 0;
      font-size: 8.5pt;
      page-break-inside: avoid;
    }
    table.data-table th, table.data-table td {
      border: 1px solid #cbd5e1;
      padding: 6px 10px;
      text-align: left;
    }
    table.data-table th {
      background: #f1f5f9;
      color: #0f172a;
      font-weight: 700;
    }
  </style>
</head>
<body>

  <!-- Header -->
  <table class="header-table">
    <tr>
      <td>
        <div class="header-title">University of Perpetual Help System DALTA</div>
        <div class="header-subtitle">College of Computer Studies • Molino Campus • BSCS Curriculum Automation</div>
      </td>
      <td style="text-align: right; vertical-align: bottom;">
        <span class="badge badge-primary">Technical Documentation</span>
      </td>
    </tr>
  </table>

  <!-- Metadata -->
  <div class="metadata-bar">
    <div><strong>Project Title:</strong> 18-Week OBE Syllabus Microservice Interactive Studio</div>
    <div><strong>Course & Term:</strong> BSCS 3112 / Artificial Intelligence (Lesson 5)</div>
    <div><strong>Evaluator:</strong> Prof. Roberto L. Malitao</div>
    <div><strong>Port Architecture:</strong> http://127.0.0.1:8001 (ThreadingHTTPServer)</div>
    <div><strong>Lead Architect:</strong> Christian Ezekiel L. Carvajal</div>
    <div><strong>Collaborating Partner:</strong> John Miko P. Sarsalijo</div>
    <div><strong>Model Engine:</strong> Ollama qwen3.5:4b (Local Inference)</div>
    <div><strong>Storage & Compilation:</strong> SQLite 3 (PRAGMA foreign_keys = ON) + Jinja2</div>
  </div>

  <h2>1. Executive Summary & Architecture Overview</h2>
  <p>
    This project implements an autonomous Outcomes-Based Education (OBE) course syllabus microservice adhering to CHED CMO No. 25, Series of 2015 and the institutional standards of the College of Computer Studies at UPHSD Molino Campus.
    The system utilizes an offline local Large Language Model (<strong>qwen3.5:4b</strong>), runtime data validation via <strong>Pydantic v2</strong>, a normalized relational database in <strong>SQLite</strong> with cascading deletes, and an institutional document compiler powered by <strong>Jinja2</strong>.
  </p>

  <!-- Process Flow Table -->
  <table class="data-table">
    <thead>
      <tr>
        <th>Phase / Pipeline Component</th>
        <th>Input Artifact</th>
        <th>Processing Engine</th>
        <th>Output Deliverable & Verification</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>1. Curriculum Ingestion</strong></td>
        <td>Catalog Metadata (8 BSCS Courses)</td>
        <td><code>curriculum_catalog.py</code></td>
        <td>Auto-filled Course Specifications (Code, Title, Prereqs, Units)</td>
      </tr>
      <tr>
        <td><strong>2. AI Generation & CoT Stripping</strong></td>
        <td>System Prompt + Academic Constraints</td>
        <td><code>llm_engine.py</code> (Ollama qwen3.5:4b)</td>
        <td>Pure JSON substring extracted from raw <code>&lt;think&gt;...&lt;/think&gt;</code> tokens</td>
      </tr>
      <tr>
        <td><strong>3. Runtime Schema Validation</strong></td>
        <td>Extracted JSON Payload</td>
        <td><code>obe_schemas.py</code> (Pydantic v2)</td>
        <td>Rejects passive verbs, validates tripartite K/S/A, enforces 18 weeks</td>
      </tr>
      <tr>
        <td><strong>4. Relational Persistence & CRUD</strong></td>
        <td>Validated <code>FullSyllabusSchema</code></td>
        <td><code>db_manager.py</code> (SQLite 3)</td>
        <td>Atomic inserts into <code>courses</code>, <code>course_outcomes</code>, <code>weekly_schedules</code>, <code>lesson_outcomes</code></td>
      </tr>
      <tr>
        <td><strong>5. Institutional Document Export</strong></td>
        <td>Relational SQLite Records</td>
        <td><code>export_engine.py</code> (Jinja2)</td>
        <td>Browser-ready <code>official_syllabus_*.html</code> with vector print layout</td>
      </tr>
    </tbody>
  </table>

  <div class="page-break"></div>

  <h2>2. Interactive Web Studio Component Walkthrough</h2>
  <p>
    The following section documents each component and modal dialog of the web interface operating on <code>http://127.0.0.1:8001</code>. All screenshots were captured at full 1080p desktop resolution.
  </p>

  <!-- Figure 1 -->
  <div class="figure-card">
    <img src="documentation_assets/01_curriculum_studio_overview.png" alt="Curriculum Studio Overview">
    <div class="figure-caption">
      <strong>Figure 1: 18-Week Curriculum Studio Overview & Course Catalog</strong><br>
      The primary dashboard showing the 8-subject curriculum catalog in the left sidebar, top institutional banner with system health pills (<code>Ollama Online</code>, <code>8 Ready</code>), and active course display for <code>BSCS 3112: Artificial Intelligence</code> with 4 formulated Course Learning Outcomes categorized under Bloom's Revised Taxonomy.
    </div>
  </div>

  <!-- Figure 2 -->
  <div class="figure-card">
    <img src="documentation_assets/02_course_parameters_drawer.png" alt="Course Parameters Drawer">
    <div class="figure-caption">
      <strong>Figure 2: Course Specification & Parameters Configuration Drawer</strong><br>
      Faculty configuration drawer displaying pre-loaded institutional catalog parameters: Catalogue Description, Credit Units (Lecture/Lab hours), Course Prerequisites, and Target Program Learning Outcomes (PLOs). Allows zero-typing auto-fill or custom faculty modification before triggering generation.
    </div>
  </div>

  <div class="page-break"></div>

  <!-- Figure 3 -->
  <div class="figure-card">
    <img src="documentation_assets/03_human_in_the_loop_clo_editor.png" alt="Human-in-the-Loop CLO Editor">
    <div class="figure-caption">
      <strong>Figure 3: Faculty Human-in-the-Loop Course Learning Outcome (CLO) Editor</strong><br>
      Interactive outcome editor modal implementing Milestone 2 requirement. Features Quick Active Verb chips (<code>+ Analyze</code>, <code>+ Implement</code>, <code>+ Design</code>). Enforces active Bloom's verbs before saving directly to SQLite, rejecting passive verbs such as <em>understand</em>, <em>know</em>, or <em>learn</em>.
    </div>
  </div>

  <!-- Figure 4 -->
  <div class="figure-card">
    <img src="documentation_assets/04_plo_alignment_matrix.png" alt="PLO Alignment Matrix">
    <div class="figure-caption">
      <strong>Figure 4: CHED CMO 25 s.2015 Program Learning Outcomes (PLO) Alignment Matrix</strong><br>
      Cross-validation matrix demonstrating how Course Outcomes systematically scaffold the 5 Core Computer Science Graduate Attributes. Follows CHED curriculum scaffolding principles where specialized courses target distinct graduate outcomes to prevent outcome inflation.
    </div>
  </div>

  <div class="page-break"></div>

  <!-- Figure 5 -->
  <div class="figure-card">
    <img src="documentation_assets/05_18_week_schedule_matrix.png" alt="18-Week Schedule Matrix">
    <div class="figure-caption">
      <strong>Figure 5: 18-Week Semester Curriculum Roadmap & Tripartite K/S/A Tracking</strong><br>
      Chronological 18-week academic matrix displaying hard-locked departmental milestones: Week 9 Midterm Examination Lock and Week 18 Final Examination / Capstone Defense Lock. Displays real-time tripartite K/S/A domain tracking (100% Cognitive, Psychomotor, and Affective coverage).
    </div>
  </div>

  <!-- Figure 6 -->
  <div class="figure-card">
    <img src="documentation_assets/06_batch_generation_modal.png" alt="Batch Generation Modal">
    <div class="figure-caption">
      <strong>Figure 6: Intelligent Batch Generation Dispatcher & Selective Synthesis Window</strong><br>
      Intelligent modal window triggered when initiating batch generation. Inspects database and filesystem records, displays status pill badges (<code>✓ All 8 Courses Complete</code>, <code>📚 100% Persisted in SQLite</code>), renders a course chip grid, and confirms whether to freshly re-synthesize or process remaining pending courses.
    </div>
  </div>

  <div class="page-break"></div>

  <!-- Figure 7 -->
  <div class="figure-card">
    <img src="documentation_assets/07_dedicated_syllabus_viewer.png" alt="Dedicated Syllabus Viewer">
    <div class="figure-caption">
      <strong>Figure 7: Dedicated Syllabus Viewer & Publication Print Studio (View 2)</strong><br>
      Master-detail document viewer rendering the official institutional Jinja2 layout for all 8 catalog courses. Features sticky document controls: zoom scaling, paper mode toggle, vector PDF printing (<code>window.print()</code>), and standalone tab viewing.
    </div>
  </div>

  <!-- Figure 8 -->
  <div class="figure-card">
    <img src="documentation_assets/08_sqlite_relational_database_inspector.png" alt="SQLite Relational Database Inspector">
    <div class="figure-caption">
      <strong>Figure 8: SQLite Relational Database & Multi-Table Live Inspector (View 3)</strong><br>
      Direct database administrative view showing live table counts (8 Courses, 32 CLOs, 144 Weeks, 432 LLOs). Allows multi-table inspection, relational data review, direct navigation to rendered syllabi, and selective course resets.
    </div>
  </div>

  <div class="page-break"></div>

  <!-- Figure 9 -->
  <div class="figure-card">
    <img src="documentation_assets/09_accreditation_rubric_audit.png" alt="Accreditation Rubric Audit">
    <div class="figure-caption">
      <strong>Figure 9: Automated CHED CMO 25 Invariant Auditor & Compliance Scorecard</strong><br>
      Programmatic verification engine testing 7 strict academic invariants: 18-week length, Week 9/18 exam locks, tripartite K/S/A coverage, active Bloom action verbs, PLO mapping, and the UPHSD CCS institutional grading formula (70% Class Standing + 30% Major Exam). Score: 100% Compliant.
    </div>
  </div>

  <!-- Figure 10 -->
  <div class="figure-card">
    <img src="documentation_assets/10_command_palette.png" alt="Universal Command Palette">
    <div class="figure-caption">
      <strong>Figure 10: Universal Command Palette (Ctrl + K)</strong><br>
      Quick-navigation overlay accessible via <code>Ctrl + K</code>. Enables instant fuzzy search across course codes, titles, descriptions, and categories, alongside one-click action execution (batch generation, theme switching, selective wiping).
    </div>
  </div>

  <div class="page-break"></div>

  <h2>3. Backend Engineering & Data Contracts</h2>
  <p>
    This section details the underlying database architecture, schema enforcement, and Python backend microservice components.
  </p>

  <h3>3.1 Normalized SQLite Relational DDL (<code>database/schema.sql</code>)</h3>
  <p>
    Enforces relational integrity across 4 tables with foreign keys and cascading deletes:
  </p>
  <div class="code-container">
<pre>-- Enable Foreign Key constraints
PRAGMA foreign_keys = ON;

-- 1. Courses Table (Parent Entity)
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_code TEXT NOT NULL UNIQUE,
    course_title TEXT NOT NULL,
    course_description TEXT NOT NULL,
    credit_units INTEGER NOT NULL DEFAULT 3,
    lecture_hours INTEGER NOT NULL DEFAULT 2,
    lab_hours INTEGER NOT NULL DEFAULT 3,
    prerequisites TEXT NOT NULL DEFAULT 'None',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Course Outcomes Table (1-to-Many from courses)
CREATE TABLE IF NOT EXISTS course_outcomes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    clo_id TEXT NOT NULL,
    description TEXT NOT NULL,
    bloom_level TEXT NOT NULL,
    program_outcomes_mapped TEXT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);

-- 3. Weekly Schedules Table (1-to-Many from courses)
CREATE TABLE IF NOT EXISTS weekly_schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    week_number INTEGER NOT NULL,
    topics TEXT NOT NULL,
    teaching_learning_activities TEXT NOT NULL,
    assessment_tasks TEXT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);

-- 4. Lesson Outcomes Table (1-to-Many from weekly_schedules)
CREATE TABLE IF NOT EXISTS lesson_outcomes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    schedule_id INTEGER NOT NULL,
    llo_id TEXT NOT NULL,
    domain TEXT NOT NULL CHECK(domain IN ('K', 'S', 'A')),
    description TEXT NOT NULL,
    FOREIGN KEY (schedule_id) REFERENCES weekly_schedules(id) ON DELETE CASCADE
);</pre>
  </div>

  <div class="page-break"></div>

  <h3>3.2 Pydantic v2 Data Contracts & Bloom Verb Enforcement (<code>obe_schemas.py</code>)</h3>
  <p>
    Runtime validation rejects unmeasurable verbs and enforces strict tripartite domain constraints:
  </p>
  <div class="code-container">
<pre>class CourseOutcomeSchema(BaseModel):
    clo_id: str
    description: str
    bloom_level: str
    program_outcomes_mapped: List[str]

    @field_validator("description")
    @classmethod
    def validate_action_verbs(cls, v: str) -> str:
        banned_verbs = [
            "understand", "know", "learn", "study", 
            "familiarize", "be exposed to", "appreciate"
        ]
        first_word = v.strip().split()[0].lower() if v.strip() else ""
        for banned in banned_verbs:
            if banned in first_word:
                raise ValueError(
                    f"Banned non-measurable verb '{banned}' detected in outcome statement. "
                    "Use active Bloom verbs (e.g., Analyze, Implement, Evaluate, Formulate)."
                )
        return v

class LessonOutcomeSchema(BaseModel):
    llo_id: str
    domain: Literal["K", "S", "A"]  # K: Knowledge, S: Skills, A: Attitude
    description: str

class WeeklyScheduleSchema(BaseModel):
    week_number: int
    topics: List[str]
    lesson_outcomes: List[LessonOutcomeSchema]
    teaching_learning_activities: List[str]
    assessment_tasks: List[str]</pre>
  </div>

  <h3>3.3 LLM Client & Self-Healing Retry Loop (<code>llm_engine.py</code>)</h3>
  <p>
    Calls Ollama on <code>http://127.0.0.1:11434/api/generate</code> with Chain-of-Thought reasoning stripping and iterative error correction:
  </p>
  <div class="code-container">
<pre>def clean_llm_json(raw_text: str) -> str:
    '''Strips Chain-of-Thought (&lt;think&gt;...&lt;/think&gt;) and isolates valid JSON boundaries.'''
    cleaned = re.sub(r"&lt;think&gt;.*?&lt;/think&gt;", "", raw_text, flags=re.DOTALL)
    start_brace = cleaned.find("{")
    end_brace = cleaned.rfind("}")
    if start_brace != -1 and end_brace != -1 and end_brace > start_brace:
        return cleaned[start_brace:end_brace + 1].strip()
    return cleaned.strip()

# Multi-turn self-healing loop
for attempt in range(1, max_retries + 1):
    try:
        raw_resp = query_ollama(prompt, model="qwen3.5:4b", format="json")
        json_str = clean_llm_json(raw_resp)
        validated_data = FullSyllabusSchema.model_validate_json(json_str)
        return validated_data
    except (ValidationError, json.JSONDecodeError) as err:
        prompt = (
            f"Your previous JSON output failed validation: {err}. "
            "Correct the output. Ensure description begins with an active Bloom verb and "
            "domain is strictly 'K', 'S', or 'A'."
        )</pre>
  </div>

  <div class="page-break"></div>

  <h3>3.3 Deliverable 3: Official Institutional Jinja2 Layout (<code>templates/uphsd_ccs_template.html</code>)</h3>
  <p>
    Institutional template rendering relational SQLite course records into a publication-grade syllabus layout with CHED CMO 25 alignments, cognitive taxonomy badges, tripartite domain indicators, and signatory blocks:
  </p>
  <div class="code-container">
<pre>&lt;!-- Institutional Header with UPHSD Molino Seal --&gt;
&lt;div class="inst-header"&gt;
  &lt;div style="display:flex; align-items:center; justify-content:center; gap:18px;"&gt;
    &lt;img src="../assets/logo/uphsd.png" alt="UPHSD Seal" style="height:70px;"&gt;
    &lt;div&gt;
      &lt;h1&gt;University of Perpetual Help System DALTA&lt;/h1&gt;
      &lt;h2&gt;Molino Campus &bull; Bacoor City, Cavite&lt;/h2&gt;
      &lt;h3&gt;College of Computer Studies&lt;/h3&gt;
    &lt;/div&gt;
  &lt;/div&gt;
  &lt;div class="doc-title"&gt;Course Syllabus: {{ course.course_code }}&lt;/div&gt;
&lt;/div&gt;

&lt;!-- Section I: Course Overview &amp; Specifications --&gt;
&lt;div class="section-title"&gt;I. Course Identification &amp; Specification&lt;/div&gt;
&lt;table class="meta-table"&gt;
  &lt;tr&gt;&lt;td&gt;Course Code&lt;/td&gt;&lt;td&gt;&lt;strong&gt;{{ course.course_code }}&lt;/strong&gt;&lt;/td&gt;&lt;/tr&gt;
  &lt;tr&gt;&lt;td&gt;Course Title&lt;/td&gt;&lt;td&gt;&lt;strong&gt;{{ course.course_title }}&lt;/strong&gt;&lt;/td&gt;&lt;/tr&gt;
  &lt;tr&gt;&lt;td&gt;Credit Units&lt;/td&gt;&lt;td&gt;{{ course.credit_units }}.0 Units ({{ course.lecture_hours }} Lec / {{ course.lab_hours }} Lab)&lt;/td&gt;&lt;/tr&gt;
  &lt;tr&gt;&lt;td&gt;Prerequisites&lt;/td&gt;&lt;td&gt;{{ course.prerequisites }}&lt;/td&gt;&lt;/tr&gt;
  &lt;tr&gt;&lt;td&gt;Course Description&lt;/td&gt;&lt;td&gt;{{ course.course_description }}&lt;/td&gt;&lt;/tr&gt;
&lt;/table&gt;

&lt;!-- Section II: Course Learning Outcomes (CLOs) --&gt;
&lt;div class="section-title"&gt;II. Course Learning Outcomes (CLOs)&lt;/div&gt;
&lt;table&gt;
  &lt;thead&gt;
    &lt;tr&gt;&lt;th&gt;CLO ID&lt;/th&gt;&lt;th&gt;Outcome Statement&lt;/th&gt;&lt;th&gt;Bloom's Taxonomy&lt;/th&gt;&lt;th&gt;PLOs Mapped&lt;/th&gt;&lt;/tr&gt;
  &lt;/thead&gt;
  &lt;tbody&gt;
    {% for clo in clos %}
    &lt;tr&gt;
      &lt;td&gt;&lt;strong&gt;{{ clo.clo_id }}&lt;/strong&gt;&lt;/td&gt;
      &lt;td&gt;{{ clo.description }}&lt;/td&gt;
      &lt;td&gt;&lt;span class="badge badge-bloom"&gt;{{ clo.bloom_level }}&lt;/span&gt;&lt;/td&gt;
      &lt;td&gt;{{ clo.program_outcomes_mapped | join(', ') }}&lt;/td&gt;
    &lt;/tr&gt;
    {% endfor %}
  &lt;/tbody&gt;
&lt;/table&gt;

&lt;!-- Section III: 18-Week Detailed Schedule with Tripartite Domains --&gt;
&lt;div class="section-title"&gt;III. 18-Week Detailed Teaching-Learning Schedule&lt;/div&gt;
&lt;table&gt;
  &lt;thead&gt;
    &lt;tr&gt;
      &lt;th&gt;Week&lt;/th&gt;&lt;th&gt;Topics / Subject Matter&lt;/th&gt;&lt;th&gt;Lesson Outcomes (K/S/A)&lt;/th&gt;
      &lt;th&gt;TLAs&lt;/th&gt;&lt;th&gt;Assessment Tasks&lt;/th&gt;
    &lt;/tr&gt;
  &lt;/thead&gt;
  &lt;tbody&gt;
    {% for w in schedule %}
    &lt;tr class="{% if w.week_number in [9, 18] %}exam-row{% endif %}"&gt;
      &lt;td&gt;&lt;strong&gt;Week {{ w.week_number }}&lt;/strong&gt;&lt;/td&gt;
      &lt;td&gt;{{ w.topics | join('; ') }}&lt;/td&gt;
      &lt;td&gt;
        {% for llo in w.lesson_outcomes %}
        &lt;div&gt;&lt;span class="badge badge-{{ llo.domain | lower }}"&gt;{{ llo.domain }}&lt;/span&gt; {{ llo.description }}&lt;/div&gt;
        {% endfor %}
      &lt;/td&gt;
      &lt;td&gt;{{ w.teaching_learning_activities | join('; ') }}&lt;/td&gt;
      &lt;td&gt;{{ w.assessment_tasks | join('; ') }}&lt;/td&gt;
    &lt;/tr&gt;
    {% endfor %}
  &lt;/tbody&gt;
&lt;/table&gt;

&lt;!-- Institutional Signatories --&gt;
&lt;div class="sign-grid"&gt;
  &lt;div class="sign-box"&gt;&lt;div class="sign-line"&gt;Faculty Member&lt;/div&gt;&lt;div class="sign-title"&gt;Prepared By&lt;/div&gt;&lt;/div&gt;
  &lt;div class="sign-box"&gt;&lt;div class="sign-line"&gt;Department Chair, CS&lt;/div&gt;&lt;div class="sign-title"&gt;Verified &amp; Recommended&lt;/div&gt;&lt;/div&gt;
  &lt;div class="sign-box"&gt;&lt;div class="sign-line"&gt;Dean, CCS&lt;/div&gt;&lt;div class="sign-title"&gt;Approved By&lt;/div&gt;&lt;/div&gt;
&lt;/div&gt;</pre>
  </div>

  <div class="page-break"></div>

  <h3>3.4 Deliverable 4: SQLite Query &amp; HTML/PDF Syllabus Compilation (<code>export_engine.py</code>)</h3>
  <p>
    Queries the SQLite relational database by <code>course_code</code> and renders an official, browser-ready HTML/PDF syllabus document using Jinja2:
  </p>
  <div class="code-container">
<pre>from pathlib import Path
from typing import Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape
from db_manager import get_syllabus, DEFAULT_DB_PATH
from obe_schemas import FullSyllabusSchema

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
TEMPLATE_FILENAME = "uphsd_ccs_template.html"

def get_jinja_env() -> Environment:
    '''Configures and returns the Jinja2 template environment with autoescaping.'''
    if not TEMPLATES_DIR.exists():
        raise FileNotFoundError(f"Templates directory not found at '{TEMPLATES_DIR}'.")
    return Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html", "xml"])
    )

def render_syllabus_html(course_code: str, db_path: str = DEFAULT_DB_PATH) -> str:
    '''Queries SQLite for course_code and compiles the official UPHSD CCS syllabus HTML.'''
    syllabus: Optional[FullSyllabusSchema] = get_syllabus(course_code, db_path=db_path)
    if not syllabus:
        raise ValueError(f"No syllabus records found in database for course code '{course_code}'.")

    env = get_jinja_env()
    template = env.get_template(TEMPLATE_FILENAME)
    return template.render(
        course=syllabus.course_metadata,
        clos=syllabus.course_outcomes,
        schedule=syllabus.weekly_schedule
    )

def export_to_file(course_code: str, output_path: Optional[str] = None, db_path: str = DEFAULT_DB_PATH) -> str:
    '''Compiles HTML syllabus and saves it to a persistent output deliverable file.'''
    html_content = render_syllabus_html(course_code, db_path=db_path)
    if not output_path:
        clean_code = course_code.replace(" ", "_").replace("/", "-")
        outputs_dir = BASE_DIR / "outputs"
        outputs_dir.mkdir(parents=True, exist_ok=True)
        output_file = outputs_dir / f"official_syllabus_{clean_code}.html"
    else:
        output_file = Path(output_path)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[+] Successfully exported official syllabus to '{output_file}'.")
    return str(output_file.resolve())</pre>
  </div>

  <h3>3.5 Relational Persistence &amp; Human-in-the-Loop CRUD (<code>db_manager.py</code>)</h3>
  <p>
    Provides transactional persistence, atomic parent-child cascade deletions, and faculty CLO editing:
  </p>
  <div class="code-container">
<pre>def save_syllabus(syllabus: FullSyllabusSchema, db_path: str = DEFAULT_DB_PATH) -> int:
    '''Atomically persists full syllabus across all 4 relational tables.'''
    with get_connection(db_path) as conn:
        with conn:
            # 1. Insert course metadata
            cur = conn.execute(
                "INSERT OR REPLACE INTO courses (course_code, course_title, course_description, "
                "credit_units, lecture_hours, lab_hours, prerequisites) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (m.course_code, m.course_title, m.course_description, m.credit_units, 
                 m.lecture_hours, m.lab_hours, m.prerequisites)
            )
            course_id = cur.lastrowid

            # 2. Insert Course Learning Outcomes
            for clo in syllabus.course_outcomes:
                conn.execute(
                    "INSERT INTO course_outcomes (course_id, clo_id, description, bloom_level, "
                    "program_outcomes_mapped) VALUES (?, ?, ?, ?, ?)",
                    (course_id, clo.clo_id, clo.description, clo.bloom_level, 
                     json.dumps(clo.program_outcomes_mapped))
                )

            # 3. Insert Weekly Schedules & Lesson Outcomes
            for week in syllabus.weekly_schedule:
                w_cur = conn.execute(
                    "INSERT INTO weekly_schedules (course_id, week_number, topics, "
                    "teaching_learning_activities, assessment_tasks) VALUES (?, ?, ?, ?, ?)",
                    (course_id, week.week_number, json.dumps(week.topics),
                     json.dumps(week.teaching_learning_activities), json.dumps(week.assessment_tasks))
                )
                sched_id = w_cur.lastrowid
                for llo in week.lesson_outcomes:
                    conn.execute(
                        "INSERT INTO lesson_outcomes (schedule_id, llo_id, domain, description) "
                        "VALUES (?, ?, ?, ?)",
                        (sched_id, llo.llo_id, llo.domain, llo.description)
                    )
    return course_id

def update_clo(clo_id: str, new_description: str, db_path: str = DEFAULT_DB_PATH) -> bool:
    '''Updates a CLO statement after validating active Bloom verbs.'''
    CourseOutcomeSchema.validate_action_verbs(new_description)
    with get_connection(db_path) as conn:
        with conn:
            conn.execute("UPDATE course_outcomes SET description = ? WHERE clo_id = ?", 
                         (new_description, clo_id))
    return True

def delete_course(course_code: str, db_path: str = DEFAULT_DB_PATH) -> bool:
    '''Nuclear deletes a specific course and all its cascaded relational records.'''
    norm_code = course_code.strip()
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM courses WHERE UPPER(TRIM(course_code)) = UPPER(?);", (norm_code,))
        rows = cursor.fetchall()
        for row in rows:
            cid = row["id"]
            cursor.execute("DELETE FROM lesson_outcomes WHERE schedule_id IN (SELECT id FROM weekly_schedules WHERE course_id = ?);", (cid,))
            cursor.execute("DELETE FROM weekly_schedules WHERE course_id = ?;", (cid,))
            cursor.execute("DELETE FROM course_outcomes WHERE course_id = ?;", (cid,))
            cursor.execute("DELETE FROM courses WHERE id = ?;", (cid,))
        conn.commit()
        conn.execute("VACUUM;")
    return True</pre>
  </div>

  <h3>3.6 Selective Synthesis &amp; Batch Worker (<code>app.py</code>)</h3>
  <p>
    Enables selective batch generation that skips existing courses to save computation time:
  </p>
  <div class="code-container">
<pre>def run_batch_generation_worker(skip_existing: bool = False):
    all_subjects = get_all_subjects()
    if skip_existing:
        queue = [s for s in all_subjects if not is_subject_generated(s["course_code"])]
        skipped = [s for s in all_subjects if is_subject_generated(s["course_code"])]
    else:
        queue = all_subjects
        skipped = []

    total = len(queue)
    for idx, subj in enumerate(queue, 1):
        code = subj["course_code"]
        # Progress callback calculating granular percentage
        base_pct = int(((idx - 1) / total) * 100)
        subj_weight = 100.0 / total
        llm_engine.generate_custom_subject(course_code=code, progress_callback=make_batch_progress())</pre>
  </div>

  <div style="margin-top: 30px; padding-top: 10px; border-top: 1px solid #cbd5e1; font-size: 8.5pt; color: #64748b; text-align: center;">
    College of Computer Studies • University of Perpetual Help System DALTA • Molino Campus<br>
    BSCS 3112 / Artificial Intelligence Mini-Project • Evaluated by Prof. Roberto L. Malitao • All Rights Reserved
  </div>

</body>
</html>
"""

output_path = BASE_DIR / "compiled_documentation.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"[+] Documentation HTML successfully generated at: {output_path}")

# Automated Compilation to PDF via Headless Edge
import subprocess
import shutil

root_dir = BASE_DIR.parent
doc_pdf_root = root_dir / "Documentation.pdf"
full_pdf_root = root_dir / "OBE_Syllabus_Generator_18th_Week_Documentation.pdf"
doc_pdf_sub = BASE_DIR / "OBE_Syllabus_Generator_18th_Week_Documentation.pdf"

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if os.path.exists(edge_path):
    print("[*] Compiling Documentation.pdf via Microsoft Edge headless print-to-pdf...")
    temp_profile = os.environ.get("TEMP", str(BASE_DIR)) + "\\edge_doc_compile_profile"
    cmd = [
        edge_path,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--user-data-dir={temp_profile}",
        f"--print-to-pdf={doc_pdf_root}",
        "http://127.0.0.1:8001/compiled_documentation.html"
    ]
    try:
        subprocess.run(cmd, check=True, timeout=30)
        if doc_pdf_root.exists():
            shutil.copy(doc_pdf_root, full_pdf_root)
            shutil.copy(doc_pdf_root, doc_pdf_sub)
            print(f"[+] Successfully compiled '{doc_pdf_root.name}' ({doc_pdf_root.stat().st_size:,} bytes).")
            print(f"[+] Synced copies to '{full_pdf_root.name}' and '18thWeekOutput/'.")
    except Exception as e:
        print(f"[-] Automated PDF compilation warning: {e}")
    finally:
        shutil.rmtree(temp_profile, ignore_errors=True)
else:
    print(f"[-] Edge binary not found at '{edge_path}'.")
