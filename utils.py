import json

from openai import OpenAI


def call_openai(client: OpenAI, prompt: str, model: str = "gpt-3.5-turbo") -> str:
    """Send a prompt to OpenAI and return the raw response content."""
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def parse_ai_response(raw: str) -> dict:
    """Parse a JSON string from the AI, falling back to a raw_response wrapper."""
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return {"raw_response": raw}
