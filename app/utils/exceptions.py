from functools import wraps
from quart import jsonify

def handle_api_error(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except APIRequestError as e:
            return jsonify({"error": str(e)}), 502
        except InvalidResponseFormat as e:
            return jsonify({"error": str(e)}), 502
        except ValidationError as e:
            return jsonify({"error": str(e)}), 422
        except Exception as e:
            return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    return wrapper

class APIRequestError(Exception):
    """Base exception for API request failures"""
    def __init__(self, message: str, status_code: int = None):
        self.status_code = status_code
        super().__init__(message)

class InvalidResponseFormat(Exception):
    """Exception for malformed API responses"""
    def __init__(self, message: str = "Invalid response format from API"):
        super().__init__(message)

class ValidationError(Exception):
    """Exception for data validation failures"""
    def __init__(self, message: str = "Data validation failed"):
        super().__init__(message)

class ServiceUnavailableError(Exception):
    """Exception for service availability issues"""
    def __init__(self, message: str = "Service temporarily unavailable"):
        super().__init__(message)

