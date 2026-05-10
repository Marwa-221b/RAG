from abc import ABC, abstractmethod
from enum import Enum
# from google import genai
import google.generativeai as genai
from openai import OpenAI
import requests  # Add this import

class LLMEnums(Enum):
    GEMINI = "GEMINI"
    OPENAI = "OPENAI"
    OLLAMA = "OLLAMA"  # Add this

class LLMInterface(ABC):
    @abstractmethod
    def generate_text(self, prompt: str): pass

    @abstractmethod
    def embed_text(self, text: str): pass


class OllamaProvider(LLMInterface):
    def __init__(self, model_name="llama3.2", base_url="http://host.docker.internal:11434"):
        self.model_name = model_name
        self.base_url = base_url
        
    def generate_text(self, prompt: str):
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            }
        )
        if response.status_code == 200:
            return response.json()["response"]
        else:
            raise Exception(f"Ollama error: {response.text}")
    
    def embed_text(self, text: str):
        response = requests.post(
            f"{self.base_url}/api/embeddings",
            json={
                "model": self.model_name,
                "prompt": text
            }
        )
        if response.status_code == 200:
            return response.json()["embedding"]
        else:
            raise Exception(f"Ollama embedding error: {response.text}")


# Keep your existing providers (GeminiProvider, OpenAIProvider)...

class LLMProviderFactory:
    def __init__(self, config):
        self.config = config or {}

    def create(self, provider_name: str):
        if not provider_name:
            provider_name = "OLLAMA"
        p_name = provider_name.upper()

   
        
        # Add Ollama support
        if p_name == LLMEnums.OLLAMA.value:
            return OllamaProvider(
                model_name=self.config.get("OLLAMA_MODEL", "llama3.2")
            )
        raise ValueError(f"Unsupported provider: {provider_name}")