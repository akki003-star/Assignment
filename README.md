# AI Product Automation API

## Project Overview

This project is an AI-powered backend system that automates product classification and B2B proposal generation using artificial intelligence.

The API allows businesses to automatically generate product categories, SEO tags, sustainability filters, and business proposals using AI.

The system is built using **Python**, **FastAPI**, and **OpenAI API**.

---

# Features

## 1. AI Product Category Generator

This module analyzes a product name and generates:

* Primary category
* Sub category
* SEO tags
* Sustainability filters

Example Input:

```json
{
 "product_name": "bamboo toothbrush"
}
```

Example Output:

```json
{
 "product": "bamboo toothbrush",
 "ai_output": {
   "category": "Personal Care",
   "sub_category": "Oral Care",
   "tags": ["eco friendly toothbrush","bamboo toothbrush"],
   "filters": ["plastic-free","sustainable"]
 }
}
```

---

## 2. AI B2B Proposal Generator

This module generates sustainable product kit proposals for companies based on a given budget.

Example Input:

```json
{
 "company_type": "IT company",
 "budget": 50000
}
```

Example Output:

```json
{
 "company_type": "IT company",
 "budget": 50000,
 "proposal": {
   "products": ["Bamboo bottles","Recycled notebooks"],
   "budget_breakdown": {
     "bottle": 200,
     "notebook": 150
   },
   "total_cost": "45000",
   "impact_summary": "This proposal reduces plastic waste and promotes sustainable materials."
 }
}
```

---

# System Architecture

The system follows a **simple AI-powered API architecture**.

```
Client (Browser / API Tester)
        |
        v
FastAPI Backend
        |
        v
AI Prompt Processing
        |
        v
OpenAI API
        |
        v
Structured JSON Response
```

### Components

**Client Layer**

* Browser or API testing interface (Swagger UI)

**API Layer**

* FastAPI handles HTTP requests and responses

**AI Processing Layer**

* Prompts are sent to OpenAI models
* AI generates structured outputs

**Response Layer**

* AI output is formatted as JSON and returned to the client

---

# AI Prompt Design

Prompt engineering is used to guide the AI to generate structured responses.

Example prompt used for category generation:

```
Product: bamboo toothbrush

Generate:
- primary category
- sub category
- 5 SEO tags
- sustainability filters

Return JSON format.
```

Key design considerations:

1. **Clear instructions** to the AI
2. **Structured JSON output**
3. **Domain-specific context (sustainability)**

This ensures the AI produces consistent and usable responses.

---

# Technologies Used

* Python
* FastAPI
* OpenAI API
* Pydantic
* Uvicorn

---

# How to Run the Project

1. Install dependencies

```
pip install -r requirements.txt
```

2. Start the server

```
uvicorn main:app --reload
```

3. Open API documentation

```
http://127.0.0.1:8000/docs
```

---

# API Endpoints

| Method | Endpoint           | Description               |
| ------ | ------------------ | ------------------------- |
| GET    | /                  | API status                |
| POST   | /generate-category | Generate product category |
| POST   | /generate-proposal | Generate B2B proposal     |

---

# Future Improvements

* Add database logging
* Add AI response caching
* Add WhatsApp chatbot integration
* Add sustainability impact calculator

---

# Author

AI Internship Assignment Project
