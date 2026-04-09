from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import json

from models.schemas import RecipeGenerationRequest, RecipeResponse
from models.database import get_db, RecipeDB
from utils.text_cleaning import clean_ingredients
from ml_service.mistral_engine import generate_recipe as generate_recipe_from_ingredients

router = APIRouter()

@router.post("/generate-recipe", response_model=RecipeResponse)
def generate_recipe(request: RecipeGenerationRequest, db: Session = Depends(get_db)):
    # 1. Clean the ingredients
    cleaned_ingredients = clean_ingredients(request.ingredients)
    if not cleaned_ingredients:
        raise HTTPException(status_code=400, detail="No valid ingredients provided.")
        
    # 2. Call the LLM (or mock)
    recipe = generate_recipe_from_ingredients(cleaned_ingredients)
    
    # 3. Save to database
    db_recipe = RecipeDB(
        name=recipe.name,
        ingredients_list=json.dumps(recipe.ingredients_list),
        instructions=json.dumps(recipe.instructions),
        cook_time=recipe.cook_time,
        nutrition=json.dumps(recipe.nutrition) if recipe.nutrition else None
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    
    # Return populated ID
    recipe.id = db_recipe.id
    recipe.created_at = db_recipe.created_at
    return recipe

@router.get("/recipes", response_model=List[RecipeResponse])
def get_recent_recipes(db: Session = Depends(get_db), limit: int = 10):
    db_recipes = db.query(RecipeDB).order_by(RecipeDB.created_at.desc()).limit(limit).all()
    
    response_list = []
    for r in db_recipes:
        response_list.append(RecipeResponse(
            id=r.id,
            name=r.name,
            ingredients_list=json.loads(r.ingredients_list),
            instructions=json.loads(r.instructions),
            cook_time=r.cook_time,
            nutrition=json.loads(r.nutrition) if r.nutrition else None,
            created_at=r.created_at
        ))
    return response_list
