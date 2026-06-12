from sqlalchemy.orm import Session

from backend.app.models.job import Job
from backend.app.schemas.job import JobSearch


class JobService:
    def __init__(self, db: Session):
        self.db = db

    def search_jobs(self, search: JobSearch) -> list[Job]:
        query = self.db.query(Job)

        if search.keywords:
            for keyword in search.keywords:
                query = query.filter(
                    Job.title.ilike(f"%{keyword}%")
                    | Job.description.ilike(f"%{keyword}%")
                )

        if search.location:
            query = query.filter(Job.location.ilike(f"%{search.location}%"))

        if search.salary_min:
            query = query.filter(
                (Job.salary_max >= search.salary_min) | (Job.salary_max.is_(None))
            )

        if search.salary_max:
            query = query.filter(
                (Job.salary_min <= search.salary_max) | (Job.salary_min.is_(None))
            )

        if search.source:
            query = query.filter(Job.source == search.source)

        return query.order_by(Job.posted_date.desc()).limit(50).all()

    def get_job_by_id(self, job_id: int) -> Job | None:
        return self.db.query(Job).filter(Job.id == job_id).first()

    def create_job(self, job_data: dict) -> Job:
        job = Job(**job_data)
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    async def fetch_jobs_from_sources(self, keywords: list[str], location: str | None = None) -> list[dict]:
        """Fetch jobs from external sources (placeholder for Playwright scraping)."""
        # In production, this would use Playwright to scrape job boards
        # For now, return sample data structure
        return [
            {
                "title": f"{keywords[0]} Developer" if keywords else "Software Developer",
                "company": "Tech Corp",
                "location": location or "Remote",
                "description": f"Looking for experienced {', '.join(keywords)} developer",
                "requirements": keywords,
                "url": "https://example.com/job/1",
                "source": "sample",
            }
        ]
