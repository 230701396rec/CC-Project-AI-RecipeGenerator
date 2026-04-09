import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv(".env")
client = InferenceClient(token=os.getenv("HF_API_KEY"))

try:
    print("Testing Default Image to Text...")
    res = client.image_to_text(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg/800px-Good_Food_Display_-_NCI_Visuals_Online.jpg"
    )
    print("Image to Text Success:", res.generated_text)
except Exception as e:
    print("Image to Text Error:", repr(e))

try:
    print("\nTesting Default Chat Completion...")
    res = client.chat_completion(
        messages=[{"role":"user", "content":"Extract ingredients from: A warm bowl of potato soup with salt. Respond strictly in comma separated values."}],
        max_tokens=60
    )
    print("Chat Success:", res.choices[0].message.content)
except Exception as e:
    print("Chat Error:", repr(e))
