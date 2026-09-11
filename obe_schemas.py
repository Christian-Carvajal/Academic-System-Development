"""
obe_schemas.py
Pydantic data models for UPHSD CCS Outcome-Based Education (OBE) Syllabi.
"""
from typing import List, Literal
from pydantic import BaseModel, Field, field_validator


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

    @field_validator("co_description")
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
    week_number: int = Field(..., ge=1, le=14, description="Week number from 1 to 14")
    period: Literal["PRELIM", "MIDTERM", "FINAL"] = Field(
        ..., description="Academic term period"
    )
    topic: str = Field(..., description="Main subject topic covered this week")
    llos: List[LessonLearningOutcome] = Field(
        ..., min_items=3, max_items=3, description="Tripartite outcomes: exactly one K, one S, and one A"
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
    weekly_schedule: List[WeeklyScheduleItem] = Field(
        ..., min_items=14, max_items=14, description="Strict 14-week schedule"
    )
    grading_breakdown: GradingBreakdown = Field(default_factory=GradingBreakdown)
