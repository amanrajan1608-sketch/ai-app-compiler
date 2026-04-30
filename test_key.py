import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Load the environment
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

print("--- DIAGNOSTIC START ---")

if not api_key:
    print("❌ ERROR: No API Key found. Check your .env file.")
    exit()

print(f"✅ API Key detected: {api_key[:8]}...{api_key[-4:]}")

# 2. Configure
genai.configure(api_key=api_key)

# 3. List available models (This is the most important part)
print("\n--- CHECKING SUPPORTED MODELS ---")
available_models = []
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Found supported model: {m.name}")
            available_models.append(m.name)
except Exception as e:
    print(f"❌ ERROR while listing models: {e}")
    print("This usually means the API Key is invalid or the 'Generative Language API' is not enabled in Google Cloud Console.")
    exit()

# 4. Try the most likely model
if not available_models:
    print("❌ ERROR: No generative models found for this key.")
    exit()

# We will try 'models/gemini-1.5-flash' first as it's the current standard
target_model = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in available_models else available_models[0]

print(f"\n--- TESTING GENERATION WITH: {target_model} ---")
try:
    model = genai.GenerativeModel(target_model)
    response = model.generate_content("Say 'The Compiler is Ready'")
    print(f"✅ SUCCESS! AI Response: {response.text}")
    print("\nUSE THIS MODEL NAME IN YOUR engine.py:")
    print(f"model = genai.GenerativeModel('{target_model}')")
except Exception as e:
    print(f"❌ GENERATION FAILED: {e}")

print("\n--- DIAGNOSTIC END ---")
