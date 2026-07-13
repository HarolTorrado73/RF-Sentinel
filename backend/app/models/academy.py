from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Course(Base):
    __tablename__ = "academy_courses"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50), nullable=False)
    difficulty = Column(String(20), default="beginner")
    estimated_hours = Column(Float, default=1.0)
    disclaimer = Column(Text)
    order_index = Column(Integer, default=0)
    is_published = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    lessons = relationship(
        "Lesson",
        back_populates="course",
        order_by="Lesson.order_index",
        cascade="all, delete-orphan",
    )
    enrollments = relationship("UserEnrollment", back_populates="course")


class Lesson(Base):
    __tablename__ = "academy_lessons"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("academy_courses.id"), nullable=False)
    slug = Column(String(100), nullable=False)
    title = Column(String(255), nullable=False)
    content_type = Column(String(30), default="markdown")
    content = Column(Text, nullable=False)
    visual_type = Column(String(30), default="none")
    visual_data = Column(Text)
    quiz = Column(Text)
    order_index = Column(Integer, default=0)
    duration_minutes = Column(Integer, default=10)

    course = relationship("Course", back_populates="lessons")
    progress_records = relationship("UserLessonProgress", back_populates="lesson")

    __table_args__ = (UniqueConstraint("course_id", "slug", name="uq_course_lesson_slug"),)


class UserEnrollment(Base):
    __tablename__ = "academy_enrollments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("academy_courses.id"), nullable=False)
    progress_percent = Column(Float, default=0.0)
    enrolled_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="academy_enrollments")
    course = relationship("Course", back_populates="enrollments")

    __table_args__ = (UniqueConstraint("user_id", "course_id", name="uq_user_course_enrollment"),)


class UserLessonProgress(Base):
    __tablename__ = "academy_lesson_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("academy_lessons.id"), nullable=False)
    status = Column(String(20), default="not_started")
    quiz_score = Column(Float)
    time_spent_seconds = Column(Integer, default=0)
    completed_at = Column(DateTime(timezone=True))

    user = relationship("User", back_populates="lesson_progress")
    lesson = relationship("Lesson", back_populates="progress_records")

    __table_args__ = (UniqueConstraint("user_id", "lesson_id", name="uq_user_lesson_progress"),)
