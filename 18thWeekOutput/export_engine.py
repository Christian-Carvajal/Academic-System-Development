"""
export_engine.py
Institutional Jinja2 Document Assembly & HTML/PDF Syllabus Compilation Engine.

Authors:
- Christian Ezekiel L. Carvajal (Lead Architect & Systems Engineer)
- John Miko P. Sarsalijo (Collaborative Partner & Systems Engineer)

Institution: College of Computer Studies, University of Perpetual Help System DALTA (Molino Campus)
Course: BSCS 3112 / Artificial Intelligence (Lesson 5 - Midterm Mini-Project)
Instructor: Prof. Roberto L. Malitao
"""
import os
from pathlib import Path
from typing import Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape

from db_manager import get_syllabus, DEFAULT_DB_PATH
from obe_schemas import FullSyllabusSchema

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
TEMPLATE_FILENAME = "uphsd_ccs_template.html"


def get_jinja_env() -> Environment:
    """Configures and returns the Jinja2 template environment with autoescaping."""
    if not TEMPLATES_DIR.exists():
        raise FileNotFoundError(f"Templates directory not found at '{TEMPLATES_DIR}'.")
    return Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html", "xml"])
    )


def render_syllabus_html(course_code: str, db_path: str = DEFAULT_DB_PATH) -> str:
    """
    Queries the SQLite database for the specified course_code and compiles the
    official UPHSD CCS institutional HTML syllabus document.
    """
    syllabus: Optional[FullSyllabusSchema] = get_syllabus(course_code, db_path=db_path)
    if not syllabus:
        raise ValueError(f"No syllabus records found in database for course code '{course_code}'.")

    env = get_jinja_env()
    template = env.get_template(TEMPLATE_FILENAME)

    rendered_html = template.render(
        course=syllabus.course_metadata,
        clos=syllabus.course_outcomes,
        schedule=syllabus.weekly_schedule
    )
    return rendered_html


def export_to_file(
    course_code: str,
    output_path: Optional[str] = None,
    db_path: str = DEFAULT_DB_PATH
) -> str:
    """
    Compiles the HTML syllabus and saves it to a persistent output file.
    Returns the absolute path of the generated HTML document.
    """
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
    return str(output_file.resolve())


# =============================================================================
# CLI TEST FIXTURE
# =============================================================================

if __name__ == "__main__":
    import sys
    target_course = " ".join(sys.argv[1:]).strip() if len(sys.argv) > 1 else "CS 3110"
    if not target_course:
        target_course = "CS 3110"
    print(f"[*] Testing export engine for course '{target_course}'...")
    try:
        exported_path = export_to_file(target_course)
        print(f"[+] Verification: File size is {os.path.getsize(exported_path):,} bytes.")
    except Exception as exc:
        print(f"[-] Export engine execution failed: {exc}")
        sys.exit(1)
