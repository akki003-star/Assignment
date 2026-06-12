from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class JobSearch(BaseModel):
    keywords: list[str] = Field(default=[], max_length=20)
    location: str | None = Field(None, max_length=200)
    salary_min: float | None = Field(None, ge=0)
    salary_max: float | None = Field(None, ge=0)
    source: str | None = Field(None, max_length=100)


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
