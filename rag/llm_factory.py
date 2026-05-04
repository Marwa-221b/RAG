from abc import ABC, abstractmethod
from enum import Enum
import google.genai as genai 
from openai import OpenAI 

class LLMEnums(Enum):
    GEMINI = "GEMINI"
    OPENAI = "OPENAI"

class LLMInterface(ABC):
    @abstractmethod
    def generate_text(self, prompt: str): pass

    @abstractmethod
    def embed_text(self, text: str): pass


class GeminiProvider(LLMInterface):
    def __init__(self, api_key, model_id="gemini-1.5-flash"):
        self.client = genai.Client(api_key=api_key)
        self.model_id = model_id

    def generate_text(self, prompt: str):
        response = self.client.models.generate_content(model=self.model_id, contents=prompt)
        return response.text

    def embed_text(self, text: str):
        result = self.client.models.embed_content(model="text-embedding-004", contents=text)
        return result.embeddings[0].values


class OpenAIProvider(LLMInterface):
    def __init__(self, api_key, model_id="gpt-3.5-turbo"):
        self.client = OpenAI(api_key=api_key)
        self.model_id = model_id

    def generate_text(self, prompt: str):
        response = self.client.chat.completions.create(
            model=self.model_id,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    def embed_text(self, text: str):
        response = self.client.embeddings.create(input=[text], model="text-embedding-3-small")
        return response.data[0].embedding


class LLMProviderFactory:
    def __init__(self, config):
        self.config = config

    def create(self, provider_name: str):
        p_name = provider_name.upper()
        
        if p_name == LLMEnums.GEMINI.value:
            return GeminiProvider(api_key=self.config.get("GEMINI_API_KEY"))
        
        elif p_name == LLMEnums.OPENAI.value:
            return OpenAIProvider(api_key=self.config.get("OPENAI_API_KEY"))
            
        else:
            raise ValueError(f"Provider {p_name} is not supported in the Remote Factory.")