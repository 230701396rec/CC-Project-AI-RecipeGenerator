import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from models.schemas import RecipeResponse

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

def generate_recipe_from_ingredients(ingredients: list[str]) -> RecipeResponse:
    ingredient_str = ", ".join(ingredients)
    
    # Mock fallback if no API key is provided
    if not API_KEY or API_KEY == "your_openai_api_key_here":
        return get_mock_recipe(ingredients)
    
    # Real Generation
    client = OpenAI(api_key=API_KEY)
    
    system_prompt = """You are an expert AI chef. The user will give you a list of ingredients. 
Create a delicious recipe strictly using those ingredients and basic pantry staples (salt, pepper, oil, water).
Respond ONLY with a valid JSON object matching this schema:
{
  "name": "Recipe Name",
  "ingredients_list": ["ingredient 1 with quantity", "ingredient 2 with quantity"],
  "instructions": ["Step 1", "Step 2"],
  "cook_time": "Estimated Time (e.g., 30 mins)",
  "nutrition": {
    "calories": "xxx kcal",
    "protein": "xx g",
    "carbs": "xx g", 
    "fat": "xx g"
  }
}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Ingredients: {ingredient_str}"}
            ],
            temperature=0.7,
        )
        
        # Parse the JSON response
        response_text = response.choices[0].message.content
        
        if response_text.startswith("```json"):
            response_text = response_text[7:-3].strip()
        elif response_text.startswith("```"):
            response_text = response_text[3:-3].strip()
            
        data = json.loads(response_text)
        
        return RecipeResponse(
            name=data.get("name", "Generated Recipe"),
            ingredients_list=data.get("ingredients_list", ingredients),
            instructions=data.get("instructions", ["Mix all together and cook."]),
            cook_time=data.get("cook_time", "Unknown"),
            nutrition=data.get("nutrition", {})
        )
        
    except Exception as e:
        print(f"LLM Error: {e}")
        return get_mock_recipe(ingredients)


def get_mock_recipe(ingredients: list[str]) -> RecipeResponse:
    """Fallback generator when API key is missing."""
    import random
    main_ingredient = ingredients[0] if ingredients else "Mystery Item"
    
    mock_instructions = [
        f"Preheat your oven or pan.",
        f"Chop the {main_ingredient} into bite-sized pieces.",
        "Sauté with a bit of olive oil and salt.",
        "Add the rest of your ingredients and stir frequently.",
        "Serve hot and enjoy out of the box!"
    ]
    
    return RecipeResponse(
        name=f"Quick & Easy {main_ingredient.capitalize()} Delight",
        ingredients_list=[f"1 cup {ing}" for ing in ingredients] + ["Salt and pepper to taste", "2 tbsp Olive oil"],
        instructions=mock_instructions,
        cook_time=f"{random.randint(15, 45)} mins",
        nutrition={
            "calories": f"{random.randint(200, 600)} kcal",
            "protein": f"{random.randint(10, 40)} g",
            "carbs": f"{random.randint(10, 60)} g",
            "fat": f"{random.randint(5, 30)} g"
        }
    )