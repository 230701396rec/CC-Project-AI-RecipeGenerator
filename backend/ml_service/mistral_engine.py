import os
import json
import requests
import re
from dotenv import load_dotenv
from models.schemas import RecipeResponse

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
# Using Mistral-7B-Instruct
API_URL = "https://router.huggingface.co/hf-inference/models/mistralai/Mistral-7B-Instruct-v0.3"

headers = {"Authorization": f"Bearer {HF_API_KEY}"} if HF_API_KEY else {}

def _call_hf_api(prompt: str, max_new_tokens: int = 500) -> str:
    """Helper to call Hugging Face Inference API with Mistral instruction format."""
    if not HF_API_KEY:
        print("HF API Key missing. Returning fallback.")
        return ""
        
    # Mistral Instruction format
    formatted_prompt = f"<s>[INST] {prompt} [/INST]"
    
    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json={
                "inputs": formatted_prompt,
                "parameters": {
                    "temperature": 0.5,
                    "max_new_tokens": max_new_tokens,
                    "return_full_text": False
                }
            }
        )
        response.raise_for_status()
        result = response.json()
        
        if isinstance(result, list):
            text = result[0].get("generated_text", "")
        else:
            text = result.get("generated_text", "")
            
        return text.strip()
    except Exception as e:
        print(f"Error calling Mistral API: {e}")
        # Could fail due to timeout initially
        return ""

def extract_ingredients(caption: str) -> str:
    """Extract ingredients from image caption."""
    prompt = f"Extract only food ingredients from this description: {caption}. Return as a clean comma-separated list."
    
    response_text = _call_hf_api(prompt, max_new_tokens=100)
    
    if not response_text:
        return "tomato, onion, garlic, chicken" # Mock fallback
        
    return response_text

def generate_recipe(ingredients: str) -> RecipeResponse:
    """Generate structured recipe JSON from ingredients list."""
    prompt = f"""You are an expert chef. Create a recipe using: {ingredients}. Return JSON with name, ingredients_list, instructions, cook_time, nutrition."""
    
    response_text = _call_hf_api(prompt, max_new_tokens=800)
    
    # Fallback response
    fallback = RecipeResponse(
        name="Fallback Recipe (API Error)",
        ingredients_list=[i.strip() for i in ingredients.split(",")],
        instructions=["Cook the ingredients properly", "Serve hot"],
        cook_time="30 mins",
        nutrition={"calories": "Unknown"}
    )
    
    if not response_text:
        return fallback

    # Extract JSON robustly
    try:
        # Regex to find JSON block if Mistral wraps it in markdown
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL | re.IGNORECASE)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Fallback to finding the first { and last }
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}')
            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx+1]
            else:
                json_str = response_text
                
        data = json.loads(json_str)
        
        return RecipeResponse(
            name=data.get("name", "Generated Recipe"),
            ingredients_list=data.get("ingredients_list", [i.strip() for i in ingredients.split(",")]),
            instructions=data.get("instructions", []),
            cook_time=data.get("cook_time", "Unknown"),
            nutrition=data.get("nutrition", {})
        )
    except json.JSONDecodeError as e:
        print(f"JSON Parse Error: {e}\nRaw output: {response_text}")
        fallback.name = "Recipe Format Error"
        return fallback
