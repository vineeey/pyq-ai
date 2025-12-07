"""
Ollama API client for local LLM inference.
"""
import logging
from typing import Optional
import httpx
from django.conf import settings

logger = logging.getLogger(__name__)


class OllamaClient:
    """Client for Ollama API (local LLM)."""
    
    def __init__(
        self,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        timeout: float = 120.0
    ):
        self.base_url = base_url or getattr(settings, 'OLLAMA_BASE_URL', 'http://localhost:11434')
        self.model = model or getattr(settings, 'OLLAMA_MODEL', 'llama3.2:3b')
        self.timeout = timeout
    
    def generate(
        self,
        prompt: str,
        max_tokens: int = 500,
        temperature: float = 0.7,
        stream: bool = False
    ) -> str:
        """
        Generate text using Ollama.
        
        Args:
            prompt: The prompt to send to the model
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            stream: Whether to stream the response
            
        Returns:
            Generated text
        """
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": stream,
                        "options": {
                            "num_predict": max_tokens,
                            "temperature": temperature,
                        }
                    }
                )
                response.raise_for_status()
                data = response.json()
                return data.get('response', '')
                
        except httpx.HTTPError as e:
            logger.error(f"Ollama API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Ollama generation failed: {e}")
            raise
    
    def is_available(self) -> bool:
        """Check if Ollama is running and model is available."""
        try:
            with httpx.Client(timeout=5.0) as client:
                response = client.get(f"{self.base_url}/api/tags")
                if response.status_code == 200:
                    models = response.json().get('models', [])
                    model_names = [m['name'] for m in models]
                    return self.model in model_names or self.model.split(':')[0] in [m.split(':')[0] for m in model_names]
            return False
        except Exception:
            return False
    
    def pull_model(self) -> bool:
        """Pull the model if not already available."""
        try:
            with httpx.Client(timeout=600.0) as client:  # Long timeout for model download
                response = client.post(
                    f"{self.base_url}/api/pull",
                    json={"name": self.model, "stream": False}
                )
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Failed to pull model: {e}")
            return False
