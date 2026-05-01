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
        res = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        try:
            data = json.loads(res.text)
            return data[0] if isinstance(data, list) else data
        except:
            return {"error": "failed"}
