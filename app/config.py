import os

class Config:
    DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions")
    DEEPSEEK_KEY = os.getenv("DEEPSEEK_K1")
    REDIS_URL = os.getenv("REDIS_URL", "redis-18448.c328.europe-west3-1.gce.redns.redis-cloud.com")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 18448))
    REDIS_USERNAME = os.getenv("REDIS_USERNAME", "default")
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
    MODEL_NAME = os.getenv("MODEL_NAME", "deepseek-chat")
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 30))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", 2000))
    TEMPERATURE = float(os.getenv("TEMPERATURE", 0.3))

config = Config()
