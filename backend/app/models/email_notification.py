from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from backend.app.db.base import Base


class EmailNotification(Base):
    __tablename__ = "email_notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=True)
    subject = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    email_type = Column(String, nullable=False)  # confirmation, clarification, update
    sent_at = Column(DateTime, nullable=True)
    status = Column(String, default="pending")  # pending, sent, failed

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
