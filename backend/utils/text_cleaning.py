import re

def clean_ingredients(ingredients_str: str) -> str:
    cleaned = []
    # Split by comma or newline
    items = re.split(r'[,\n]', ingredients_str)
    for item in items:
        # Relaxed regex to keep numbers and spaces
        clean_item = re.sub(r'[^a-zA-Z0-9\s-]', '', item).strip().lower()
        if clean_item and clean_item not in cleaned:
            cleaned.append(clean_item)
    return ", ".join(cleaned)
