from dotenv import load_dotenv
import os
load_dotenv()

OPENROUTER_API = "https://openrouter.ai/api/v1"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")