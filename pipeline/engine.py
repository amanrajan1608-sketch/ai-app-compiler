import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from pipeline.validator import validate_consistency
from runtime.simulator import simulate_execution

load_dotenv()

# Configure using the SUCCESSFUL model from your diagnostic test
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
# We use the specific model name that worked in your test_key.py
model = genai.GenerativeModel('models/gemini-2.5-flash')

class CompilerEngine:
    async def run(self, user_prompt: str):
        print(f"🚀 Starting Multi-Stage Pipeline for: {user_prompt}")

        # STAGE 1: Intent Extraction
        # We simplify the user input into a clean list of needs
        intent_prompt = f"Extract core features and user roles from this request: '{user_prompt}'. Return only JSON."
        intent = self._call_ai(intent_prompt)
        print("✅ Stage 1: Intent Extracted")

        # STAGE 2: System Design
        # We turn those features into an app architecture
        design_prompt = f"Design a software architecture for these features: {intent}. Define entities and flows. Return only JSON."
        design = self._call_ai(design_prompt)
        print("✅ Stage 2: System Design Completed")

        # STAGE 3: Schema Generation
        # We generate the actual "code" (The structured config)
        schema_prompt = (
            f"Based on this design: {design}, generate a strict JSON configuration including: "
            f"1. ui_schema (pages, components), 2. api_schema (endpoints, target_table), "
            f"3. db_schema (tables, columns). Return only JSON."
        )
        schema = self._call_ai(schema_prompt)
        print("✅ Stage 3: Schema Generated")

        # STAGE 4: Validation & Repair (The Core Requirement)
        # We check if the AI made mistakes and ask it to fix them
        validation = validate_consistency(schema)
        if not validation["is_valid"]:
            print(f"⚠️ Stage 4: Inconsistency found. Triggering Repair Engine...")
            repair_prompt = (
                f"The following inconsistencies were found in the schema: {validation['errors']}. "
                f"Fix the schema: {schema} and return the PERFECTED JSON."
            )
            schema = self._call_ai(repair_prompt)
        print("✅ Stage 4: Validation & Repair Finished")

        # FINAL: Execution Awareness (Simulation)
        # We prove it works by building it in-memory
        success, exec_msg = simulate_execution(schema)
        print(f"✅ Final: Execution Awareness: {exec_msg}")

        return {
            "status": "Success" if success else "Simulation Warning",
            "stages_completed": 4,
            "execution_log": exec_msg,
            "config": schema
        }

   def _call_ai(self, prompt):
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        try:
            data = json.loads(response.text)
            
            # REPAIR LOGIC: If AI returns a list [ {...} ], extract the dict inside
            if isinstance(data, list) and len(data) > 0:
                return data[0]
            
            return data
        except (json.JSONDecodeError, Exception) as e:
            return {"error": "Invalid JSON format", "details": str(e)}
