"""
db_manager.py
Relational SQLite Database Manager & CRUD Operations for UPHSD CCS OBE Syllabi.

Authors:
- Christian Ezekiel L. Carvajal (Lead Architect & Systems Engineer)
- John Miko P. Sarsalijo (Collaborative Partner & Systems Engineer)

Institution: College of Computer Studies, University of Perpetual Help System DALTA (Molino Campus)
Course: BSCS 3112 / Artificial Intelligence (Lesson 5 - Midterm Mini-Project)
Instructor: Prof. Roberto L. Malitao
"""
import os
import json
import sqlite3
from pathlib import Path
from typing import Optional, List, Dict, Any

from obe_schemas import (
    CourseMetadataSchema,
    CourseOutcomeSchema,
    LessonOutcomeSchema,
    WeeklyScheduleSchema,
    FullSyllabusSchema
)

BASE_DIR = Path(__file__).resolve().parent
DATABASE_DIR = BASE_DIR / "database"
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_DB_PATH = str(DATABASE_DIR / "obe_syllabus.db")
SCHEMA_SQL_PATH = DATABASE_DIR / "schema.sql"
if not SCHEMA_SQL_PATH.exists() and (BASE_DIR / "schema.sql").exists():
    SCHEMA_SQL_PATH = BASE_DIR / "schema.sql"


def get_connection(db_path: str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """Creates a database connection with foreign keys enabled."""
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str = DEFAULT_DB_PATH) -> None:
    """
    Initializes the SQLite database using schema.sql.
    Creates normalized tables: courses, course_outcomes, weekly_schedules, lesson_outcomes.
    """
    if not SCHEMA_SQL_PATH.exists():
        raise FileNotFoundError(f"Schema file not found at '{SCHEMA_SQL_PATH}'.")

    with open(SCHEMA_SQL_PATH, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    with get_connection(db_path) as conn:
        conn.executescript(schema_sql)
    print(f"[+] Database initialized successfully at '{db_path}'.")


def save_syllabus(syllabus: FullSyllabusSchema, db_path: str = DEFAULT_DB_PATH) -> int:
    """
    Persists a validated FullSyllabusSchema into normalized relational tables.
    Uses an atomic transaction to insert metadata, CLOs, weeks, and LLOs.
    Returns the integer primary key ID of the inserted/updated course.
    """
    meta = syllabus.course_metadata
    prereqs = json.dumps(meta.prerequisites) if isinstance(meta.prerequisites, list) else str(meta.prerequisites)

    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        
        # 1. Upsert course record
        cursor.execute(
            """
            INSERT INTO courses (course_code, course_title, credit_units, lecture_hours, lab_hours, prerequisites, course_description, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(course_code) DO UPDATE SET
                course_title=excluded.course_title,
                credit_units=excluded.credit_units,
                lecture_hours=excluded.lecture_hours,
                lab_hours=excluded.lab_hours,
                prerequisites=excluded.prerequisites,
                course_description=excluded.course_description,
                updated_at=CURRENT_TIMESTAMP
            RETURNING id;
            """,
            (meta.course_code, meta.course_title, meta.credit_units, meta.lecture_hours, meta.lab_hours, prereqs, meta.course_description)
        )
        row = cursor.fetchone()
        course_id = row[0]

        # 2. Clear old children if updating (cascades or delete explicitly)
        cursor.execute("DELETE FROM course_outcomes WHERE course_id = ?", (course_id,))
        cursor.execute("DELETE FROM weekly_schedules WHERE course_id = ?", (course_id,))

        # 3. Insert Course Learning Outcomes (CLOs)
        for clo in syllabus.course_outcomes:
            cursor.execute(
                """
                INSERT INTO course_outcomes (course_id, clo_id, description, bloom_level, program_outcomes_mapped)
                VALUES (?, ?, ?, ?, ?);
                """,
                (course_id, clo.clo_id, clo.description, clo.bloom_level, json.dumps(clo.program_outcomes_mapped))
            )

        # 4. Insert Weekly Schedules and nested Lesson Learning Outcomes (LLOs)
        for week in syllabus.weekly_schedule:
            topics_val = json.dumps(week.topics) if isinstance(week.topics, list) else str(week.topics)
            cursor.execute(
                """
                INSERT INTO weekly_schedules (course_id, week_number, topics, teaching_learning_activities, assessment_tasks, resources)
                VALUES (?, ?, ?, ?, ?, ?)
                RETURNING id;
                """,
                (
                    course_id,
                    week.week_number,
                    topics_val,
                    json.dumps(week.teaching_learning_activities),
                    json.dumps(week.assessment_tasks),
                    json.dumps(week.resources)
                )
            )
            schedule_id = cursor.fetchone()[0]

            for llo in week.lesson_outcomes:
                cursor.execute(
                    """
                    INSERT INTO lesson_outcomes (schedule_id, llo_id, description, domain)
                    VALUES (?, ?, ?, ?);
                    """,
                    (schedule_id, llo.llo_id, llo.description, llo.domain)
                )

        conn.commit()
    print(f"[+] Persisted syllabus for '{meta.course_code}' (Course ID: {course_id}) into SQLite.")
    return course_id


def get_syllabus(course_code: str, db_path: str = DEFAULT_DB_PATH) -> Optional[FullSyllabusSchema]:
    """
    Queries relational tables and reconstructs the strongly typed FullSyllabusSchema object.
    Returns None if course_code is not found.
    """
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        
        # 1. Fetch course metadata
        cursor.execute("SELECT * FROM courses WHERE course_code = ?;", (course_code,))
        course_row = cursor.fetchone()
        if not course_row:
            return None

        course_id = course_row["id"]
        try:
            prereqs = json.loads(course_row["prerequisites"])
        except Exception:
            prereqs = course_row["prerequisites"]

        metadata = CourseMetadataSchema(
            course_code=course_row["course_code"],
            course_title=course_row["course_title"],
            credit_units=course_row["credit_units"],
            lecture_hours=course_row["lecture_hours"],
            lab_hours=course_row["lab_hours"],
            prerequisites=prereqs,
            course_description=course_row["course_description"]
        )

        # 2. Fetch Course Learning Outcomes
        cursor.execute("SELECT * FROM course_outcomes WHERE course_id = ? ORDER BY clo_id ASC;", (course_id,))
        clo_rows = cursor.fetchall()
        course_outcomes = []
        for r in clo_rows:
            try:
                pos = json.loads(r["program_outcomes_mapped"])
            except Exception:
                pos = [r["program_outcomes_mapped"]]
            course_outcomes.append(
                CourseOutcomeSchema(
                    clo_id=r["clo_id"],
                    description=r["description"],
                    bloom_level=r["bloom_level"],
                    program_outcomes_mapped=pos
                )
            )

        # 3. Fetch Weekly Schedules & nested LLOs
        cursor.execute("SELECT * FROM weekly_schedules WHERE course_id = ? ORDER BY week_number ASC;", (course_id,))
        sched_rows = cursor.fetchall()
        weekly_schedule = []
        for s in sched_rows:
            sched_id = s["id"]
            try:
                topics = json.loads(s["topics"])
            except Exception:
                topics = s["topics"]

            try:
                tlas = json.loads(s["teaching_learning_activities"])
            except Exception:
                tlas = [s["teaching_learning_activities"]]

            try:
                tasks = json.loads(s["assessment_tasks"])
            except Exception:
                tasks = [s["assessment_tasks"]]

            try:
                resources = json.loads(s["resources"])
            except Exception:
                resources = [s["resources"]]

            # Fetch LLOs for this week
            cursor.execute("SELECT * FROM lesson_outcomes WHERE schedule_id = ? ORDER BY id ASC;", (sched_id,))
            llo_rows = cursor.fetchall()
            llos = [
                LessonOutcomeSchema(
                    llo_id=l["llo_id"],
                    description=l["description"],
                    domain=l["domain"]
                )
                for l in llo_rows
            ]

            weekly_schedule.append(
                WeeklyScheduleSchema(
                    week_number=s["week_number"],
                    topics=topics,
                    lesson_outcomes=llos,
                    teaching_learning_activities=tlas,
                    assessment_tasks=tasks,
                    resources=resources
                )
            )

    return FullSyllabusSchema(
        course_metadata=metadata,
        course_outcomes=course_outcomes,
        weekly_schedule=weekly_schedule
    )


def update_clo(clo_id: str, new_description: str, course_code: Optional[str] = None, db_path: str = DEFAULT_DB_PATH) -> bool:
    """
    Allows faculty human-in-the-loop editing of a Course Learning Outcome.
    Validates the new description using CourseOutcomeSchema's Bloom verb rules before updating.
    """
    # Defensive validation: verify the new description doesn't violate Bloom's verbs
    try:
        CourseOutcomeSchema.reject_unmeasurable_verbs(new_description)
    except ValueError as val_err:
        print(f"[-] Rejection: Proposed CLO edit violates Bloom's taxonomy: {val_err}")
        return False

    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        if course_code:
            cursor.execute(
                """
                UPDATE course_outcomes
                SET description = ?
                WHERE clo_id = ? AND course_id = (SELECT id FROM courses WHERE course_code = ?);
                """,
                (new_description, clo_id, course_code)
            )
        else:
            cursor.execute(
                """
                UPDATE course_outcomes
                SET description = ?
                WHERE clo_id = ?;
                """,
                (new_description, clo_id)
            )
        affected = cursor.rowcount
        conn.commit()

    if affected > 0:
        target_info = f" for {course_code}" if course_code else ""
        print(f"[+] Successfully updated {clo_id}{target_info} in SQLite database.")
        return True
    print(f"[-] CLO '{clo_id}' not found.")
    return False


# =============================================================================
# CLI TEST FIXTURE
# =============================================================================

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="OBE Syllabus SQLite Relational Database Manager")
    parser.add_argument("--db", default=DEFAULT_DB_PATH, help="Path to SQLite database file")
    parser.add_argument("--file", default="", help="Path to syllabus JSON deliverable to ingest")
    parser.add_argument("--update-clo-id", default="", help="CLO ID to update (e.g. CLO1)")
    parser.add_argument("--new-desc", default="", help="New Bloom-compliant description for CLO")
    parser.add_argument("--course", default="", help="Target course code")
    args = parser.parse_args()

    target_db = args.db
    print(f"[*] Initializing relational database at '{target_db}'...")
    init_db(target_db)

    # Ingest syllabus file if provided or auto-detect in outputs/
    candidate_files = []
    if args.file:
        candidate_files.append(Path(args.file))
    else:
        outputs_dir = BASE_DIR / "outputs"
        if outputs_dir.exists():
            candidate_files.extend(list(outputs_dir.glob("sample_validated_output*.json")))
        if (BASE_DIR / "sample_validated_output.json").exists():
            candidate_files.append(BASE_DIR / "sample_validated_output.json")

    ingested_any = False
    for s_file in candidate_files:
        if s_file.exists():
            try:
                with open(s_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "course_metadata" in data and "weekly_schedule" in data:
                        syllabus_obj = FullSyllabusSchema(**data)
                        cid = save_syllabus(syllabus_obj, db_path=target_db)
                        print(f"[+] Ingested '{s_file.name}' -> Course ID: {cid} ({syllabus_obj.course_metadata.course_code})")
                        ingested_any = True
            except Exception as e:
                print(f"[-] Warning ingesting '{s_file}': {e}")

    # Display database courses
    with get_connection(target_db) as conn:
        rows = conn.execute("SELECT id, course_code, course_title FROM courses").fetchall()
        print(f"[+] Total courses registered in database: {len(rows)}")
        for r in rows:
            w_count = conn.execute("SELECT COUNT(*) FROM weekly_schedules WHERE course_id = ?", (r["id"],)).fetchone()[0]
            c_count = conn.execute("SELECT COUNT(*) FROM course_outcomes WHERE course_id = ?", (r["id"],)).fetchone()[0]
            print(f"    - [{r['id']}] {r['course_code']} - {r['course_title']} ({w_count} weeks, {c_count} CLOs)")

    # Human-in-the-loop update test or user request
    if args.update_clo_id and args.new_desc:
        updated = update_clo(args.update_clo_id, args.new_desc, course_code=args.course, db_path=target_db)
        print(f"[+] Manual CLO update status: {updated}")
    elif ingested_any:
        # Perform human-in-the-loop verification on CLO1
        updated = update_clo("CLO1", "Formulate and optimize time and space complexity models.", db_path=target_db)
        print(f"[+] Human-in-the-loop rubric demonstration update status: {updated}")
