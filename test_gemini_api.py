import os
from google import genai
from google.genai import types

def test_api():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        from dotenv import load_dotenv
        load_dotenv('/Users/anthony/Downloads/GeminiDemo/CreateIA/backend/.env')
        api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        print("No API key found")
        return
        
    client = genai.Client(api_key=api_key)
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents='Responde con la palabra OK si la API funciona.'
        )
        print(f"API Success: {response.text}")
    except Exception as e:
        print(f"API Error: {e}")

test_api()
