import os
import requests
from io import BytesIO
from PIL import Image
import base64
from quart import jsonify

DEEPSEEK_OCR_URL = 'https://api.deepseek.com/v1/ocr'
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_K1')

async def process_image(file):
    """Process image and extract text using DeepSeek OCR"""
    try:
        # Validate image
        if not file or not file.filename:
            return None, "No image file provided"
            
        # Convert image to base64
        image = Image.open(BytesIO(file.read()))
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        # Call DeepSeek OCR
        response = requests.post(
            DEEPSEEK_OCR_URL,
            headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
            json={"image": img_str}
        )
        
        if response.status_code != 200:
            return None, f"OCR failed: {response.text}"
            
        extracted_text = response.json().get('text', '')
        
        if not extracted_text:
            return None, "No text found in image"
            
        return extracted_text, None
        
    except Exception as e:
        return None, f"Image processing error: {str(e)}" 