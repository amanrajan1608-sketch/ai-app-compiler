import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from pipeline.validator import validate_consistency
from runtime.simulator import simulate_execution

load_dotenv()

# Configure with Gemini 2.5 Flash
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-2.5-flash')

class CompilerEngine:
    async def run(self, user_prompt: str):
        # STAGE 1: Intent Extraction
        intent = self._call_ai(f"Extract features and roles from: {user_prompt}. Return JSON.")
        
        # STAGE 2: System Design
        design = self._call_ai(f"Design app architecture for these features: {intent}. Return JSON.")
        
        # STAGE 3: Schema Generation (UI, API, DB)
        schema = self._call_ai(f"Generate strict UI, API, and DB schemas for this design: {design}. Return JSON.")
        
        # STAGE 4: Refinement & Repair Engine
        validation = validate_consistency(schema)
        if not validation["is_valid"]:
            # If inconsistencies found, re-prompt to repair (The 'Core' requirement)
            repair_prompt = f"Fix these inconsistencies: {validation['errors']} in this schema: {schema}. Return perfected JSON."
            schema = self._call_ai(repair_prompt)
            
        # FINAL: Execution Awareness Simulation
        success, exec_msg = simulate_execution(schema)
        
        return {
            "status": "Success" if success else "Simulation Warning",
            "stages_completed": 4,
            "execution_log": exec_msg,
            "config": schema
        }

    def _call_ai(self, prompt):
        """Standardized AI call with logic to handle list/dict inconsistencies"""
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        try:
            data = json.loads(response.text)
            # REPAIR: If AI returns a list [ {...} ], extract the dict inside
            if isinstance(data, list) and len(data) > 0:
                return data[0]
            return data
        except Exception as e:
            return {"error": "JSON Parsing Failed", "details": str(e)}
