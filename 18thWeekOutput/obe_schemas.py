"""
obe_schemas.py
Pydantic v2 Data Contracts for UPHSD CCS Outcome-Based Education (OBE) Syllabi.

Authors:
- Christian Ezekiel L. Carvajal (Lead Architect & Systems Engineer)
- John Miko P. Sarsalijo (Collaborative Partner & Systems Engineer)

Institution: College of Computer Studies, University of Perpetual Help System DALTA (Molino Campus)
Course: BSCS 3112 / Artificial Intelligence (Lesson 5 - Midterm Mini-Project)
Instructor: Prof. Roberto L. Malitao
"""
from typing import List, Literal, Union, Optional
from pydantic import BaseModel, Field, field_validator, model_validator


# =============================================================================
# MILESTONE 1 OFFICIAL OBE PYDANTIC SCHEMAS (18-WEEK INSTITUTIONAL CONTRACT)
# =============================================================================

class CourseMetadataSchema(BaseModel):
    """Catalog metadata defining the institutional subject parameters."""
    course_code: str = Field(..., description="Subject code, e.g., 'CS 3110' or 'CCS 3101'")
    course_title: str = Field(..., description="Full descriptive course title")
    credit_units: int = Field(default=3, ge=1, le=6, description="Total academic credit units")
    lecture_hours: int = Field(default=2, ge=0, le=6, description="Weekly lecture contact hours")
    lab_hours: int = Field(default=3, ge=0, le=6, description="Weekly laboratory contact hours")
    prerequisites: Union[str, List[str]] = Field(
        default="None", description="Prerequisite course code(s) or 'None'"
    )
    course_description: str = Field(..., description="Official catalog course description")


class CourseOutcomeSchema(BaseModel):
    """
    Course Learning Outcome (CLO).
    Must begin with a measurable Bloom's Taxonomy cognitive action verb.
    """
    clo_id: str = Field(..., description="Identifier, e.g., 'CLO1', 'CLO2'")
    description: str = Field(
        ..., description="Measurable outcome statement starting with an active Bloom's verb"
    )
    bloom_level: str = Field(
        ..., description="Bloom's Taxonomy Cognitive Level (Remember, Understand, Apply, Analyze, Evaluate, Create)"
    )
    program_outcomes_mapped: List[str] = Field(
        ..., min_items=1, description="Mapped Program Outcomes (e.g., ['PLO1', 'PLO2'])"
    )

    @field_validator("bloom_level", mode="before")
    @classmethod
    def normalize_bloom_level(cls, v: str) -> str:
        if not isinstance(v, str):
            return v
        v_clean = v.strip().capitalize()
        synonyms = {
            "Design": "Create",
            "Develop": "Create",
            "Synthesize": "Create",
            "Integrating": "Create",
            "Integrate": "Create",
            "Build": "Create",
            "Construct": "Create",
            "Formulate": "Create",
            "Analysis": "Analyze",
            "Analyzing": "Analyze",
            "Application": "Apply",
            "Applying": "Apply",
            "Implementation": "Apply",
            "Implement": "Apply",
            "Evaluation": "Evaluate",
            "Evaluating": "Evaluate",
            "Assess": "Evaluate",
            "Assessing": "Evaluate",
            "Comprehension": "Understand",
            "Understanding": "Understand",
            "Knowledge": "Remember",
            "Remembering": "Remember"
        }
        return synonyms.get(v_clean, v_clean)

    @field_validator("description")
    @classmethod
    def reject_unmeasurable_verbs(cls, value: str) -> str:
        banned = [
            "understand", "know", "learn", "study",
            "familiarize", "be familiar with", "be exposed to",
            "appreciate", "comprehend"
        ]
        val_lower = value.strip().lower()
        first_token = val_lower.split(" ")[0]
        
        for b in banned:
            if val_lower.startswith(b) or first_token == b:
                raise ValueError(
                    f"Banned non-measurable verb '{b}' detected in outcome statement. "
                    "Must begin with an active, measurable Bloom's Taxonomy action verb "
                    "(e.g., 'Analyze', 'Design', 'Evaluate', 'Implement', 'Develop')."
                )
        return value


class LessonOutcomeSchema(BaseModel):
    """
    Lesson Learning Outcome (LLO) categorized strictly across tripartite domains.
    K: Knowledge (Cognitive)
    S: Skills (Psychomotor)
    A: Attitude (Affective)
    """
    llo_id: str = Field(..., description="Outcome tag, e.g., 'LLO1.1' or 'LLO-K1'")
    description: str = Field(..., description="Action statement detailing the specific learning outcome")
    domain: Literal["K", "S", "A"] = Field(
        ..., description="Educational domain: 'K' for Knowledge, 'S' for Skills, 'A' for Attitude"
    )


class WeeklyScheduleSchema(BaseModel):
    """Weekly breakdown item across the institutional 18-week semester."""
    week_number: int = Field(..., ge=1, le=18, description="Week index (1 to 18)")
    topics: Union[List[str], str] = Field(..., description="Topics covered during the week")
    lesson_outcomes: List[LessonOutcomeSchema] = Field(
        ..., min_items=1, description="List of Lesson Learning Outcomes for this week"
    )
    teaching_learning_activities: List[str] = Field(
        ..., min_items=1, description="Hands-on TLAs, lectures, or interactive exercises"
    )
    assessment_tasks: List[str] = Field(
        ..., min_items=1, description="Assessment tools, e.g., Lab Rubric, Practical Exam, Quiz"
    )
    resources: List[str] = Field(
        default_factory=lambda: ["Textbook", "IDE", "LMS Portal"],
        description="Learning resources and references"
    )


class FullSyllabusSchema(BaseModel):
    """
    Root OBE Syllabus Model aggregating course metadata, 3-5 CLOs,
    and a strictly validated 18-week academic schedule.
    """
    course_metadata: CourseMetadataSchema
    course_outcomes: List[CourseOutcomeSchema] = Field(
        ..., min_items=3, max_items=5, description="3 to 5 Course Learning Outcomes (CLOs)"
    )
    weekly_schedule: List[WeeklyScheduleSchema] = Field(
        ..., min_items=18, max_items=18, description="Strict 18-week semester schedule"
    )

    @model_validator(mode="after")
    def validate_ksa_coverage_across_schedule(self) -> "FullSyllabusSchema":
        """Asserts that all three K/S/A educational domains are represented across the schedule."""
        domains_found = set()
        for week in self.weekly_schedule:
            for llo in week.lesson_outcomes:
                domains_found.add(llo.domain)
        
        required_domains = {"K", "S", "A"}
        missing_domains = required_domains - domains_found
        if missing_domains:
            raise ValueError(
                f"Syllabus weekly schedule lacks complete tripartite domain coverage. "
                f"Missing domains: {missing_domains}. Schedule must include Knowledge (K), "
                "Skills (S), and Attitude (A) outcomes across the 18 weeks."
            )
        return self


# =============================================================================
# BACKWARD-COMPATIBILITY ALIASES & MODELS (LESSON 4 LAB 1.1 / 1.2 WORKSPACE)
# =============================================================================

class CourseOutcome(BaseModel):
    clo_number: int = Field(..., ge=1, le=5, description="Course Outcome index (1 to 5)")
    bloom_level: Literal["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"] = Field(
        ..., description="Bloom's Taxonomy Cognitive Level"
    )
    co_description: str = Field(
        ..., description="Measurable outcome statement starting with an active Bloom's verb"
    )
    mapped_po: List[int] = Field(
        ..., min_items=1, description="Mapped Program Outcome (PO/PLO) indices"
    )

    @field_validator("bloom_level", mode="before")
    @classmethod
    def normalize_bloom_level(cls, v: str) -> str:
        return CourseOutcomeSchema.normalize_bloom_level(v)

    @field_validator("co_description")
    @classmethod
    def reject_unmeasurable_verbs(cls, value: str) -> str:
        banned = ["understand", "learn", "know", "be exposed to", "study"]
        first_word = value.strip().split(" ")[0].lower()
        for b in banned:
            if b in first_word:
                raise ValueError(f"Banned non-measurable verb '{b}' detected. Must use an active Bloom's verb.")
        return value


class CourseOutcomesPayload(BaseModel):
    course_title: str = Field(..., description="Full course name")
    course_code: str = Field(..., description="Subject code, e.g., CS 3110")
    course_description: str = Field(..., description="Catalogue description")
    course_outcomes: List[CourseOutcome] = Field(
        ..., min_items=4, max_items=5, description="Array of 4-5 measurable Course Outcomes"
    )


class LessonLearningOutcome(BaseModel):
    category: Literal["K", "S", "A"] = Field(
        ..., description="Category: K for Knowledge, S for Skills, A for Attitude"
    )
    outcome_text: str = Field(
        ..., description="Action statement starting with a Bloom's verb"
    )


class WeeklyScheduleItem(BaseModel):
    week_number: int = Field(..., ge=1, le=18, description="Week number from 1 to 18")
    period: Literal["PRELIM", "MIDTERM", "FINAL"] = Field(
        ..., description="Academic term period"
    )
    topic: str = Field(..., description="Main subject topic covered this week")
    llos: List[LessonLearningOutcome] = Field(
        ..., min_items=1, description="Lesson learning outcomes"
    )
    teaching_learning_activity: str = Field(
        ..., description="IT/CS hands-on lab exercise or active learning activity"
    )
    assessment_tool: str = Field(
        ..., description="Assessment strategy, e.g., Lab Rubric, Practical Exam, Quiz"
    )
    evidence: str = Field(
        ..., description="Student artifact, e.g., Executable Source Code, Git Repository"
    )
    aligned_co: List[int] = Field(
        ..., min_items=1, description="List of CLO numbers covered in this week"
    )


class GradingBreakdown(BaseModel):
    quizzes_pct: float = Field(default=30.0, description="Quiz weight (30%)")
    research_pct: float = Field(default=20.0, description="Research weight (20%)")
    seatwork_lab_pct: float = Field(default=50.0, description="Seatwork/Lab weight (50%)")
    class_standing_weight: float = Field(default=70.0, description="Class standing factor (70%)")
    major_exam_weight: float = Field(default=30.0, description="Major exam factor (30%)")


class FullSyllabusPayload(BaseModel):
    course_code: str
    course_title: str
    course_description: str
    course_outcomes: List[CourseOutcome]
    weekly_schedule: List[WeeklyScheduleItem]
    grading_breakdown: GradingBreakdown = Field(default_factory=GradingBreakdown)
