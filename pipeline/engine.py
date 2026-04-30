import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

class CompilerEngine:
    async def run(self, user_prompt: str):
        # STAGE 1: Intent Extraction
        intent = self._call_ai(f"Extract app features/roles from: {user_prompt}. Return JSON.")
        
        # STAGE 2: System Design
        design = self._call_ai(f"Based on features {intent}, design architecture. Return JSON.")
        
        # STAGE 3: Schema Generation
        schema = self._call_ai(f"Generate UI, API, and DB schemas for: {design}. Return JSON.")
        
        # STAGE 4: Refinement (Repair Engine)
        final_output = self._call_ai(f"Review and fix errors in this schema: {schema}. Return final JSON.")
        
        return final_output

    def _call_ai(self, prompt):
        response = model.generate_content(
            prompt, 
            generation_config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text)
