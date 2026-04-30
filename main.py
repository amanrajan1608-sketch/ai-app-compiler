from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pipeline.engine import CompilerEngine
import os

app = FastAPI()
compiler = CompilerEngine()

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

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
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
