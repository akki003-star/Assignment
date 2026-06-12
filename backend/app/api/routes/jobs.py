from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.core.dependencies import get_current_user
from backend.app.db.session import get_db
from backend.app.models.user import User
from backend.app.schemas.job import JobResponse, JobSearch
from backend.app.services.ai_service import AIService
from backend.app.services.job_service import JobService

router = APIRouter(prefix="/jobs", tags=["Job Search"])


@router.post("/search", response_model=list[JobResponse])
def search_jobs(
    search: JobSearch,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = JobService(db)
    return service.search_jobs(search)


@router.get("/{job_id}", response_model=JobResponse)
def get_job(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = JobService(db)
    job = service.get_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.get("/{job_id}/match-score")
async def get_match_score(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = JobService(db)
    job = service.get_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    ai_service = AIService()
    result = await ai_service.calculate_match_score(
        user_skills=current_user.skills or [],
        job_requirements=job.requirements or [],
        job_description=job.description or "",
    )
    return result
