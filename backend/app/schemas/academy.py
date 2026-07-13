from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class LessonSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    title: str
    order_index: int
    duration_minutes: int
    visual_type: str
    status: str | None = None


class CourseSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    title: str
    description: str
    category: str
    difficulty: str
    estimated_hours: float
    lesson_count: int = 0
    progress_percent: float | None = None
    is_enrolled: bool = False


class CourseDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    title: str
    description: str
    category: str
    difficulty: str
    estimated_hours: float
    disclaimer: str | None = None
    lessons: list[LessonSummary] = []
    progress_percent: float | None = None
    is_enrolled: bool = False


class LessonDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    title: str
    content_type: str
    content: str
    visual_type: str
    visual_data: dict | None = None
    quiz: dict | None = None
    duration_minutes: int
    course_slug: str
    course_title: str
    status: str | None = None
    quiz_score: float | None = None


class EnrollmentResponse(BaseModel):
    course_slug: str
    progress_percent: float
    enrolled_at: datetime


class LessonProgressUpdate(BaseModel):
    status: str = Field(..., pattern="^(in_progress|completed)$")
    quiz_score: float | None = Field(default=None, ge=0, le=100)
    time_spent_seconds: int | None = Field(default=None, ge=0)


class UserLearningSummary(BaseModel):
    enrolled_courses: int
    completed_lessons: int
    total_lessons: int
    overall_progress_percent: float
    courses: list[CourseSummary]
