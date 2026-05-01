from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from pipeline.engine import CompilerEngine
import os

app = FastAPI()
compiler = CompilerEngine()

# Get absolute path for static files
base_path = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(base_path, "static")

@app.get("/")
async def read_index():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse(status_code=404, content={"error": "index.html missing"})

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_app(request: PromptRequest):
    try:
        result = await compiler.run(request.prompt)
        return result
    except Exception as e:
        # This catches the crash and sends it as JSON so the browser doesn't break
        print(f"CRASH LOG: {str(e)}")
        return JSONResponse(
            status_code=500, 
            content={"error": "Internal Server Error", "details": str(e)}
        )

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
