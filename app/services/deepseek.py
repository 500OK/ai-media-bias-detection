import json
import httpx
import re
from app.config import config
from app.utils.exceptions import APIRequestError, InvalidResponseFormat
from app.schemas.analysis import BiasResultList  # Ensure this import exists

class DeepSeekAnalyzer:
    def __init__(self, client: httpx.AsyncClient = None):
        self.client = client or httpx.AsyncClient(timeout=config.REQUEST_TIMEOUT)
        self.headers = {
            "Authorization": f"Bearer {config.DEEPSEEK_KEY}",
            "Content-Type": "application/json"
        }

    async def analyze_text(self, text: str, prompt: str) -> dict:
        payload = self._build_payload(text, prompt)
        try:
            response = await self.client.post(
                config.DEEPSEEK_API_URL,
                json=payload,
                headers=self.headers
            )
            response.raise_for_status()
            return self._parse_response(response.json())
        except httpx.HTTPStatusError as e:
            raise APIRequestError(f"API request failed: {e.response.status_code}") from e

    def _build_payload(self, text: str, prompt: str) -> dict:
        return {
            "model": config.MODEL_NAME,
            "messages": [{
                "role": "user",
                "content": f"{prompt}\n\nNews Text:\n{text}"
            }],
            "temperature": config.TEMPERATURE,
            "max_tokens": config.MAX_TOKENS,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0
        }

    def _parse_response(self, response: dict) -> dict:
        try:
            # Extract raw content from API response
            content = response['choices'][0]['message']['content']

            # Clean and normalize the JSON string
            content = self._clean_json_content(content)

            # Parse and validate the response format
            return self._validate_response_structure(content)

        except (KeyError, json.JSONDecodeError) as e:
            # Log raw response for debugging
            print(f"Failed to parse response. Raw content: {content}")
            raise InvalidResponseFormat("Invalid API response structure") from e

    def _clean_json_content(self, content: str) -> str:
        """Clean and normalize potential JSON formats from API response"""
        # Remove JSON code block markers if present
        content = re.sub(r'^```json|```$', '', content, flags=re.IGNORECASE)

        # Remove escape characters and control characters
        content = content.strip().replace("\\", "")
        content = re.sub(r'[\x00-\x1F]+', '', content)

        return content

    def _validate_response_structure(self, content: str) -> dict:
        """Validate and normalize the response structure"""
        try:
            # First try parsing as direct list
            parsed = json.loads(content)

            # If parsed as list, wrap in results key
            if isinstance(parsed, list):
                parsed = {"results": parsed}

            # Validate against our schema
            validated = BiasResultList(**parsed)
            return validated.model_dump()

        except (json.JSONDecodeError, TypeError) as e:
            print(f"JSON parsing failed. Content: {content}")
            raise InvalidResponseFormat("Invalid JSON structure") from e
        except Exception as e:
            print(f"Validation failed. Content: {content}")
            raise InvalidResponseFormat("Response validation error") from e