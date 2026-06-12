import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.models.application import Application, ApplicationStatus
from backend.app.models.job import Job
from backend.app.models.user import User
from backend.app.schemas.application import DashboardStats
from backend.app.services.ai_service import AIService
from backend.app.services.email_service import EmailService
from backend.app.services.resume_service import ResumeService


logger = logging.getLogger(__name__)


class ApplicationService:
    def __init__(self, db: Session):
        self.db = db
        self.ai_service = AIService()
        self.email_service = EmailService()
        self.resume_service = ResumeService(db)

    async def apply_to_job(self, user: User, job_id: int) -> Application:
        job = self.db.query(Job).filter(Job.id == job_id).first()
        if not job:
            raise ValueError("Job not found")

        # Check if already applied
        existing = (
            self.db.query(Application)
            .filter(Application.user_id == user.id, Application.job_id == job_id)
            .first()
        )
        if existing:
            raise ValueError("Already applied to this job")

        # Calculate match score
        match_result = await self.ai_service.calculate_match_score(
            user_skills=user.skills or [],
            job_requirements=job.requirements or [],
            job_description=job.description or "",
        )

        match_score = match_result.get("match_score", 0.0)

        # Check threshold
        if match_score < settings.MATCH_THRESHOLD:
            raise ValueError(
                f"Match score ({match_score:.0%}) is below threshold "
                f"({settings.MATCH_THRESHOLD:.0%}). Consider improving your profile."
            )

        # Generate cover letter
        cover_letter = await self.ai_service.generate_cover_letter(
            user_name=user.full_name,
            user_skills=user.skills or [],
            job_title=job.title,
            company=job.company,
        )

        # Get optimized resume
        resume = self.resume_service.get_latest_resume(user.id)

        application = Application(
            user_id=user.id,
            job_id=job_id,
            resume_id=resume.id if resume else None,
            match_score=match_score,
            cover_letter=cover_letter,
            status="applied",
            applied_at=datetime.now(timezone.utc),
        )
        self.db.add(application)
        self.db.commit()
        self.db.refresh(application)

        # Add status entry
        status_entry = ApplicationStatus(
            application_id=application.id,
            status="applied",
            notes=f"Auto-applied with {match_score:.0%} match score",
        )
        self.db.add(status_entry)
        self.db.commit()

        # Send confirmation email (non-critical; log failure but don't block the application)
        email_sent = await self.email_service.send_application_confirmation(
            to_email=user.email,
            user_name=user.full_name,
            job_title=job.title,
            company=job.company,
        )
        if not email_sent:
            logger.warning(
                "Confirmation email failed for application %s (user=%s, job=%s)",
                application.id,
                user.email,
                job.title,
            )

        return application

    def get_user_applications(self, user_id: int) -> list[Application]:
        return (
            self.db.query(Application)
            .filter(Application.user_id == user_id)
            .order_by(Application.created_at.desc())
            .all()
        )

    def get_dashboard_stats(self, user_id: int) -> DashboardStats:
        applications = (
            self.db.query(Application).filter(Application.user_id == user_id).all()
        )

        stats = {
            "total_applications": len(applications),
            "pending": sum(1 for a in applications if a.status == "pending"),
            "applied": sum(1 for a in applications if a.status == "applied"),
            "interviews": sum(1 for a in applications if a.status == "interview"),
            "rejections": sum(1 for a in applications if a.status == "rejected"),
            "offers": sum(1 for a in applications if a.status == "offer"),
        }
        return DashboardStats(**stats)

    def update_status(
        self, application_id: int, user_id: int, status: str, notes: str | None = None
    ) -> Application:
        application = (
            self.db.query(Application)
            .filter(Application.id == application_id, Application.user_id == user_id)
            .first()
        )
        if not application:
            raise ValueError("Application not found")

        application.status = status
        status_entry = ApplicationStatus(
            application_id=application.id, status=status, notes=notes
        )
        self.db.add(status_entry)
        self.db.commit()
        self.db.refresh(application)
        return application
