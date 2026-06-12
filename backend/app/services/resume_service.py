import os
import re
from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.models.resume import Resume
from backend.app.services.ai_service import AIService


def _sanitize_filename(filename: str) -> str:
    """Strip path components and dangerous characters from an upload filename."""
    name = os.path.basename(filename)
    name = re.sub(r"[^\w.\-]", "_", name)
    return name or "upload"


class ResumeService:
    def __init__(self, db: Session):
        self.db = db
        self.ai_service = AIService()

    async def upload_resume(self, user_id: int, file: UploadFile) -> Resume:
        upload_dir = Path(settings.UPLOAD_DIR).resolve() / str(user_id)
        upload_dir.mkdir(parents=True, exist_ok=True)

        # Get current version count
        existing_count = (
            self.db.query(Resume)
            .filter(Resume.user_id == user_id, Resume.is_base == 1)
            .count()
        )

        safe_name = _sanitize_filename(file.filename or "upload")
        file_path = (upload_dir / f"resume_v{existing_count + 1}_{safe_name}").resolve()

        # Ensure the resolved path is still inside the upload directory
        if not str(file_path).startswith(str(upload_dir)):
            raise ValueError("Invalid filename")

        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        # Parse resume content
        parsed_content = self._parse_resume(file_path, file.filename)

        resume = Resume(
            user_id=user_id,
            version=existing_count + 1,
            file_path=str(file_path),
            file_name=file.filename,
            parsed_content=parsed_content,
            is_base=1,
        )
        self.db.add(resume)
        self.db.commit()
        self.db.refresh(resume)
        return resume

    def get_user_resumes(self, user_id: int) -> list[Resume]:
        return (
            self.db.query(Resume)
            .filter(Resume.user_id == user_id)
            .order_by(Resume.version.desc())
            .all()
        )

    def get_latest_resume(self, user_id: int) -> Resume | None:
        return (
            self.db.query(Resume)
            .filter(Resume.user_id == user_id, Resume.is_base == 1)
            .order_by(Resume.version.desc())
            .first()
        )

    async def optimize_resume(
        self, user_id: int, job_title: str, job_description: str
    ) -> Resume | None:
        base_resume = self.get_latest_resume(user_id)
        if not base_resume:
            return None

        optimized_content = await self.ai_service.optimize_resume(
            resume_content=base_resume.parsed_content or "",
            job_title=job_title,
            job_description=job_description,
        )

        resume = Resume(
            user_id=user_id,
            version=base_resume.version,
            file_path=base_resume.file_path,
            file_name=f"optimized_{base_resume.file_name}",
            parsed_content=optimized_content,
            is_base=0,
        )
        self.db.add(resume)
        self.db.commit()
        self.db.refresh(resume)
        return resume

    def _parse_resume(self, file_path: Path, filename: str) -> str:
        ext = os.path.splitext(filename)[1].lower()
        if ext == ".pdf":
            return self._parse_pdf(file_path)
        elif ext == ".txt":
            return self._parse_txt(file_path)
        return ""

    def _parse_pdf(self, file_path: Path) -> str:
        try:
            from PyPDF2 import PdfReader

            reader = PdfReader(str(file_path))
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
        except Exception:
            return ""

    def _parse_txt(self, file_path: Path) -> str:
        try:
            with open(file_path) as f:
                return f.read()
        except Exception:
            return ""
