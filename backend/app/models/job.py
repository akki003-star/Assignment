from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Integer, JSON, String, Text
from sqlalchemy.orm import relationship

from backend.app.db.base import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    company = Column(String, nullable=False)
    location = Column(String, nullable=True)
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    description = Column(Text, nullable=True)
    requirements = Column(JSON, default=[])
    url = Column(String, nullable=True)
    source = Column(String, nullable=True)
    posted_date = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    applications = relationship(
        "Application", back_populates="job", cascade="all, delete-orphan"
    )
