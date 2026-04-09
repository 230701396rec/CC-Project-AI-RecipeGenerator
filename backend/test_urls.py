import requests, os
from dotenv import load_dotenv
load_dotenv(".env")
headers = {"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"}

def check(url, payload):
    res = requests.post(url, headers=headers, json=payload)
    print(f"URL: {url} -> Status: {res.status_code}")
    if res.status_code == 200:
        print("SUCCESS")
    else:
        print(f"Error: {res.text[:100]}")

base_model = "mistralai/Mistral-7B-Instruct-v0.3"
urls = [
    f"https://api-inference.huggingface.co/models/{base_model}",
    f"https://router.huggingface.co/hf-inference/models/{base_model}",
    f"https://router.huggingface.co/models/{base_model}",
    f"https://api-inference.huggingface.co/pipeline/text-generation/{base_model}"
]

for u in urls:
    check(u, {"inputs": "What is 1+1?"})

print("---- BLIP -----")
blip_model = "Salesforce/blip-image-captioning-base"
blip_urls = [
    f"https://api-inference.huggingface.co/models/{blip_model}",
    f"https://router.huggingface.co/hf-inference/models/{blip_model}",
    f"https://router.huggingface.co/models/{blip_model}",
    f"https://api-inference.huggingface.co/pipeline/image-to-text/{blip_model}"
]
for u in blip_urls:
    # BLIP is image, so we pass dummy data as json inputs but the url is what matters for 404
    check(u, {"inputs": "fake"})

