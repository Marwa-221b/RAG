import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROVIDER = os.getenv("PROVIDER", "OPENAI")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


settings = Settings()


def get_llm_config():
    return {
        "PROVIDER": settings.PROVIDER,
        "OPENAI_API_KEY": settings.OPENAI_API_KEY,
        "GEMINI_API_KEY": settings.GEMINI_API_KEY
    }