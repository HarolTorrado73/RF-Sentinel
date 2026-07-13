from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db, get_optional_user
from app.schemas.academy import (
    CourseDetail,
    CourseSummary,
    EnrollmentResponse,
    LessonDetail,
    LessonProgressUpdate,
    UserLearningSummary,
)
from app.schemas.user import User
from app.services.academy import AcademyService

router = APIRouter()


@router.get("/courses", response_model=list[CourseSummary])
async def list_courses(
    db: AsyncSession = Depends(get_db),
    current_user: User | None = Depends(get_optional_user),
):
    user_id = current_user.id if current_user else None
    return await AcademyService.list_courses(db, user_id)


@router.get("/courses/{slug}", response_model=CourseDetail)
async def get_course(
    slug: str,
    db: AsyncSession = Depends(get_db),
    current_user: User | None = Depends(get_optional_user),
):
    user_id = current_user.id if current_user else None
    course = await AcademyService.get_course(db, slug, user_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.get("/courses/{slug}/lessons/{lesson_slug}", response_model=LessonDetail)
async def get_lesson(
    slug: str,
    lesson_slug: str,
    db: AsyncSession = Depends(get_db),
    current_user: User | None = Depends(get_optional_user),
):
    user_id = current_user.id if current_user else None
    lesson = await AcademyService.get_lesson(db, slug, lesson_slug, user_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


@router.post("/courses/{slug}/enroll", response_model=EnrollmentResponse)
async def enroll_course(
    slug: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    enrollment = await AcademyService.enroll(db, current_user.id, slug)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Course not found")
    return enrollment


@router.put("/lessons/{lesson_id}/progress", response_model=LessonDetail)
async def update_lesson_progress(
    lesson_id: int,
    progress_in: LessonProgressUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        lesson = await AcademyService.update_lesson_progress(
            db,
            current_user.id,
            lesson_id,
            progress_in.status,
            progress_in.quiz_score,
            progress_in.time_spent_seconds,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


@router.get("/me/learning", response_model=UserLearningSummary)
async def get_my_learning(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await AcademyService.get_user_learning(db, current_user.id)
