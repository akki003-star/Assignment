from fastapi import FastAPI
from pydantic import BaseModel
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

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
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.choices[0].message.content

        try:
            result_json = json.loads(result)
        except:
            result_json = {"raw_response": result}

        return {
            "product": data.product_name,
            "ai_output": result_json
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
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.choices[0].message.content

        try:
            result_json = json.loads(result)
        except:
            result_json = {"raw_response": result}

        return {
            "company_type": data.company_type,
            "budget": data.budget,
            "proposal": result_json
        }

    except Exception as e:
        return {"error": str(e)}