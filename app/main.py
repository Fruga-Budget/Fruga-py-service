from fastapi import FastAPI, Request, HTTPException
from openai import OpenAI
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


client = OpenAI(api_key=OPENAI_API_KEY)

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
                f"For the following messages provide a response as concise as possible."
                f"A user has a total income of {total_income}."
                f"Their needs are: {needs_data}."
                f"Their wants are: {wants_data}."
                f"Their savings are: {savings_data}."
                f"Please check if the user's budget matches the 50/30/20 rule."
                f"If it does not, provide specific recommendations on how they can adjust their budget to meet the rule."
                f"Highlight which items can be modified and suggest specific changes, considering whether the items are negotiable."
                f"Additionally, provide a revised budget breakdown that meets the 50/30/20 rule as closely as possible."
            )}
        ]

        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=250,
            temperature=0.8
        )
        advice = chat_completion.choices[0].message.content.strip()
        return {"advice": advice}
    except Exception as e:
        logger.error(f"Error generating advice: {e}")
        return {"error": str(e)}

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)