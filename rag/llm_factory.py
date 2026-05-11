from abc import ABC, abstractmethod
from enum import Enum
from google import genai
from openai import OpenAI
import requests  # Add this import

class LLMEnums(Enum):
    GEMINI = "GEMINI"
    OPENAI = "OPENAI"
    OLLAMA = "OLLAMA"  # Add this
    MOCK   = "MOCK"
class LLMInterface(ABC):
    @abstractmethod
    def generate_text(self, prompt: str): pass

    @abstractmethod
    def embed_text(self, text: str): pass


class OllamaProvider(LLMInterface):
    def __init__(self, model_name="llama3.2", base_url="http://localhost:11434"):
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
                    "temperature": 0.1,
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
class GeminiProvider(LLMInterface):
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        from google import genai
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def generate_text(self, prompt: str):
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        return response.text

    def embed_text(self, text: str):
        raise NotImplementedError("Use sentence-transformers for embeddings")


class OpenAIProvider(LLMInterface):
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate_text(self, prompt: str):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        return response.choices[0].message.content

    def embed_text(self, text: str):
        raise NotImplementedError("Use sentence-transformers for embeddings")
    
class LLMProviderFactory:
    def __init__(self, config):
        self.config = config or {}

    def create(self, provider_name: str):
        p_name = provider_name.upper()
     
        # Add Ollama support
        if p_name == LLMEnums.OLLAMA.value:
            return OllamaProvider(
                model_name=self.config.get("OLLAMA_MODEL", "llama3.2")
            )
        if p_name == LLMEnums.GEMINI.value:
         return GeminiProvider(api_key=self.config.get("GEMINI_API_KEY"))
        if p_name == LLMEnums.OPENAI.value:
         return OpenAIProvider(api_key=self.config.get("OPENAI_API_KEY"))
        if p_name == LLMEnums.MOCK.value:
         return MockProvider()
        raise ValueError(f"Unsupported provider: {provider_name}")
    



class MockProvider(LLMInterface):
    def generate_text(self, prompt: str):
        return "[MOCK] This is a test response. Real LLM not configured."
    def embed_text(self, text: str):
        return []
    


