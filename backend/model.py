import os
import requests

API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"

headers = {
    "Authorization": f"Bearer {os.environ.get('HF_API_TOKEN')}"
}

def generate_caption(image_path):
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    response = requests.post(
        API_URL,
        headers=headers,
        data=image_bytes,
        timeout=60
    )

    print("Status Code:", response.status_code)
    print("Response Body:", response.text)

    if response.status_code != 200:
        raise Exception(
            f"Hugging Face API Error ({response.status_code}): {response.text}"
        )

    result = response.json()

    if isinstance(result, list) and len(result) > 0:
        return result[0]["generated_text"]

    raise Exception(f"Unexpected response: {result}")