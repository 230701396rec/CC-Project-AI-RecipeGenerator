import requests, os
from dotenv import load_dotenv
load_dotenv(".env")
headers = {"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"}

def test_model_post(model_name):
    url = f"https://router.huggingface.co/hf-inference/models/{model_name}"
    res = requests.post(url, headers=headers, json={"inputs": "What is 1+1?"})
    print(f"[{res.status_code}] {model_name}")
    try:
        print(f"Data: {res.json()}")
    except:
        print(f"Text: {res.text[:100]}")

test_model_post("Salesforce/blip-image-captioning-base")
test_model_post("Salesforce/blip-image-captioning-large")
test_model_post("mistralai/Mistral-7B-Instruct-v0.2")
test_model_post("mistralai/Mistral-7B-Instruct-v0.3")
test_model_post("meta-llama/Llama-3.2-3B-Instruct")
test_model_post("HuggingFaceH4/zephyr-7b-beta")
