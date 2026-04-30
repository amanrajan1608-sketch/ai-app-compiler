import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from pipeline.validator import validate_consistency
from runtime.simulator import simulate_execution

load_dotenv()

# Configure
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
# Switching to 1.5-flash to avoid the 'Quota Exceeded' error you saw earlier
model = genai.GenerativeModel('models/gemini-1.5-flash')

class CompilerEngine:
    async def run(self, user_prompt: str):
        # Stage 1: Intent
        intent = self._call_ai(f"Extract features from: {user_prompt}. Return JSON.")
        
        # Stage 2: Design
        design = self._call_ai(f"Design architecture for: {intent}. Return JSON.")
        
        # Stage 3: Schema
        schema = self._call_ai(f"Generate UI, API, DB schemas for: {design}. Return JSON.")
        
        # Stage 4: Validation & Repair
        validation = validate_consistency(schema)
        if not validation["is_valid"]:
            repair_prompt = f"Fix these errors: {validation['errors']} in this schema: {schema}. Return JSON."
            schema = self._call_ai(repair_prompt)
            
        # Final: Simulation
        success, exec_msg = simulate_execution(schema)
        
        return {
            "status": "Success" if success else "Simulation Warning",
            "execution_log": exec_msg,
            "config": schema
        }

    def _call_ai(self, prompt):
        """Standardized AI call with Defensive Parsing"""
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        try:
            data = json.loads(response.text)
            # Unwrap if AI returns a list instead of a dictionary
            if isinstance(data, list) and len(data) > 0:
                return data[0]
            return data
        except Exception as e:
            return {"error": "JSON Parsing Failed", "details": str(e)}
