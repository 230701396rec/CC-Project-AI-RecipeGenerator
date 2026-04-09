from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from ml_service.llm_engine import extract_ingredients, generate_recipe, generate_image_caption
from models.schemas import ImageToRecipeResponse
from models.database import get_db, RecipeDB
import json

router = APIRouter()

@router.post("/image-to-recipe", response_model=ImageToRecipeResponse)
async def image_to_recipe(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        contents = await file.read()
        
        # 1. BLIP -> caption
        caption = generate_image_caption(contents)
        
        # 2. Mistral -> ingredients
        ingredients_str = extract_ingredients(caption)
        
        # 3. Mistral -> recipe
        recipe = generate_recipe(ingredients_str)
        
        # Save to database
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
        
        recipe.id = db_recipe.id
        recipe.created_at = db_recipe.created_at
        
        return ImageToRecipeResponse(
            caption=caption,
            ingredients=ingredients_str,
            recipe=recipe
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
