from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class RecipeGenerationRequest(BaseModel):
    ingredients: List[str]

class RecipeResponse(BaseModel):
    id: Optional[int] = None
    name: str
    ingredients_list: List[str]
    instructions: List[str]
    cook_time: str
    nutrition: Optional[dict] = None
    created_at: Optional[datetime] = None

class ImageAnalysisResponse(BaseModel):
    detected_ingredients: List[str]
