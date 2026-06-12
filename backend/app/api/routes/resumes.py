from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.core.dependencies import get_current_user
from backend.app.db.session import get_db
from backend.app.models.user import User
from backend.app.schemas.resume import ResumeOptimize, ResumeResponse
from backend.app.services.resume_service import ResumeService

router = APIRouter(prefix="/resumes", tags=["Resume Management"])


@router.post("/upload", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    allowed_extensions = {".pdf", ".txt", ".doc", ".docx"}
    ext = "." + file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="File type not supported")

    if file.size and file.size > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large")

    service = ResumeService(db)
    resume = await service.upload_resume(current_user.id, file)
    return resume


@router.get("/", response_model=list[ResumeResponse])
def list_resumes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ResumeService(db)
    return service.get_user_resumes(current_user.id)


@router.post("/optimize", response_model=ResumeResponse)
async def optimize_resume(
    data: ResumeOptimize,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ResumeService(db)
    result = await service.optimize_resume(
        current_user.id, data.job_title, data.job_description
    )
    if not result:
        raise HTTPException(status_code=404, detail="No base resume found. Upload one first.")
    return result
