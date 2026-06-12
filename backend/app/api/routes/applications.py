from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.core.dependencies import get_current_user
from backend.app.db.session import get_db
from backend.app.models.user import User
from backend.app.schemas.application import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationStatusUpdate,
    DashboardStats,
)
from backend.app.services.application_service import ApplicationService

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.post("/apply", response_model=ApplicationResponse)
async def apply_to_job(
    data: ApplicationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ApplicationService(db)
    try:
        application = await service.apply_to_job(current_user, data.job_id)
        return application
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[ApplicationResponse])
def list_applications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ApplicationService(db)
    return service.get_user_applications(current_user.id)


@router.get("/dashboard", response_model=DashboardStats)
def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ApplicationService(db)
    return service.get_dashboard_stats(current_user.id)


@router.put("/{application_id}/status", response_model=ApplicationResponse)
def update_application_status(
    application_id: int,
    data: ApplicationStatusUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ApplicationService(db)
    try:
        return service.update_status(application_id, current_user.id, data.status, data.notes)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
