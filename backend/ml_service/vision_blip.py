import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
API_URL = "https://router.huggingface.co/hf-inference/models/Salesforce/blip-image-captioning-base"
headers = {"Authorization": f"Bearer {HF_API_KEY}"}

def generate_image_caption(image_bytes: bytes) -> str:
    """Use BLIP model to generate a basic caption for the food image."""
    if not HF_API_KEY:
        print("Using mock vision service because HF_API_KEY is missing.")
        return "a photo of a delicious meal with various ingredients"
        
    try:
        response = requests.post(API_URL, headers=headers, data=image_bytes)
        response.raise_for_status()
        result = response.json()
        
        # Hugging Face returns a list with generated_text dict
        if isinstance(result, list) and len(result) > 0:
            caption = result[0].get("generated_text", "")
            return caption
        
        return "a photo of a meal"
    except Exception as e:
        print(f"Error processing image with BLIP: {e}")
        return "Fallback: a photo of a meal"
