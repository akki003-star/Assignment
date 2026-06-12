import json
import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from openai import OpenAI, APIConnectionError, RateLimitError, APIStatusError
from pydantic import BaseModel, field_validator

# Load environment variables
load_dotenv()

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Validate required configuration at startup
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.warning(
        "OPENAI_API_KEY is not set. AI endpoints will return 503 until it is configured."
    )

# Create FastAPI app
app = FastAPI(title="AI Assignment API")

# OpenAI client (initialized even if key is missing so the app can still serve the home route)
client = OpenAI(api_key=api_key or "")


# -----------------------------
# Input Models
# -----------------------------


class ProductInput(BaseModel):
    product_name: str

    @field_validator("product_name")
    @classmethod
    def product_name_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("product_name must not be blank")
        return v.strip()


class ProposalInput(BaseModel):
    company_type: str
    budget: int

    @field_validator("company_type")
    @classmethod
    def company_type_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("company_type must not be blank")
        return v.strip()

    @field_validator("budget")
    @classmethod
    def budget_must_be_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("budget must be a positive integer")
        return v


# -----------------------------
# Helpers
# -----------------------------


def _require_api_key() -> None:
    """Raise 503 if the OpenAI API key was never configured."""
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="OpenAI API key is not configured. Set OPENAI_API_KEY in the environment.",
        )


def _extract_content(response) -> str:
    """Safely extract the text content from an OpenAI chat completion response."""
    if not response.choices:
        raise HTTPException(
            status_code=502,
            detail="AI returned an empty response (no choices).",
        )
    content = response.choices[0].message.content
    if content is None:
        raise HTTPException(
            status_code=502,
            detail="AI returned a response with no text content.",
        )
    return content


def _parse_ai_json(raw: str, context: str) -> dict:
    """Parse a JSON string from AI output; raise 502 with details on failure."""
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, ValueError) as exc:
        logger.warning("Failed to parse AI JSON for %s: %s — raw: %s", context, exc, raw)
        raise HTTPException(
            status_code=502,
            detail=f"AI returned invalid JSON. Raw response: {raw}",
        )


def _call_openai(prompt: str, context: str) -> str:
    """Call the OpenAI chat API with unified error handling. Returns raw content."""
    _require_api_key()
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
    except APIConnectionError as exc:
        logger.error("OpenAI connection error (%s): %s", context, exc)
        raise HTTPException(
            status_code=502,
            detail="Failed to connect to the AI service. Please try again later.",
        )
    except RateLimitError as exc:
        logger.error("OpenAI rate limit hit (%s): %s", context, exc)
        raise HTTPException(
            status_code=429,
            detail="AI service rate limit exceeded. Please try again later.",
        )
    except APIStatusError as exc:
        logger.error("OpenAI API error (%s): status=%s body=%s", context, exc.status_code, exc.body)
        raise HTTPException(
            status_code=502,
            detail=f"AI service error (status {exc.status_code}). Please try again later.",
        )
    return _extract_content(response)


# -----------------------------
# Home Route
# -----------------------------


@app.get("/")
def home():
    return {
        "project": "AI Product Automation System",
        "status": "Running Successfully",
        "version": "1.0",
        "description": "This API uses AI to generate product categories and B2B proposals.",
        "available_endpoints": {
            "Generate Product Category": "POST /generate-category",
            "Generate B2B Proposal": "POST /generate-proposal",
            "API Documentation": "/docs",
        },
    }


# -----------------------------
# Module 1: Category Generator
# -----------------------------


@app.post("/generate-category")
def generate_category(data: ProductInput):
    prompt = f"""
    Product: {data.product_name}

    Generate:
    - primary category
    - sub category
    - 5 SEO tags
    - sustainability filters

    Return JSON format:
    {{
      "category": "",
      "sub_category": "",
      "tags": [],
      "filters": []
    }}
    """

    raw = _call_openai(prompt, context=f"generate-category({data.product_name!r})")
    result_json = _parse_ai_json(raw, context=f"generate-category({data.product_name!r})")

    return {
        "product": data.product_name,
        "ai_output": result_json,
    }


# -----------------------------
# Module 2: B2B Proposal Generator
# -----------------------------


@app.post("/generate-proposal")
def generate_proposal(data: ProposalInput):
    prompt = f"""
    Company type: {data.company_type}
    Budget: {data.budget}

    Suggest sustainable gift products.

    Return JSON format:
    {{
      "products": [],
      "budget_breakdown": {{}},
      "total_cost": "",
      "impact_summary": ""
    }}
    """

    raw = _call_openai(prompt, context=f"generate-proposal({data.company_type!r}, {data.budget})")
    result_json = _parse_ai_json(raw, context=f"generate-proposal({data.company_type!r}, {data.budget})")

    return {
        "company_type": data.company_type,
        "budget": data.budget,
        "proposal": result_json,
    }
