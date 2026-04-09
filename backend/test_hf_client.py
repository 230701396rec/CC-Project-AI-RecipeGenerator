import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv(".env")
client = InferenceClient(token=os.getenv("HF_API_KEY"))

try:
    print("Testing BLIP Large...")
    res = client.image_to_text(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg/800px-Good_Food_Display_-_NCI_Visuals_Online.jpg",
        model="Salesforce/blip-image-captioning-large"
    )
    print("BLIP Success")
except Exception as e:
    print("BLIP Large Error:", repr(e))

try:
    print("\nTesting Mistral v0.2...")
    res = client.chat_completion(
        messages=[{"role":"user", "content":"What is 1+1?"}],
        model="mistralai/Mistral-7B-Instruct-v0.2",
        max_tokens=20
    )
    print("Mistral v0.2 Success:", res.choices[0].message.content)
except Exception as e:
    print("Mistral v0.2 Error:", repr(e))

try:
    print("\nTesting Mistral v0.2 Text Gen...")
    res = client.text_generation(
        model="mistralai/Mistral-7B-Instruct-v0.2",
        prompt="[INST] What is 1+1? [/INST]"
    )
    print("Mistral v0.2 Gen Success:", res)
except Exception as e:
    print("Mistral v0.2 Gen Error:", repr(e))
