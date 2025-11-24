# debug_models.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def list_available_models():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: No API Key found in .env")
        return

    print(f"--- Checking Available Models for Key ending in ...{api_key[-4:]} ---")
    
    try:
        genai.configure(api_key=api_key)
        
        print("\nAvailable 'generateContent' Models:")
        print("-" * 40)
        found_any = False
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"✅ {m.name}")
                found_any = True
        
        if not found_any:
            print("⚠️ No models found supporting 'generateContent'. Check your API key permissions.")
            
    except Exception as e:
        print(f"❌ Connectivity Error: {e}")

if __name__ == "__main__":
    list_available_models()