# OBE_RUBRIC_SPECIFICATION.md — Pedagogical & Academic Rubric

## 1. Institutional Standards (UPHSD College of Computer Studies)
Outcome-Based Education (OBE) requires curriculum design to begin with clear, measurable outcomes that students demonstrate upon course completion, rather than passive content topics taught by the instructor.

Under the direction of **Prof. Roberto L. Malitao** at the **University of Perpetual Help System DALTA (UPHSD)**, syllabi must adhere to **CHED CMO 25 series of 2015** (Policies, Standards, and Guidelines for Bachelor of Science in Computer Science).

### Outcomes Hierarchy
```text
Institutional Mission & Core Values (UPHSD DALTA)
                       ↓
         Graduate Attributes (GAs)
                       ↓
   Program Educational Objectives (PEOs)
                       ↓
   Program Learning Outcomes (PLOs / POs)
                       ↓
   Course Learning Outcomes (CLOs / COs)
                       ↓
   Lesson Learning Outcomes (LLOs / ILOs)
```

---

## 2. Bloom's Taxonomy Cognitive Verbs Matrix

Every Course Outcome (CLO) and Lesson Outcome (LLO) must start with an active, measurable cognitive verb corresponding to Bloom's Revised Taxonomy.

| Cognitive Level | Permitted Action Verbs | Strictly Banned Passive Verbs |
|---|---|---|
| **Remember / Understand** | `Identify`, `Define`, `Recall`, `Describe`, `Explain`, `Classify`, `Summarize` | `Know`, `Understand`, `Learn`, `Be exposed to`, `Study`, `Be familiar with` |
| **Apply / Analyze** | `Apply`, `Implement`, `Configure`, `Calculate`, `Analyze`, `Differentiate`, `Examine` | `Appreciate`, `Grasp`, `Perceive`, `Review`, `Comprehend` |
| **Evaluate / Create** | `Design`, `Develop`, `Synthesize`, `Integrate`, `Defend`, `Construct`, `Formulate` | `Internalize`, `Become aware of`, `Look at` |

### Automated Pydantic Enforcement
The schema validator in `obe_schemas.py` inspects every outcome statement at runtime:
```python
BANNED_PASSIVE_VERBS = {
    "understand", "know", "learn", "study", "familiarize",
    "be exposed to", "appreciate", "grasp", "comprehend"
}

@field_validator("description")
@classmethod
def validate_bloom_action_verb(cls, value: str) -> str:
    cleaned = value.strip()
    first_word = cleaned.split()[0].lower() if cleaned else ""
    if first_word in BANNED_PASSIVE_VERBS:
        raise ValueError(
            f"Banned non-measurable verb '{first_word}' detected in outcome statement. "
            "Must start with an active Bloom's Taxonomy verb (e.g., Analyze, Implement, Design)."
        )
    return cleaned
```

---

## 3. Tripartite Educational Domains (K / S / A)
Every instructional week must systematically scaffold student competencies across all three educational domains:

1. **Knowledge (K) — Cognitive Domain:** Theoretical concepts, computational principles, algorithms, and models (e.g., *Formulate recurrence relations for divide-and-conquer algorithms*).
2. **Skills (S) — Psychomotor Domain:** Practical implementation, code development, testing, debugging, and tool mastery (e.g., *Implement Dijkstra's shortest-path algorithm in Python*).
3. **Attitude (A) — Affective Domain:** Professional ethics, persistence in troubleshooting, collaborative teamwork, and code cleanliness (e.g., *Demonstrate adherence to PEP 8 standards and ethical data collection practices*).

---

## 4. 18-Week Semester Schedule Invariants (CHED CMO 25 s.2015)

In accordance with Philippine higher education standards for collegiate degree programs, each semester comprises exactly **18 academic weeks**:

```text
+-----------------------------------------------------------------------------------------+
|                              18-WEEK ACADEMIC SCHEDULE MAP                              |
+-----------------------------------------------------------------------------------------+
| Weeks 1–8   | Midterm Instructional Term (Foundations, Lab Exercises, Formative Quizzes) |
| Week 9      | MIDTERM EXAMINATION MILESTONE LOCK (Departmental Examination)             |
| Weeks 10–17 | Final Instructional Term (Advanced Topics, Machine Problems, Projects)   |
| Week 18     | FINAL EXAMINATION & CAPSTONE DEFENSE LOCK (Departmental Final Defense)    |
+-----------------------------------------------------------------------------------------+
```

### Schedule Verification Rules:
1. **Total Weeks:** Exactly 18 weeks (`week_number: 1..18`). No gaps, duplicates, or missing weeks allowed.
2. **Period Designation:**
   - Weeks 1–8: `period: "MIDTERM"`
   - Week 9: `period: "MIDTERM EXAM"` (Milestone Lock)
   - Weeks 10–17: `period: "FINAL"`
   - Week 18: `period: "FINAL EXAM"` (Milestone Lock)
3. **Week 9 Milestone Lock:** Module topic must explicitly contain `Midterm Examination` or `Departmental Midterm Exam`.
4. **Week 18 Milestone Lock:** Module topic must explicitly contain `Final Examination`, `Final Project Defense`, or `Capstone Defense`.
5. **100% CLO Mapping Guarantee:** 100% of defined Course Learning Outcomes (`clo_id`: `CLO 1` .. `CLO 4/5`) must be aligned with weekly schedule items.
6. **Tripartite Completeness:** The entire 18-week curriculum must comprehensively incorporate Knowledge (K), Skills (S), and Attitude (A) outcomes.

---

## 5. Institutional Grading Formula

Assessments map to term grades using the mandatory institutional formula of the **UPHSD College of Computer Studies**:

$$\text{Class Standing} = (\text{Quizzes} \times 30\%) + (\text{Research \& Assignments} \times 20\%) + (\text{Hands-on Laboratory \& Machine Problems} \times 50\%)$$

$$\text{Term Grade} = (\text{Class Standing} \times 70\%) + (\text{Major Examination} \times 30\%)$$

```python
# UPHSD CCS Institutional Grading Parameters
quizzes_weight: float = 30.0        # Formative quizzes & mastery assessments
research_weight: float = 20.0       # Research papers, assignments & case studies
laboratory_weight: float = 50.0     # Laboratory experiments & machine problems
class_standing_weight: float = 70.0 # Total Class Standing Factor
major_exam_weight: float = 30.0     # Departmental Examination Factor
```

---

## 6. Automated Accreditation Audit Engine (7 Invariants)

The microservice backend exposes `/api/audit?code={course_code}`, programmatically asserting 100% compliance before institutional approval:

| Invariant ID | Assertion Criteria | Threshold | Severity |
|---|---|---|---|
| **INV-1** | `len(weekly_schedule) == 18` | Exactly 18 scheduled academic weeks | Blocking |
| **INV-2** | `week_9.topic.contains("midterm" | "exam")` | Week 9 locked to Departmental Midterm Exam | Blocking |
| **INV-3** | `week_18.topic.contains("final" | "exam" | "defense")` | Week 18 locked to Final Exam / Capstone Defense | Blocking |
| **INV-4** | `set(all_domains) == {"K", "S", "A"}` | Full coverage of Knowledge, Skills, and Attitude | Blocking |
| **INV-5** | `all(not clo.startswith(banned_verbs))` | Zero unmeasurable passive verbs | Blocking |
| **INV-6** | `len(course_outcomes) >= 3 and all(clo.mapped_pos)` | All CLOs aligned to Program Learning Outcomes | Blocking |
| **INV-7** | Institutional 70% Class Standing / 30% Major Exam | Strict UPHSD CCS Institutional Grading Scheme | Informational |
