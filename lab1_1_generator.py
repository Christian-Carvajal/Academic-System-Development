"""
lab1_1_generator.py
CLI script for generating and validating core course details and OBE Course Outcomes.
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

from obe_schemas import CourseOutcomesPayload

MODEL_NAME = "qwen3.5:4b"

SYSTEM_PROMPT_LAB1_1 = """You are an expert IT/CS Curriculum Designer for the College of Computer Studies at UPHSD.
Your task is to generate Course Learning Outcomes (COs) strictly compliant with Outcome-Based Education (OBE).

IMPORTANT EFFICIENCY CONSTRAINT:
Keep internal reasoning extremely brief (under 150 words). Immediately generate the target JSON object.

STRICT COMPLIANCE RULES:
1. NEVER use non-measurable verbs such as "understand", "learn", "know", "be exposed to", or "study".
2. Every CO MUST specify bloom_level as one of: "Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create".
   Every CO statement MUST begin with an active Bloom's Taxonomy verb matched to cognitive levels:
   - Remember/Understand: Identify, Define, Recall, Describe.
   - Apply/Analyze: Apply, Implement, Configure, Calculate, Analyze.
   - Evaluate/Create: Design, Develop, Synthesize, Integrate, Defend.
3. You MUST generate between 4 and 5 Course Outcomes.
4. Output MUST be 100% valid JSON matching the schema below. Do not include markdown fences or conversational intros.

TARGET JSON SCHEMA:
{
  "course_title": "string",
  "course_code": "string",
  "course_description": "string",
  "course_outcomes": [
    {
      "clo_number": 1,
      "bloom_level": "Apply",
      "co_description": "Implement...",
      "mapped_po": [1, 2]
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
            cleaned = cleaned[end_think + len("</think>"):].strip()
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        return cleaned[start:end + 1]
    return cleaned

def generate_course_outcomes(course_title: str, course_code: str, description: str, target_pos: str, max_retries: int = 4) -> CourseOutcomesPayload:
    user_prompt = f"""Generate 4 to 5 Course Outcomes for the following subject:
Course Title: {course_title}
Course Code: {course_code}
Description: {description}
Target Program Outcomes (POs): {target_pos}
"""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_LAB1_1},
        {"role": "user", "content": user_prompt}
    ]

    for attempt in range(1, max_retries + 1):
        print(f"[*] [Lab 1.1] Querying {MODEL_NAME} with format='json' (Attempt {attempt}/{max_retries})...")
        try:
            response = ollama.chat(
                model=MODEL_NAME,
                format="json",
                messages=messages,
                options={
                    "temperature": 0.2,
                    "num_ctx": 16384,
                    "num_predict": 4096
                }
            )
            raw_text = response["message"].get("content", "").strip()
            if not raw_text and response["message"].get("thinking"):
                raw_text = response["message"]["thinking"].strip()

            clean_json = extract_json(raw_text)
            if not clean_json or clean_json == "{}":
                raise ValueError("Model generated empty content. Keep reasoning short and directly output JSON.")

            data = json.loads(clean_json)
            validated = CourseOutcomesPayload(**data)
            print("[+] [Lab 1.1] Schema validation successful.")
            return validated
        except (json.JSONDecodeError, ValidationError, ValueError) as exc:
            print(f"[-] [Lab 1.1] Attempt {attempt} validation failed: {exc}")
            if attempt == max_retries:
                raise exc
            feedback = (
                f"Your output failed validation with error:\n{str(exc)}\n"
                "Keep reasoning under 100 words. Regenerate the entire JSON object strictly complying with the schema."
            )
            messages.append({"role": "assistant", "content": raw_text if 'raw_text' in locals() else "{}"})
            messages.append({"role": "user", "content": feedback})

if __name__ == "__main__":
    course_data = {
        "course_title": "Data Structures and Algorithms",
        "course_code": "CS 3110",
        "description": "Study of fundamental data structures, recursive algorithms, dynamic memory, sorting, trees, and algorithmic complexity.",
        "target_pos": "PLO 1 (Computing Knowledge), PLO 2 (Problem Analysis), PLO 3 (Systems Development)"
    }
    result = generate_course_outcomes(**course_data)
    output_path = BASE_DIR / "co_output_lab1_1.json"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result.model_dump_json(indent=2))
    print(f"[+] Saved validated Course Outcomes to {output_path.name}")
