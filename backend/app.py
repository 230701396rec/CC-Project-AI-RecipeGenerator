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

@app.get("/")
def read_root():
    return {"message": "Welcome to the Recipe Generator API!"}
