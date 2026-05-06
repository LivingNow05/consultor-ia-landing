import google.generativeai as genai
env_path = "/Users/anthony/Downloads/GeminiDemo/CreateIA/backend/.env"
api_key = None
with open(env_path, "r") as f:
    for line in f:
        if line.startswith("GEMINI_API_KEY="):
            api_key = line.split("=")[1].strip()
genai.configure(api_key=api_key)
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
