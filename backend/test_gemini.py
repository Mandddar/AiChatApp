import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
print(f"API Key found: {'Yes' if api_key else 'No'}")

if api_key:
    genai.configure(api_key=api_key)
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        gemini_history = [{"role": "user", "parts": [{"text": "hey"}]}]
        response = model.generate_content(gemini_history)
        print("Response:", response.text)
    except Exception as e:
        print("Error:", e)
