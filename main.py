from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.routers import quotes
from app.database.models import Base, engine

# Initialize Database
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI()

# Mount the static directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Serve index.html at the root URL
@app.get("/")
async def read_root():
    return FileResponse("app/static/index.html")

# Include Quotes Router
app.include_router(quotes.router)

# Run with: uvicorn main:app --reload
