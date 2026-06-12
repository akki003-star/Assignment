import json

from backend.app.core.config import settings


class AIService:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY

    async def calculate_match_score(
        self, user_skills: list[str], job_requirements: list[str], job_description: str
    ) -> dict:
        """Calculate match score between user profile and job requirements."""
        if not self.api_key:
            return self._fallback_match_score(user_skills, job_requirements)

        try:
            from openai import AsyncOpenAI

            client = AsyncOpenAI(api_key=self.api_key)
            prompt = f"""Analyze the match between a candidate and a job posting.

Candidate Skills: {', '.join(user_skills)}
Job Requirements: {', '.join(job_requirements)}
Job Description: {job_description}

Return a JSON object with:
- match_score: float between 0 and 1
- matched_skills: list of matching skills
- missing_skills: list of skills the candidate lacks
- recommendations: list of suggestions to improve match

Return ONLY valid JSON."""

            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            content = response.choices[0].message.content or "{}"
            return json.loads(content)
        except Exception:
            return self._fallback_match_score(user_skills, job_requirements)

    def _fallback_match_score(
        self, user_skills: list[str], job_requirements: list[str]
    ) -> dict:
        """Fallback scoring without AI - simple keyword matching."""
        if not job_requirements:
            return {
                "match_score": 0.0,
                "matched_skills": [],
                "missing_skills": [],
                "recommendations": [],
            }

        user_skills_lower = {s.lower() for s in user_skills}
        requirements_lower = {r.lower() for r in job_requirements}

        matched = user_skills_lower & requirements_lower
        missing = requirements_lower - user_skills_lower

        score = len(matched) / len(requirements_lower) if requirements_lower else 0.0

        return {
            "match_score": round(score, 2),
            "matched_skills": list(matched),
            "missing_skills": list(missing),
            "recommendations": [f"Consider learning: {s}" for s in list(missing)[:3]],
        }

    async def generate_cover_letter(
        self, user_name: str, user_skills: list[str], job_title: str, company: str
    ) -> str:
        """Generate a customized cover letter."""
        if not self.api_key:
            return self._fallback_cover_letter(user_name, user_skills, job_title, company)

        try:
            from openai import AsyncOpenAI

            client = AsyncOpenAI(api_key=self.api_key)
            prompt = f"""Write a professional cover letter for:
Name: {user_name}
Skills: {', '.join(user_skills)}
Position: {job_title}
Company: {company}

Keep it concise (3 paragraphs) and professional."""

            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            return response.choices[0].message.content or ""
        except Exception:
            return self._fallback_cover_letter(user_name, user_skills, job_title, company)

    def _fallback_cover_letter(
        self, user_name: str, user_skills: list[str], job_title: str, company: str
    ) -> str:
        skills_text = ", ".join(user_skills[:5]) if user_skills else "various technical skills"
        return f"""Dear Hiring Manager,

I am writing to express my interest in the {job_title} position at {company}. With my expertise in {skills_text}, I am confident I can contribute meaningfully to your team.

My professional background has equipped me with the skills necessary to excel in this role. I am eager to bring my experience and dedication to {company}.

Thank you for considering my application. I look forward to the opportunity to discuss how my skills align with your needs.

Sincerely,
{user_name}"""

    async def optimize_resume(
        self, resume_content: str, job_title: str, job_description: str
    ) -> str:
        """Optimize resume content for a specific job."""
        if not self.api_key:
            return resume_content

        try:
            from openai import AsyncOpenAI

            client = AsyncOpenAI(api_key=self.api_key)
            prompt = f"""Optimize the following resume for the job posting.

Resume:
{resume_content}

Job Title: {job_title}
Job Description: {job_description}

Return an optimized version of the resume that highlights relevant skills and experience.
Keep the factual content accurate but reorder and emphasize relevant points."""

            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
            )
            return response.choices[0].message.content or resume_content
        except Exception:
            return resume_content
