from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models import prompt
from settings import OPENAI_API_KEY
import openai

app = FastAPI()

openai.api_key = OPENAI_API_KEY

base_url = "/api"

class generations_request_body(BaseModel):
  text: str
  context: str = "txt_to_sql" 

@app.post(base_url + "/generations")
async def generations(request_body: generations_request_body):
  try:
    output = prompt(request_body.text, request_body.context)
    return output
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))