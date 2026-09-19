-- =============================================================================
-- schema.sql: UPHSD CCS Outcome-Based Education (OBE) Relational Database Schema
-- 
-- Authors:
--   - Christian Ezekiel L. Carvajal (Lead Architect & Systems Engineer)
--   - John Miko P. Sarsalijo (Collaborative Partner & Systems Engineer)
--
-- Institution: College of Computer Studies, University of Perpetual Help System DALTA
-- Course: BSCS 3112 / Artificial Intelligence (Lesson 5 - Midterm Mini-Project)
-- Evaluator: Prof. Roberto L. Malitao
-- Target DB: SQLite 3 (obe_syllabus.db)
-- =============================================================================

PRAGMA foreign_keys = ON;

-- 1. Courses Metadata Table
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_code TEXT NOT NULL UNIQUE,
    course_title TEXT NOT NULL,
    credit_units INTEGER NOT NULL DEFAULT 3,
    lecture_hours INTEGER NOT NULL DEFAULT 2,
    lab_hours INTEGER NOT NULL DEFAULT 3,
    prerequisites TEXT NOT NULL DEFAULT 'None',
    course_description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Course Learning Outcomes (CLOs) Table
CREATE TABLE IF NOT EXISTS course_outcomes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    clo_id TEXT NOT NULL,
    description TEXT NOT NULL,
    bloom_level TEXT NOT NULL,
    program_outcomes_mapped TEXT NOT NULL, -- Stored as JSON array or comma-separated string
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE,
    UNIQUE(course_id, clo_id)
);

-- 3. Weekly Schedules Table (18-Week Academic Matrix)
CREATE TABLE IF NOT EXISTS weekly_schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    week_number INTEGER NOT NULL CHECK (week_number BETWEEN 1 AND 18),
    topics TEXT NOT NULL, -- JSON array or newline-delimited text
    teaching_learning_activities TEXT NOT NULL, -- JSON array
    assessment_tasks TEXT NOT NULL, -- JSON array
    resources TEXT NOT NULL, -- JSON array
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE,
    UNIQUE(course_id, week_number)
);

-- 4. Lesson Learning Outcomes (LLOs) Table with Tripartite K/S/A Domains
CREATE TABLE IF NOT EXISTS lesson_outcomes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    schedule_id INTEGER NOT NULL,
    llo_id TEXT NOT NULL,
    description TEXT NOT NULL,
    domain TEXT NOT NULL CHECK (domain IN ('K', 'S', 'A')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (schedule_id) REFERENCES weekly_schedules (id) ON DELETE CASCADE
);

-- Indexes for high-speed relational queries
CREATE INDEX IF NOT EXISTS idx_courses_code ON courses (course_code);
CREATE INDEX IF NOT EXISTS idx_clo_course ON course_outcomes (course_id);
CREATE INDEX IF NOT EXISTS idx_sched_course ON weekly_schedules (course_id);
CREATE INDEX IF NOT EXISTS idx_llo_sched ON lesson_outcomes (schedule_id);
