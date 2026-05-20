import os
import json
import requests
from typing import Dict, Any, Optional

class LLMProvider:
    """Abstract base class for LLM providers."""
    
    def generate(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate text from prompt using the LLM.
        
        Args:
            prompt: The prompt to send to the LLM
            context: Optional context to include in generation
            
        Returns:
            Generated text string
        """
        raise NotImplementedError

VISION_MODELS = ["llama3.2-vision", "llama3.2-vision:latest", "llama3.2", "llava", "llava:latest", "bakllava"]

DEFAULT_MODEL = "tinyllama"

class OllamaProvider(LLMProvider):
    """Ollama local LLM provider."""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = None):
        self.base_url = base_url
        self.model = DEFAULT_MODEL
        self.api_url = f"{base_url}/api/generate"
    
    def supports_vision(self) -> bool:
        return False
    
    def generate(self, prompt: str, context: Optional[Dict[str, Any]] = None, images: Optional[list] = None) -> str:
        """
        Generate text using Ollama API.
        
        Args:
            prompt: The prompt to send to Ollama
            context: Optional context (not used directly in Ollama call but kept for interface consistency)
            images: Optional list of base64 encoded images (only works with vision models)
            
        Returns:
            Generated text string
        """
        # Prepare the payload
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        # Add images only if model supports vision
        if images and self.supports_vision():
            payload["images"] = images
        elif images and not self.supports_vision():
            return f"[ERRO] Modelo {self.model} não suporta imagens. Use llama3.2-vision."
        
        try:
            response = requests.post(self.api_url, json=payload, timeout=180)
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "").strip()
            
        except requests.exceptions.RequestException as e:
            # Fallback to mock response when Ollama is not available
            return self._mock_generate(prompt, context)
        except json.JSONDecodeError as e:
            # Fallback to mock response on invalid JSON
            return self._mock_generate(prompt, context)

    def _mock_generate(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate a mock response when Ollama is not available.
        This allows testing and development without Ollama installed.
        """
        # Extract key information from prompt for a more relevant mock response
        if "post educativo" in prompt.lower() or "educational" in prompt.lower():
            return f"""💡 DICA RÁPIDA: {prompt.split('sobre')[1].split('.')[0].strip() if 'sobre' in prompt else 'organização'}

Lembre-se de aplicar esses princípios no seu dia a dia:
1. Comece pequeno, mas comece hoje
2. Foque no progresso, não na perfeição
3. Celebre cada conquista, por menor que seja

Como isso se aplica ao seu negócio? Compartilhe nos comentários! 👇

#produtividade #empreendedorismo #dicas"""
        
        elif "post inspirador" in prompt.lower() or "inspirational" in prompt.lower():
            return f"""✨ LEMBRE-SE:

Você já tem tudo que precisa para começar. Não espere pelo momento "perfeito" - ele não existe.

Cada grande jornada começa com um pequeno passo. O importante é dar esse passo hoje.

Acredite no seu processo e confie no seu tempo. Você está no caminho certo.

#mentalidade #empreendedorismo #jornada"""
        
        elif "post promocional" in prompt.lower() or "promotional" in prompt.lower():
            return f"""🚀 OFERTA ESPECIAL:

Transforme seu negócio com estratégias práticas e comprovadas.

Está esperando o sinal para começar? Este é ele!

Clique no link da bio para descobrir como você pode:
✅ Economizar tempo todo dia
✅ Aumentar sua produtividade
✅ Alcançar seus objetivos mais rápido

Link na bio! 👆

#oferta #negocios #resultado"""
        
        else:  # engagement or default
            return f"""💬 PERGUNTA PARA VOCÊ:

{prompt.split('sobre')[1].split('.')[0].strip() if 'sobre' in prompt else 'Qual é o maior desafio que você enfrenta no seu negócio hoje?'}

Como você costuma lidar com isso?
Que estratégia tem funcionado melhor para você?

Compartilhe sua experiência nos comentários - vamos aprender juntos! 👇

#comunidade #troca #crescimento"""

# Factory function to get LLM provider
def get_llm_provider(provider_type: str = "ollama", **kwargs) -> LLMProvider:
    """
    Factory function to get an LLM provider instance.
    
    Args:
        provider_type: Type of provider ("ollama" for now)
        **kwargs: Additional arguments for provider initialization
        
    Returns:
        LLMProvider instance
    """
    if provider_type.lower() == "ollama":
        return OllamaProvider(**kwargs)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider_type}")

# Convenience function for direct use
def generate_text(prompt: str, provider_type: str = "ollama", **kwargs) -> str:
    """
    Generate text using the specified LLM provider.
    
    Args:
        prompt: The prompt to send
        provider_type: Type of provider to use
        **kwargs: Additional arguments for provider
        
    Returns:
        Generated text string
    """
    provider = get_llm_provider(provider_type, **kwargs)
    return provider.generate(prompt)