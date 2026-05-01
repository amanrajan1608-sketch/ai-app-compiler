from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pipeline.engine import CompilerEngine
import os

app = FastAPI()
compiler = CompilerEngine()

# Get the absolute path to the directory this file is in
base_path = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(base_path, "static", "index.html")

@app.get("/")
async def read_index():
    # Check if the file exists before trying to send it
    if os.path.exists(html_path):
        return FileResponse(html_path)
    else:
        # This will tell us exactly where the server is looking
        return {"error": "index.html not found", "looked_at": html_path}

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_app(request: PromptRequest):
    try:
        return await compiler.run(request.prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
