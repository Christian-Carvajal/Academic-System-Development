# OBE_RUBRIC_SPECIFICATION.md — Pedagogical & Academic Rubric

## 1. Institutional Standards (UPHSD College of Computer Studies)
Outcome-Based Education (OBE) requires that curriculum design starts with clear, measurable outcomes that students demonstrate upon course completion, rather than passive content topics taught by the instructor.

### Outcomes Hierarchy
```text
Institutional Mission & Core Values
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

| Cognitive Level | Action Verbs Permitted | Banned Passive Verbs |
|---|---|---|
| **Remember / Understand** | `Identify`, `Define`, `Recall`, `Describe`, `Explain`, `Classify` | `Know`, `Understand`, `Learn`, `Be exposed to`, `Study`, `Be familiar with` |
| **Apply / Analyze** | `Apply`, `Implement`, `Configure`, `Calculate`, `Analyze`, `Differentiate` | (Same as above) |
| **Evaluate / Create** | `Design`, `Develop`, `Synthesize`, `Integrate`, `Defend`, `Construct` | (Same as above) |

*Rule:* Every Course Outcome must begin with one of the allowed active verbs. The Pydantic validator `@field_validator("co_description")` automatically rejects strings containing banned verbs.

---

## 3. Tripartite LLO Structure (K / S / A)
Every instructional week must scaffold student learning across all three educational domains:
1. **Knowledge (K) — Cognitive Domain:** Conceptual and theoretical foundations (e.g., algorithmic complexity, graph theory).
2. **Skills (S) — Psychomotor Domain:** Practical application, coding, tools, and system construction (e.g., writing recursive functions in Python/C++).
3. **Attitude (A) — Affective Domain:** Professional ethics, persistence in debugging, precision, and collaborative workflow.

---

## 4. 14-Week Schedule Invariants

* **Total Weeks:** Exactly 14 weeks (`week_number: 1..14`).
* **Prelim Period:** Weeks 1 through 6 (`period: "PRELIM"`).
* **Midterm Exam Week:** Week 7 (`period: "MIDTERM"`, topic must contain `Midterm Examination`).
* **Final Period:** Weeks 8 through 13 (`period: "FINAL"`).
* **Final Exam Week:** Week 14 (`period: "FINAL"`, topic must contain `Final Examination`).
* **Coverage Guarantee:** 100% of defined Course Outcomes (`clo_number`) must be mapped at least once in `aligned_co` across the 14-week schedule.

---

## 5. Institutional Grading Formula

Assessments map to term grades using the mandatory institutional weights:

$$\text{Class Standing} = (\text{Quizzes} \times 30\%) + (\text{Research} \times 20\%) + (\text{Seatwork/Lab} \times 50\%)$$

$$\text{Term Grade} = (\text{Class Standing} \times 70\%) + (\text{Major Exam} \times 30\%)$$

```python
quizzes_pct: float = 30.0
research_pct: float = 20.0
seatwork_lab_pct: float = 50.0
class_standing_weight: float = 70.0
major_exam_weight: float = 30.0
```
