import os
import base64
import logging
from io import BytesIO
from PIL import Image
from openai import OpenAI

logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv('OPENAI_K1')
client = OpenAI(api_key=OPENAI_API_KEY)

async def process_image(file):
    """Process image and extract text using OpenAI Vision"""
    try:
        logger.debug(f"Starting image processing for file: {file.filename}")
        
        if not file or not file.filename:
            logger.error("No file provided")
            return None, "No image file provided"
            
        # Convert image to base64
        try:
            image = Image.open(BytesIO(file.read()))
            logger.debug(f"Image opened successfully. Size: {image.size}, Mode: {image.mode}")
            
            # Preprocess image
            image = image.convert('L').point(lambda x: 0 if x<128 else 255)
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            logger.debug(f"Image converted to base64. Length: {len(img_str)}")
        except Exception as img_error:
            logger.error(f"Image processing error: {str(img_error)}")
            return None, f"Image processing error: {str(img_error)}"

        # Call OpenAI Vision API
        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Extract all text from this image. Preserve formatting and structure."},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{img_str}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=4096
            )
            
            extracted_text = response.choices[0].message.content
            logger.debug(f"Extracted text length: {len(extracted_text)}")
            
            if not extracted_text:
                logger.error("No text found in OCR output")
                return None, "No text found in image"
                
            return extracted_text, None
            
        except Exception as ocr_error:
            logger.error(f"OCR failed: {str(ocr_error)}")
            return None, f"OCR failed: {str(ocr_error)}"
            
    except Exception as e:
        logger.error(f"Unexpected error in process_image: {str(e)}")
        return None, f"Image processing error: {str(e)}" 