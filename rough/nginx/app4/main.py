from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import os

app = FastAPI(title="Application 4", description="Simple Application Number 4")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse(os.path.join("static", "index.html"))

@app.get("/api/app-info")
async def get_app_info():
    return {
        "app_number": 4,
        "app_name": "Application 4",
        "port": 5004,
        "message": "Welcome to Application Number 4!"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5004)