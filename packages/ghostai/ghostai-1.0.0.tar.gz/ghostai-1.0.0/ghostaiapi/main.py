import requests
import json
import base64
from PIL import Image
import io

def chat(api_key, model, message):
    url = "https://api.ghostai.me/send_message"
    payload = {
        "api_key": api_key,
        "model": model,
        "message": message
    }

    airesponse = requests.post(url, json=payload)
    response = airesponse.text
    return response

def extract_base64_image_data(response):
    try:
        json_response = json.loads(response)
        image_data = json_response.get("image_response")
        return image_data
    except Exception as e:
        print("An error occurred while extracting image data:", e)
        return None

def decode_base64_image(base64_string):
    try:
        # Decode base64 and create image from bytes
        image_bytes = base64.b64decode(base64_string)
        img = Image.open(io.BytesIO(image_bytes))
        return img
    except Exception as e:
        print("An error occurred while decoding the image:", e)
        return None

def chat_with_image(api_key, model, message):
    response = chat(api_key, model, message)
    if response:
        image_data = extract_base64_image_data(response)
        if image_data:
            decoded_img = decode_base64_image(image_data)
            return decoded_img
    else:
        print("No image response received.")
        return None
