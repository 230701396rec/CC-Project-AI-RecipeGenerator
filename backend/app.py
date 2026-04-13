import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import image_routes, recipe_routes
from models.database import init_db

# Initialize database
init_db()

app = FastAPI(title="Recipe Generator API")

# Setup CORS to allow Vite React app to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For dev purposes only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(image_routes.router, tags=["Images"])
app.include_router(recipe_routes.router, tags=["Recipes"])

@app.get("/api/health")
def read_root():
    return {"message": "Welcome to the Recipe Generator API!"}

# Serve React Frontend
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dist")
if os.path.exists(frontend_path):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_path, "assets")), name="assets")
    
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # Let API routes pass through to 404 naturally if not matched above
        if full_path.startswith("generate-recipe") or full_path.startswith("image-to-recipe") or full_path.startswith("recipes"):
            return {"error": "Endpoint not found"}
        return FileResponse(os.path.join(frontend_path, "index.html"))
