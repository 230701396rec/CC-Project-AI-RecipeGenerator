import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv(".env")
client = InferenceClient(token=os.getenv("HF_API_KEY"))

chat_models = [
    "mistralai/Mistral-Nemo-Instruct-2407",
    "meta-llama/Llama-3.2-3B-Instruct",
    "google/gemma-2-2b-it",
    "Qwen/Qwen2.5-7B-Instruct"
]

for m in chat_models:
    try:
        res = client.chat_completion(
            messages=[{"role":"user", "content":"What is 1+1?"}],
            model=m,
            max_tokens=20
        )
        print(f"[{m}] Success: {res.choices[0].message.content}")
    except Exception as e:
        print(f"[{m}] Error: {repr(e)}")

vision_models = [
    "nlpconnect/vit-gpt2-image-captioning",
    "Salesforce/blip-image-captioning-base"
]

for m in vision_models:
    try:
        res = client.image_to_text(
            "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg/800px-Good_Food_Display_-_NCI_Visuals_Online.jpg",
            model=m
        )
        print(f"[{m}] Success")
    except Exception as e:
        print(f"[{m}] Error: {repr(e)}")
