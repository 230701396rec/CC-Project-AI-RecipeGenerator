from fastapi import APIRouter, UploadFile, File, HTTPException
from ml_service.vision import detect_ingredients_from_image
from models.schemas import ImageAnalysisResponse

router = APIRouter()

@router.post("/analyze-image", response_model=ImageAnalysisResponse)
async def analyze_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        detected_items = detect_ingredients_from_image(contents)
        
        # If the ML model throws a fallback or returns empty
        if not detected_items:
            detected_items = ["No recognizable ingredients found. Try typing them!"]
            
        return ImageAnalysisResponse(detected_ingredients=detected_items)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
