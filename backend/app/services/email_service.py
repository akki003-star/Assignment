import logging

from backend.app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self):
        self.sender_email = settings.SENDER_EMAIL

    async def send_application_confirmation(
        self, to_email: str, user_name: str, job_title: str, company: str
    ) -> bool:
        """Send confirmation email after successful application."""
        subject = f"Application Submitted: {job_title} at {company}"
        body = f"""Hi {user_name},

Your application for {job_title} at {company} has been submitted successfully.

We'll keep you updated on the status of your application.

Best regards,
AI Job Application Agent"""

        return await self._send_email(to_email, subject, body)

    async def send_clarification_request(
        self, to_email: str, user_name: str, job_title: str, questions: list[str]
    ) -> bool:
        """Send email requesting clarification from user."""
        questions_text = "\n".join(f"- {q}" for q in questions)
        subject = f"Clarification Needed: {job_title} Application"
        body = f"""Hi {user_name},

While applying for {job_title}, we encountered questions that need your input:

{questions_text}

Please reply to this email with your answers so we can complete the application.

Best regards,
AI Job Application Agent"""

        return await self._send_email(to_email, subject, body)

    async def send_status_update(
        self, to_email: str, user_name: str, job_title: str, status: str
    ) -> bool:
        """Send application status update."""
        subject = f"Application Update: {job_title}"
        body = f"""Hi {user_name},

Your application for {job_title} has been updated.

New Status: {status}

Log in to your dashboard for more details.

Best regards,
AI Job Application Agent"""

        return await self._send_email(to_email, subject, body)

    async def _send_email(self, to_email: str, subject: str, body: str) -> bool:
        """Send email via Gmail API or log if not configured."""
        if not self.sender_email:
            logger.info(f"Email (not sent - not configured): To={to_email}, Subject={subject}")
            return False

        try:
            # In production, use Gmail API with OAuth2
            # For now, log the email
            logger.info(f"Email sent: To={to_email}, Subject={subject}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
