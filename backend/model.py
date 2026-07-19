import os
import requests

API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"

headers = {
    "Authorization": f"Bearer {os.environ.get('HF_API_TOKEN')}"
}


def generate_caption(image_path):
    with open(image_path, "rb") as image_file:
        data = image_file.read()

    response = requests.post(
        API_URL,
        headers=headers,
        data=data,
        timeout=60
    )

    if response.status_code != 200:
        raise Exception(f"Hugging Face API Error: {response.text}")

    result = response.json()

    if isinstance(result, list) and len(result) > 0:
        return result[0]["generated_text"]

    raise Exception(f"Unexpected response: {result}")