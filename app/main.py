from fastapi import FastAPI, Request, HTTPException
import httpx
from dotenv import load_dotenv
import os
import logging

load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
  raise ValueError("OpenAI API key is missing")

async def fetch_openai_advice(messages):
  async with httpx.AsyncClient() as client:
    try:
        response = await client.post(
          "https://api.openai.com/v1/chat/completions",
          headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
          },
          json={
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "max_tokens": 250,
            "temperature": 0.7
          }
        )
        response.raise_for_status()
        return response.json()
    except httpx.RequestError as exc:
        logger.error(f"An error occurred while requesting OpenAI: {exc}")
        raise HTTPException(status_code=500, detail="OpenAI service request failed")
    except httpx.HTTPStatusError as exc:
        logger.error(f"HTTP status error: {exc.response.status_code} - {exc.response.content}")
        raise HTTPException(status_code=exc.response.status_code, detail="OpenAI API error")
    
@app.post("/v1/generate_advice")
async def generate_advice(request: Request):
  try:
    body = await request.json()
    total_income = body.get("total_income")
    needs = body.get("needs", [])
    wants = body.get("wants", [])
    savings = body.get("savings", [])

    needs_data = [{"name": item["name"], "cost": item["cost"], "description": item["description"], "isNegotiable": item["isNegotiable"]} for item in needs]
    wants_data = [{"name": item["name"], "cost": item["cost"], "description": item["description"]} for item in wants]
    savings_data = [{"name": item["name"], "cost": item["cost"], "description": item["description"]} for item in savings]

    messages = [
        {"role": "system", "content": "You are personal financial planner."},
        {"role": "user", "content": (
          "Please provide a concise response of no more than 250 tokens."
          f" A user has a total income of {total_income}. "
          f"Their needs are: {needs_data}. "
          f"Their wants are: {wants_data}. "
          f"Their savings are: {savings_data}. "
          "Check if the user's budget matches the 50/30/20 rule. "
          "If not, provide specific recommendations for adjustments, highlighting negotiable items. "
          "Additionally, provide a revised budget breakdown that closely meets the 50/30/20 rule."
        )}
    ]

    response_data = await fetch_openai_advice(messages)
    advice = response_data['choices'][0]['message']['content'].strip()
    return {"advice": advice}
  except Exception as e:
    logger.error(f"Error generating advice: {e}")
    raise HTTPException(status_code=500, detail="Failed to generate advice")

@app.get("/")
async def root():
    return {"message": "Hello World"}
