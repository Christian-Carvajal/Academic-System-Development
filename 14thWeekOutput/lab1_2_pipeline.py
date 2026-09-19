"""
lab1_2_pipeline.py
Chained generation script loading Lab 1.1 COs and generating a complete 14-week syllabus.
"""
import json
import sys
from pathlib import Path
import ollama
from pydantic import ValidationError

# Ensure local directory is on sys.path for robust module resolution
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from obe_schemas import (
    CourseOutcomesPayload,
    FullSyllabusPayload,
    WeeklyScheduleItem,
    GradingBreakdown
)

MODEL_NAME = "qwen3.5:4b"

SYSTEM_PROMPT_LAB1_2 = """You are an expert IT/CS Curriculum Designer for the College of Computer Studies at UPHSD.
Generate a complete 14-week course schedule for an Outcome-Based Education (OBE) syllabus in 100% valid JSON.

STRICT BUSINESS & PEDAGOGICAL RULES:
1. Schedule MUST contain EXACTLY 14 weeks (week_number 1 to 14).
2. Week 7 is STRICTLY the Midterm Examination:
   - period: "MIDTERM"
   - topic: "Midterm Examination"
   - teaching_learning_activity: "Departmental Midterm Practical and Theoretical Exam"
   - assessment_tool: "Departmental Exam Rubric"
   - evidence: "Examination Paper and Practical Code Submission"
   - llos: exactly 3 items (K, S, A) reviewing/evaluating midterm competencies.
3. Week 14 is STRICTLY the Final Examination:
   - period: "FINAL"
   - topic: "Final Examination / Capstone Defense"
   - teaching_learning_activity: "Comprehensive Final Project Defense and Technical Exam"
   - assessment_tool: "Comprehensive Exam Rubric"
   - evidence: "Final Project Repository and Written Examination Paper"
   - llos: exactly 3 items (K, S, A) synthesizing full course competencies.
4. Periods: Weeks 1-6 = "PRELIM", Week 7 = "MIDTERM", Weeks 8-13 = "FINAL", Week 14 = "FINAL".
5. Every week MUST contain EXACTLY 3 LLOs with categories "K", "S", and "A" and field names "category" and "outcome_text".
6. Every week MUST specify non-empty "teaching_learning_activity", "assessment_tool", and "evidence".
7. Every CLO index provided in the prompt MUST be covered at least once in "aligned_co" across the schedule.
8. Output MUST be 100% valid JSON matching the schema below without markdown fences.

TARGET JSON SCHEMA:
{
  "weekly_schedule": [
    {
      "week_number": 1,
      "period": "PRELIM",
      "topic": "Introduction to Data Structures & Abstract Data Types",
      "llos": [
        {
          "category": "K",
          "outcome_text": "Explain the differences between linear and non-linear data structures."
        },
        {
          "category": "S",
          "outcome_text": "Implement array-based list operations and dynamic memory allocation."
        },
        {
          "category": "A",
          "outcome_text": "Demonstrate precision in memory management and pointer debugging."
        }
      ],
      "teaching_learning_activity": "Hands-on coding lab on dynamic memory and pointers",
      "assessment_tool": "Laboratory Rubric & Programming Exercise",
      "evidence": "Executable Source Code in C++/Python",
      "aligned_co": [1]
    }
  ]
}
"""

def extract_json(text: str) -> str:
    """Safely extracts the outermost JSON substring, stripping any CoT <think> blocks."""
    cleaned = text.strip()
    if "<think>" in cleaned:
        end_think = cleaned.find("</think>")
        if end_think != -1:
            after_think = cleaned[end_think + len("</think>"):].strip()
            if "{" in after_think and "}" in after_think:
                cleaned = after_think
            else:
                inside_think = cleaned[len("<think>"):end_think].strip()
                if "{" in inside_think and "}" in inside_think:
                    cleaned = inside_think
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        return cleaned[start:end + 1]
    return cleaned

def generate_weekly_schedule(co_payload: CourseOutcomesPayload, max_retries: int = 4) -> FullSyllabusPayload:
    co_context = json.dumps([co.model_dump() for co in co_payload.course_outcomes], indent=2)
    user_prompt = f"""Generate the full 14-week schedule for:
Course: {co_payload.course_title} ({co_payload.course_code})
Course Outcomes:
{co_context}

Output the complete JSON object with the "weekly_schedule" array containing all 14 weeks.
"""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_LAB1_2},
        {"role": "user", "content": user_prompt}
    ]

    all_clo_numbers = {co.clo_number for co in co_payload.course_outcomes}

    for attempt in range(1, max_retries + 1):
        print(f"[*] [Lab 1.2] Generating 14-Week Schedule (Attempt {attempt}/{max_retries})...")
        try:
            response = ollama.chat(
                model=MODEL_NAME,
                format="json",
                messages=messages,
                options={
                    "temperature": 0.2,
                    "num_ctx": 16384,
                    "num_predict": 8192
                }
            )
            raw_text = response["message"].get("content", "").strip()
            if not raw_text and response["message"].get("thinking"):
                raw_text = response["message"]["thinking"].strip()
            elif raw_text and response["message"].get("thinking") and "{" not in raw_text and "{" in response["message"]["thinking"]:
                raw_text = response["message"]["thinking"].strip()
            clean_json = extract_json(raw_text)
            data = json.loads(clean_json)

            if "weekly_schedule" not in data:
                raise KeyError("JSON missing required root key 'weekly_schedule'.")

            schedule_items = [WeeklyScheduleItem(**item) for item in data["weekly_schedule"]]

            if len(schedule_items) != 14:
                raise ValueError(f"Expected 14 weeks, received {len(schedule_items)}.")

            w7 = next((w for w in schedule_items if w.week_number == 7), None)
            w14 = next((w for w in schedule_items if w.week_number == 14), None)
            if not w7 or "midterm" not in w7.topic.lower():
                raise ValueError("Week 7 is not designated as Midterm Examination.")
            if not w14 or "final" not in w14.topic.lower():
                raise ValueError("Week 14 is not designated as Final Examination.")

            covered_cos = set()
            for w in schedule_items:
                covered_cos.update(w.aligned_co)
            missing = all_clo_numbers - covered_cos
            if missing:
                raise ValueError(f"Course Outcomes {missing} are not covered in the schedule.")

            full_syllabus = FullSyllabusPayload(
                course_code=co_payload.course_code,
                course_title=co_payload.course_title,
                course_description=co_payload.course_description,
                course_outcomes=co_payload.course_outcomes,
                weekly_schedule=schedule_items,
                grading_breakdown=GradingBreakdown()
            )
            print("[+] [Lab 1.2] Schedule validation and pedagogical alignment passed.")
            return full_syllabus

        except (json.JSONDecodeError, ValidationError, ValueError, KeyError) as exc:
            print(f"[-] [Lab 1.2] Attempt {attempt} validation failed: {exc}")
            if attempt == max_retries:
                raise exc
            feedback = (
                f"Validation error:\n{str(exc)}\n"
                f"Regenerate the entire 14-week schedule JSON ensuring:\n"
                f"- Exactly 14 weeks with week_number 1 to 14\n"
                f"- Keys: week_number, period, topic, llos (with category 'K'|'S'|'A' and outcome_text), "
                f"teaching_learning_activity, assessment_tool, evidence, aligned_co\n"
                f"- Week 7 Midterm, Week 14 Final\n"
                f"- All CO IDs {list(all_clo_numbers)} covered."
            )
            # Replace previous attempt to keep context window clean
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT_LAB1_2},
                {"role": "user", "content": user_prompt},
                {"role": "user", "content": feedback}
            ]

if __name__ == "__main__":
    outputs_dir = BASE_DIR / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)

    # Check outputs/co_output_lab1_1.json first, fallback to BASE_DIR / co_output_lab1_1.json
    co_file = outputs_dir / "co_output_lab1_1.json"
    if not co_file.exists():
        co_file = BASE_DIR / "co_output_lab1_1.json"

    if not co_file.exists():
        print(f"[-] Error: 'co_output_lab1_1.json' was not found in '{outputs_dir}' or '{BASE_DIR}'.")
        print("[-] Please run 'python lab1_1_generator.py' first to generate the Course Outcomes context.")
        sys.exit(1)

    print(f"[*] Loading Course Outcomes context from '{co_file}'...")
    with open(co_file, "r", encoding="utf-8") as f:
        co_payload = CourseOutcomesPayload(**json.load(f))

    syllabus = generate_weekly_schedule(co_payload)
    output_deliverable = outputs_dir / "sample_output_syllabus.json"
    with open(output_deliverable, "w", encoding="utf-8") as f:
        f.write(syllabus.model_dump_json(indent=2))
    print(f"[+] Final deliverable saved to {output_deliverable}")
