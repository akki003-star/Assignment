from datetime import datetime

from pydantic import BaseModel, ConfigDict


class JobSearch(BaseModel):
    keywords: list[str] = []
    location: str | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    source: str | None = None


class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    location: str | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    description: str | None = None
    requirements: list[str] = []
    url: str | None = None
    source: str | None = None
    posted_date: datetime | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
