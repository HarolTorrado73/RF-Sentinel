from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship

from app.core.database import Base


class Scan(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    target_id = Column(Integer, ForeignKey("targets.id"))
    scan_type = Column(String(50), nullable=False)
    status = Column(String(50), default="pending")
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    created_by_id = Column(Integer, ForeignKey("users.id"))
    results = Column(JSON)
    error_message = Column(Text)

    target = relationship("Target", back_populates="scans")
    created_by = relationship("User", back_populates="scans")