import requests, os
from dotenv import load_dotenv
load_dotenv(".env")
headers = {"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"}

def test_model(model_name):
    url = f"https://api-inference.huggingface.co/models/{model_name}"
    res = requests.get(url, headers=headers)
    print(f"[{res.status_code}] {model_name}: {res.text[:100]}")

test_model("Salesforce/blip-image-captioning-base")
test_model("Salesforce/blip-image-captioning-large")
test_model("nlpconnect/vit-gpt2-image-captioning")
test_model("mistralai/Mistral-7B-Instruct-v0.1")
test_model("mistralai/Mistral-7B-Instruct-v0.2")
test_model("mistralai/Mistral-7B-Instruct-v0.3")
test_model("mistralai/Mixtral-8x7B-Instruct-v0.1")
test_model("meta-llama/Llama-3.2-3B-Instruct")
