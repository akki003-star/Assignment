import os

from dotenv import load_dotenv
from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel

from utils import call_openai, parse_ai_response

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(title="AI Assignment API")

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -----------------------------
# Input Models
# -----------------------------

class ProductInput(BaseModel):
    product_name: str


class ProposalInput(BaseModel):
    company_type: str
    budget: int


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
            "API Documentation": "/docs"
        }
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

    try:
        result = call_openai(client, prompt)
        return {
            "product": data.product_name,
            "ai_output": parse_ai_response(result),
        }
    except Exception as e:
        return {"error": str(e)}


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

    try:
        result = call_openai(client, prompt)
        return {
            "company_type": data.company_type,
            "budget": data.budget,
            "proposal": parse_ai_response(result),
        }
    except Exception as e:
        return {"error": str(e)}