import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
#LLM_MODEL = "gpt-3.5-turbo"
LLM_MODEL = "gpt-4-1106-preview"