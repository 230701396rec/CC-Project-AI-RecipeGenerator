import re

def clean_ingredients(ingredients: list[str]) -> list[str]:
    cleaned = []
    for item in ingredients:
        # Lowercase, remove special characters, trim whitespace
        clean_item = re.sub(r'[^a-zA-Z\s]', '', item).strip().lower()
        if clean_item and clean_item not in cleaned:
            cleaned.append(clean_item)
    return cleaned
