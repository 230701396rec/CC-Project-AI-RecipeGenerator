from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class RecipeGenerationRequest(BaseModel):
    ingredients: str

class RecipeResponse(BaseModel):
    id: Optional[int] = None
    name: str
    ingredients_list: List[str]
    instructions: List[str]
    cook_time: str
    nutrition: Optional[dict] = None
    created_at: Optional[datetime] = None

class ImageToRecipeResponse(BaseModel):
    caption: str
    ingredients: str
    recipe: RecipeResponse
