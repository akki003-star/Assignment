from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, JSON, String
from sqlalchemy.orm import relationship

from backend.app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    # Profile fields
    phone = Column(String, nullable=True)
    education = Column(String, nullable=True)
    skills = Column(JSON, default=[])
    experience_years = Column(Integer, default=0)
    preferred_locations = Column(JSON, default=[])
    expected_salary = Column(Float, nullable=True)
    preferred_roles = Column(JSON, default=[])

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    resumes = relationship("Resume", back_populates="user", cascade="all, delete-orphan")
    applications = relationship(
        "Application", back_populates="user", cascade="all, delete-orphan"
    )
