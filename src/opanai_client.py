import os

from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

_ = load_dotenv(find_dotenv())
openai_api_key = os.environ['OPEN_API_KEY']
client = OpenAI(api_key=openai_api_key)
