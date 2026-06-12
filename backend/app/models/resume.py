from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from backend.app.db.base import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    version = Column(Integer, default=1)
    file_path = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    parsed_content = Column(Text, nullable=True)
    is_base = Column(Integer, default=1)  # 1 = base resume, 0 = customized

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="resumes")
