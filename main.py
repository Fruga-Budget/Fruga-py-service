from fastapi import FastAPI, Request
import openai
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
# client = OpenAI(
#   organization='org-H62SnBA9zVxUyTrKWWaGcFHs',
#   project='proj_YmL1LLCERSFKkexPHujxpfij'
# )
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

openai.api_key = OPENAI_API_KEY

@app.post("/generate_advice")
async def generate_advice(request: Request):
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
      f"A user has a total income of {total_income}."
      f"Their needs are: {needs_data}."
      f"Their wants are: {wants_data}."
      f"Their savings are: {savings_data}."
      f"Please check if the user's budget matches the 50/30/20 rule."
      f"If it does not, provide specific recommendations on how they can adjust their budget to meet the rule."
      f"Highlight which items can be modified and suggest specific changes, considering whether the items are negotiable."
      f"Additionally, provide a revised budget breakdown that meets the 50/30/20 rule as closely as possible."
      f"Provide the top 3 suggestions on how the user can make their savings grow"
    )}
  ]

  response = client.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    max_tokens=100,
    temperature=0.8 # we can change this to see different results, higher number more creative responses
    # user="user_id variable"
  )

  advice = response['choices'][0]['message']['content'].strip()
  return {"advice": advice}

@app.get("/")
async def root():
  return {"message": "Hello World"}