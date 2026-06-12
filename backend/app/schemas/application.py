from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ApplicationCreate(BaseModel):
    job_id: int


class ApplicationResponse(BaseModel):
    id: int
    user_id: int
    job_id: int
    resume_id: int | None = None
    match_score: float | None = None
    cover_letter: str | None = None
    status: str
    applied_at: datetime | None = None
    notes: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ApplicationStatusUpdate(BaseModel):
    status: str
    notes: str | None = None


class DashboardStats(BaseModel):
    total_applications: int
    pending: int
    applied: int
    interviews: int
    rejections: int
    offers: int
