import base64
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

def detect_ingredients_from_image(image_bytes: bytes) -> list[str]:
    """Detect ingredients using OpenAI Vision API"""

    if not API_KEY or API_KEY == "your_openai_api_key_here":
        print("Using mock vision service because OpenAI API key is missing or default.")
        return ["tomato", "onion", "garlic", "chicken"] # Mock ingredients
        
    try:
        client = OpenAI(api_key=API_KEY)
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "List only food ingredients from this image as a comma-separated list"},
                        {
                            "type": "image_url",
                            "image_url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    ]
                }
            ]
        )

        # Convert response into list
        ingredients_text = response.choices[0].message.content
        ingredients_list = [i.strip() for i in ingredients_text.split(",")]

        return ingredients_list

    except Exception as e:
        print(f"Error processing image: {e}")
        return []