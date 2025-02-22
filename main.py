from fastapi import FastAPI
from app.api.routers import quotes
from app.database.models import Base, engine

# Initialize Database
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI()

# Include Quotes Router
app.include_router(quotes.router)

# Root endpoint to list all routes
@app.get("/", tags=["Root"])
async def list_routes():
    routes = []
    for route in app.routes:
        if hasattr(route, "path") and hasattr(route, "methods"):
            routes.append({
                "path": route.path,
                "methods": list(route.methods),
                "name": route.name
            })
    return {"available_routes": routes}

# Run with: uvicorn main:app --reload
