import os
from dotenv import load_dotenv

load_dotenv()

# API key
CHATANYWHERE_API_KEY = os.getenv("CHATANYWHERE_API_KEY")

if not CHATANYWHERE_API_KEY:
    raise ValueError("API key not existing in .env")

print("good to go")