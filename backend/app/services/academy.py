import json
from datetime import datetime, timezone

import copy

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.data.academy_content import ACADEMY_COURSES
from app.models.academy import Course, Lesson, UserEnrollment, UserLessonProgress
from app.schemas.academy import (
    CourseDetail,
    CourseSummary,
    EnrollmentResponse,
    LessonDetail,
    LessonSummary,
    UserLearningSummary,
)


class AcademyService:
    @staticmethod
    async def seed_content(db: AsyncSession) -> None:
        result = await db.execute(select(func.count()).select_from(Course))
        if result.scalar_one() == 0:
            for course_data in copy.deepcopy(ACADEMY_COURSES):
                lessons_data = course_data.pop("lessons")
                course = Course(**course_data)
                db.add(course)
                await db.flush()

                for lesson_data in lessons_data:
                    lesson = Lesson(course_id=course.id, **lesson_data)
                    db.add(lesson)

            await db.commit()
            return

        await AcademyService._sync_lesson_material(db)

    @staticmethod
    async def _sync_lesson_material(db: AsyncSession) -> None:
        """Actualiza contenido/quiz/visual de lecciones existentes sin romper progreso."""
        course_result = await db.execute(select(Course).options(selectinload(Course.lessons)))
        courses_by_slug = {course.slug: course for course in course_result.scalars().all()}
        changed = False

        for course_data in copy.deepcopy(ACADEMY_COURSES):
            course = courses_by_slug.get(course_data["slug"])
            if course is None:
                continue

            course.title = course_data["title"]
            course.description = course_data["description"]
            course.category = course_data["category"]
            course.difficulty = course_data["difficulty"]
            course.estimated_hours = course_data["estimated_hours"]
            course.disclaimer = course_data.get("disclaimer")
            course.order_index = course_data["order_index"]
            db.add(course)

            lessons_by_slug = {lesson.slug: lesson for lesson in course.lessons}
            for lesson_data in course_data["lessons"]:
                lesson = lessons_by_slug.get(lesson_data["slug"])
                if lesson is None:
                    lesson = Lesson(course_id=course.id, **lesson_data)
                    db.add(lesson)
                    changed = True
                    continue

                for field in (
                    "title",
                    "content",
                    "visual_type",
                    "visual_data",
                    "quiz",
                    "order_index",
                    "duration_minutes",
                ):
                    if getattr(lesson, field) != lesson_data.get(field):
                        setattr(lesson, field, lesson_data.get(field))
                        changed = True
                db.add(lesson)

        if changed:
            await db.commit()

    @staticmethod
    async def _get_progress_map(
        db: AsyncSession, user_id: int, course_id: int
    ) -> dict[int, UserLessonProgress]:
        result = await db.execute(
            select(UserLessonProgress)
            .join(Lesson)
            .where(UserLessonProgress.user_id == user_id, Lesson.course_id == course_id)
        )
        return {record.lesson_id: record for record in result.scalars().all()}

    @staticmethod
    async def _get_enrollment(
        db: AsyncSession, user_id: int, course_id: int
    ) -> UserEnrollment | None:
        result = await db.execute(
            select(UserEnrollment).where(
                UserEnrollment.user_id == user_id,
                UserEnrollment.course_id == course_id,
            )
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def _recalculate_progress(
        db: AsyncSession, user_id: int, course_id: int
    ) -> float:
        lessons_result = await db.execute(
            select(func.count()).select_from(Lesson).where(Lesson.course_id == course_id)
        )
        total_lessons = lessons_result.scalar_one()
        if total_lessons == 0:
            return 0.0

        completed_result = await db.execute(
            select(func.count())
            .select_from(UserLessonProgress)
            .join(Lesson)
            .where(
                UserLessonProgress.user_id == user_id,
                Lesson.course_id == course_id,
                UserLessonProgress.status == "completed",
            )
        )
        completed = completed_result.scalar_one()
        percent = round((completed / total_lessons) * 100, 1)

        enrollment = await AcademyService._get_enrollment(db, user_id, course_id)
        if enrollment:
            enrollment.progress_percent = percent
            db.add(enrollment)
            await db.commit()

        return percent

    @staticmethod
    async def list_courses(
        db: AsyncSession, user_id: int | None = None
    ) -> list[CourseSummary]:
        await AcademyService.seed_content(db)

        result = await db.execute(
            select(Course)
            .where(Course.is_published == 1)
            .options(selectinload(Course.lessons))
            .order_by(Course.order_index)
        )
        courses = result.scalars().all()
        summaries: list[CourseSummary] = []

        for course in courses:
            enrollment = None
            if user_id:
                enrollment = await AcademyService._get_enrollment(db, user_id, course.id)

            summaries.append(
                CourseSummary(
                    id=course.id,
                    slug=course.slug,
                    title=course.title,
                    description=course.description,
                    category=course.category,
                    difficulty=course.difficulty,
                    estimated_hours=course.estimated_hours,
                    lesson_count=len(course.lessons),
                    progress_percent=enrollment.progress_percent if enrollment else None,
                    is_enrolled=enrollment is not None,
                )
            )

        return summaries

    @staticmethod
    async def get_course(
        db: AsyncSession, slug: str, user_id: int | None = None
    ) -> CourseDetail | None:
        await AcademyService.seed_content(db)

        result = await db.execute(
            select(Course)
            .where(Course.slug == slug, Course.is_published == 1)
            .options(selectinload(Course.lessons))
        )
        course = result.scalar_one_or_none()
        if not course:
            return None

        progress_map: dict[int, UserLessonProgress] = {}
        enrollment = None
        if user_id:
            progress_map = await AcademyService._get_progress_map(db, user_id, course.id)
            enrollment = await AcademyService._get_enrollment(db, user_id, course.id)

        lessons = [
            LessonSummary(
                id=lesson.id,
                slug=lesson.slug,
                title=lesson.title,
                order_index=lesson.order_index,
                duration_minutes=lesson.duration_minutes,
                visual_type=lesson.visual_type,
                status=progress_map.get(lesson.id).status if lesson.id in progress_map else None,
            )
            for lesson in sorted(course.lessons, key=lambda item: item.order_index)
        ]

        return CourseDetail(
            id=course.id,
            slug=course.slug,
            title=course.title,
            description=course.description,
            category=course.category,
            difficulty=course.difficulty,
            estimated_hours=course.estimated_hours,
            disclaimer=course.disclaimer,
            lessons=lessons,
            progress_percent=enrollment.progress_percent if enrollment else None,
            is_enrolled=enrollment is not None,
        )

    @staticmethod
    async def get_lesson(
        db: AsyncSession, course_slug: str, lesson_slug: str, user_id: int | None = None
    ) -> LessonDetail | None:
        await AcademyService.seed_content(db)

        result = await db.execute(
            select(Lesson)
            .join(Course)
            .where(Course.slug == course_slug, Lesson.slug == lesson_slug)
            .options(selectinload(Lesson.course))
        )
        lesson = result.scalar_one_or_none()
        if not lesson:
            return None

        status = None
        quiz_score = None
        if user_id:
            progress_result = await db.execute(
                select(UserLessonProgress).where(
                    UserLessonProgress.user_id == user_id,
                    UserLessonProgress.lesson_id == lesson.id,
                )
            )
            progress = progress_result.scalar_one_or_none()
            if progress:
                status = progress.status
                quiz_score = progress.quiz_score

        visual_data = json.loads(lesson.visual_data) if lesson.visual_data else None
        quiz = json.loads(lesson.quiz) if lesson.quiz else None

        return LessonDetail(
            id=lesson.id,
            slug=lesson.slug,
            title=lesson.title,
            content_type=lesson.content_type,
            content=lesson.content,
            visual_type=lesson.visual_type,
            visual_data=visual_data,
            quiz=quiz,
            duration_minutes=lesson.duration_minutes,
            course_slug=lesson.course.slug,
            course_title=lesson.course.title,
            status=status,
            quiz_score=quiz_score,
        )

    @staticmethod
    async def enroll(
        db: AsyncSession, user_id: int, course_slug: str
    ) -> EnrollmentResponse | None:
        await AcademyService.seed_content(db)

        result = await db.execute(select(Course).where(Course.slug == course_slug))
        course = result.scalar_one_or_none()
        if not course:
            return None

        existing = await AcademyService._get_enrollment(db, user_id, course.id)
        if existing:
            return EnrollmentResponse(
                course_slug=course.slug,
                progress_percent=existing.progress_percent,
                enrolled_at=existing.enrolled_at,
            )

        enrollment = UserEnrollment(user_id=user_id, course_id=course.id)
        db.add(enrollment)
        await db.commit()
        await db.refresh(enrollment)

        return EnrollmentResponse(
            course_slug=course.slug,
            progress_percent=enrollment.progress_percent,
            enrolled_at=enrollment.enrolled_at,
        )

    @staticmethod
    async def update_lesson_progress(
        db: AsyncSession,
        user_id: int,
        lesson_id: int,
        status: str,
        quiz_score: float | None = None,
        time_spent_seconds: int | None = None,
    ) -> LessonDetail | None:
        lesson_result = await db.execute(
            select(Lesson)
            .where(Lesson.id == lesson_id)
            .options(selectinload(Lesson.course))
        )
        lesson = lesson_result.scalar_one_or_none()
        if not lesson:
            return None

        enrollment = await AcademyService._get_enrollment(db, user_id, lesson.course_id)
        if not enrollment:
            enrollment = UserEnrollment(user_id=user_id, course_id=lesson.course_id)
            db.add(enrollment)
            await db.flush()

        progress_result = await db.execute(
            select(UserLessonProgress).where(
                UserLessonProgress.user_id == user_id,
                UserLessonProgress.lesson_id == lesson_id,
            )
        )
        progress = progress_result.scalar_one_or_none()

        if not progress:
            progress = UserLessonProgress(user_id=user_id, lesson_id=lesson_id)
            db.add(progress)

        if status == "completed" and lesson.quiz and quiz_score is not None:
            quiz_data = json.loads(lesson.quiz)
            passing_score = quiz_data.get("passing_score", 70)
            if quiz_score < passing_score:
                raise ValueError(
                    f"Quiz score {quiz_score}% is below passing score {passing_score}%"
                )

        progress.status = status
        if quiz_score is not None:
            progress.quiz_score = quiz_score
        if time_spent_seconds is not None:
            progress.time_spent_seconds = time_spent_seconds
        if status == "completed":
            progress.completed_at = datetime.now(timezone.utc)

        await db.commit()
        await AcademyService._recalculate_progress(db, user_id, lesson.course_id)

        return await AcademyService.get_lesson(
            db, lesson.course.slug, lesson.slug, user_id
        )

    @staticmethod
    async def get_user_learning(
        db: AsyncSession, user_id: int
    ) -> UserLearningSummary:
        await AcademyService.seed_content(db)

        courses = await AcademyService.list_courses(db, user_id)
        enrolled = [course for course in courses if course.is_enrolled]

        total_lessons_result = await db.execute(select(func.count()).select_from(Lesson))
        total_lessons = total_lessons_result.scalar_one()

        completed_result = await db.execute(
            select(func.count())
            .select_from(UserLessonProgress)
            .where(
                UserLessonProgress.user_id == user_id,
                UserLessonProgress.status == "completed",
            )
        )
        completed_lessons = completed_result.scalar_one()

        overall = 0.0
        if enrolled:
            overall = round(
                sum(course.progress_percent or 0 for course in enrolled) / len(enrolled),
                1,
            )

        return UserLearningSummary(
            enrolled_courses=len(enrolled),
            completed_lessons=completed_lessons,
            total_lessons=total_lessons,
            overall_progress_percent=overall,
            courses=enrolled,
        )
