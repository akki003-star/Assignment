from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ResumeResponse(BaseModel):
    id: int
    user_id: int
    version: int
    file_name: str
    parsed_content: str | None = None
    is_base: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ResumeOptimize(BaseModel):
    job_title: str
    job_description: str
