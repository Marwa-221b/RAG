import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROVIDER = os.getenv("PROVIDER", "OLLAMA")  # Changed default to OLLAMA

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")  


settings = Settings()


def get_llm_config():
    return {
        "PROVIDER": settings.PROVIDER,
        "OPENAI_API_KEY": settings.OPENAI_API_KEY,
        "GEMINI_API_KEY": settings.GEMINI_API_KEY,
        "DEEPSEEK_API_KEY": settings.DEEPSEEK_API_KEY,
        "OLLAMA_MODEL": settings.OLLAMA_MODEL  
    }