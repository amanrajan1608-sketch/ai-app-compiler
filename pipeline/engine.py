import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from pipeline.validator import validate_consistency
from runtime.simulator import simulate_execution

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# I am setting this to 1.5-flash for your Loom video safety (1,500 requests/day).
# If you want 2.5-flash (20 requests/day), change it to 'models/gemini-2.5-flash'
model = genai.GenerativeModel('models/gemini-2.5-flash')

class CompilerEngine:
    async def run(self, user_prompt: str):
        # Stage 1: Intent
        intent = self._call_ai(f"Extract features from: {user_prompt}. Return JSON.")
        # Stage 2: Design
        design = self._call_ai(f"Design architecture for: {intent}. Return JSON.")
        # Stage 3: Schema
        schema = self._call_ai(f"Generate UI, API, DB schemas for: {design}. Return JSON.")
        # Stage 4: Repair
        val = validate_consistency(schema)
        if not val["is_valid"]:
            schema = self._call_ai(f"Fix these errors: {val['errors']} in: {schema}. Return JSON.")
        
        success, msg = simulate_execution(schema)
        return {"status": "Success" if success else "Error", "execution_log": msg, "config": schema}

    def _call_ai(self, prompt):
        """Universal Unwrapper: Ensures we ALWAYS return a dictionary"""
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        try:
            data = json.loads(response.text)
            
            # If it's a list, keep taking the first element until it's a dict
            while isinstance(data, list) and len(data) > 0:
                data = data[0]
            
            # If after unwrapping it's still not a dict, wrap it in one
            if not isinstance(data, dict):
                return {"ai_output": data}
                
            return data
        except Exception as e:
            return {"error": "Parsing failed", "raw": response.text}
