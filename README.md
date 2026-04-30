# AI App Compiler - Demo Task

This system behaves like a compiler for software generation. It converts natural language into a structured, executable application configuration using a multi-stage pipeline.

## 🚀 Features
- **Multi-Stage Pipeline:** Intent Extraction → System Design → Schema Generation → Refinement.
- **Strict Schema Enforcement:** Guarantees valid JSON for UI, API, and Database.
- **Repair Engine:** Automatically detects and fixes logical inconsistencies.
- **Execution Awareness:** Simulates database creation to validate the generated schema.

## 🛠️ Tech Stack
- **LLM:** Google Gemini 1.5 Flash
- **Backend:** FastAPI (Python)
- **Frontend:** HTML/JavaScript
- **Deployment:** Render

## 📂 Folder Structure
- `/pipeline`: Core logic and AI orchestrator.
- `/runtime`: Execution simulation logic.
- `/static`: Frontend interface.
