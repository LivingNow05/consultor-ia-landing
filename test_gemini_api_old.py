import os
import google.generativeai as genai

def test_api():
    from dotenv import load_dotenv
    load_dotenv('/Users/anthony/Downloads/GeminiDemo/CreateIA/backend/.env')
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        print("No API key found")
        return
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    try:
        response = model.generate_content('Responde con la palabra OK si la API funciona.')
        print(f"API Success: {response.text}")
    except Exception as e:
        print(f"API Error: {e}")

test_api()
