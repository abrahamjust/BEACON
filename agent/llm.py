import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv('GOOGLE_API_KEY')
MODEL_NAME = os.getenv('MODEL_NAME')

def get_llm():
    if not GEMINI_API_KEY:
        raise ValueError("GOOGLE_API_KEY not found in .env")

    if not MODEL_NAME:
        raise ValueError("MODEL_NAME not found in .env")

    return ChatGoogleGenerativeAI(
        model = MODEL_NAME,
        google_api_key = GEMINI_API_KEY,
    )

