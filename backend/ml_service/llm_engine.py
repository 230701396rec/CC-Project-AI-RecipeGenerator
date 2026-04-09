import os
import json
import re
import base64
from dotenv import load_dotenv
from mistralai.client import Mistral
from models.schemas import RecipeResponse

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_API_URL = os.getenv("MISTRAL_API_URL")

client = Mistral(api_key=MISTRAL_API_KEY, server_url=MISTRAL_API_URL) if MISTRAL_API_KEY else None

def extract_ingredients(caption: str) -> str:
    """Extract ingredients from image caption."""
    prompt = f"Extract only food ingredients from this description: {caption}. Return as a clean comma-separated list."
    
    if not client:
        return "tomato, onion, garlic, chicken" # Mock fallback
        
    try:
        response = client.chat.complete(
            model="open-mistral-7b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error calling Mistral API for ingredients: {e}")
        return "tomato, onion, garlic, chicken" # Mock fallback

def generate_recipe_from_ingredients(ingredients) -> RecipeResponse:
    """Generate structured recipe JSON from ingredients list."""
    # Input: list of ingredients. Convert to string
    if isinstance(ingredients, list):
        ingredients_str = ", ".join(ingredients)
    else:
        ingredients_str = ingredients
        
    prompt = f"""You are an expert chef. Create a recipe using: {ingredients_str}. 
Return ONLY valid JSON in this format:
{{
  "name": "",
  "ingredients_list": ["String format only (e.g., '1 cup of milk')"],
  "instructions": [],
  "cook_time": "",
  "nutrition": {{
    "calories": "",
    "protein": "",
    "carbs": "",
    "fat": ""
  }}
}}"""
    
    fallback = RecipeResponse(
        name="Fallback Recipe (API Error)",
        ingredients_list=[i.strip() for i in ingredients_str.split(",")],
        instructions=["Cook the ingredients properly", "Serve hot"],
        cook_time="30 mins",
        nutrition={"calories": "Unknown"}
    )
    
    if not client:
        return fallback

    try:
        response = client.chat.complete(
            model="open-mistral-7b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        response_text = response.choices[0].message.content
        
        # Remove markdown (```json if present)
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL | re.IGNORECASE)
        if json_match:
            json_str = json_match.group(1)
        else:
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}')
            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx+1]
            else:
                json_str = response_text
                
        # Parse JSON safely
        data = json.loads(json_str)
        
        return RecipeResponse(
            name=data.get("name", "Generated Recipe"),
            ingredients_list=data.get("ingredients_list", [i.strip() for i in ingredients_str.split(",")]),
            instructions=data.get("instructions", []),
            cook_time=data.get("cook_time", "Unknown"),
            nutrition=data.get("nutrition", {})
        )
    except Exception as e:
        print(f"Error calling Mistral API or parsing JSON: {e}")
        return fallback

def generate_image_caption(image_bytes: bytes) -> str:
    """Use Pixtral model to generate a basic caption for the food image."""
    if not client:
        return "a photo of a delicious meal with various ingredients"
        
    try:
        encoded_image = base64.b64encode(image_bytes).decode('utf-8')
        response = client.chat.complete(
            model="pixtral-12b-2409",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What is in this image? Provide a brief caption focusing on the food and ingredients."},
                        {"type": "image_url", "image_url": f"data:image/jpeg;base64,{encoded_image}"}
                    ]
                }
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error processing image with Pixtral: {e}")
        return "Fallback: a photo of a meal"

generate_recipe = generate_recipe_from_ingredients
