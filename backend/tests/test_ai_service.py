import pytest

from backend.app.services.ai_service import AIService


@pytest.fixture
def ai_service():
    return AIService()


def test_fallback_match_score_full_match(ai_service):
    result = ai_service._fallback_match_score(
        user_skills=["python", "fastapi", "sql"],
        job_requirements=["python", "fastapi", "sql"],
    )
    assert result["match_score"] == 1.0
    assert len(result["missing_skills"]) == 0


def test_fallback_match_score_partial_match(ai_service):
    result = ai_service._fallback_match_score(
        user_skills=["python", "javascript"],
        job_requirements=["python", "fastapi", "sql", "javascript"],
    )
    assert result["match_score"] == 0.5
    assert "fastapi" in result["missing_skills"]
    assert "sql" in result["missing_skills"]


def test_fallback_match_score_no_match(ai_service):
    result = ai_service._fallback_match_score(
        user_skills=["java", "spring"],
        job_requirements=["python", "fastapi"],
    )
    assert result["match_score"] == 0.0
    assert len(result["matched_skills"]) == 0


def test_fallback_match_score_empty_requirements(ai_service):
    result = ai_service._fallback_match_score(
        user_skills=["python"],
        job_requirements=[],
    )
    assert result["match_score"] == 0.0


def test_fallback_cover_letter(ai_service):
    letter = ai_service._fallback_cover_letter(
        user_name="John Doe",
        user_skills=["Python", "FastAPI"],
        job_title="Backend Developer",
        company="Tech Corp",
    )
    assert "John Doe" in letter
    assert "Backend Developer" in letter
    assert "Tech Corp" in letter
    assert "Python" in letter


@pytest.mark.asyncio
async def test_calculate_match_score_without_api_key(ai_service):
    result = await ai_service.calculate_match_score(
        user_skills=["python", "sql"],
        job_requirements=["python", "sql", "docker"],
        job_description="Need a Python developer",
    )
    assert "match_score" in result
    assert 0 <= result["match_score"] <= 1


@pytest.mark.asyncio
async def test_generate_cover_letter_without_api_key(ai_service):
    letter = await ai_service.generate_cover_letter(
        user_name="Jane Doe",
        user_skills=["React", "TypeScript"],
        job_title="Frontend Dev",
        company="Startup Inc",
    )
    assert "Jane Doe" in letter
    assert "Frontend Dev" in letter
