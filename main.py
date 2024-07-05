from openai import OpenAI
from fastapi import FastAPI

client = OpenAI(
  organization='org-H62SnBA9zVxUyTrKWWaGcFHs',
  project='proj_YmL1LLCERSFKkexPHujxpfij'
)

app = FastAPI()

response = client.completions.create(
  model="gpt-3.5-turbo",
  prompt="variable goes here to allow post requests from rails",
  max_tokens=100,
  user="user_id variable"
)

@app.get("/")
async def root():
  return {"message": "Hello World"}