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
            response = requests.post(self.api_url, json=payload, timeout=30)
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
        Uses profile data when available to make mocks profile-aware.
        """
        # Try to load profile data (multi-perfil aware)
        try:
            import sys as _sys
            from pathlib import Path as _Path
            _pdir = _Path(__file__).parent.parent
            if str(_pdir) not in _sys.path:
                _sys.path.insert(0, str(_pdir))
            from utils.profile_loader import load_profile
            p = load_profile()
            profile_nome = p.get("nome", "seu negócio")
            profile_publico = p.get("publico_alvo", "seu público")
            profile_instagram = "@paznaconta"  # fallback
            for cfg_path in ["./perfis/perfis.json"]:
                try:
                    import json as _json
                    cfg = _json.loads(_Path(cfg_path).read_text(encoding="utf-8"))
                    for pp in cfg.get("perfis", []):
                        if pp.get("id") == cfg.get("ativo"):
                            profile_instagram = pp.get("icone", "") + " " + pp.get("nome", "")
                except Exception:
                    pass
        except Exception:
            profile_nome = "seu negócio"
            profile_publico = "seu público"
            profile_instagram = "@seuperfil"
        # Business consultation prompts (Consultor de Negócios OPB)
        if "consultor de negócios" in prompt.lower() or "plano estratégico" in prompt.lower() or "análise swot" in prompt.lower() or "calendário editorial" in prompt.lower() or "gestão de tempo" in prompt.lower() or "kpis" in prompt.lower() or "paz na conta" in prompt.lower():
            return """## Diagnóstico Estratégico

Visão Geral:
Seus 3 negocios (Paz na Conta, Toque de Paz, Caminho Vida) formam um ecossistema integrado com enorme potencial de sinergia.

Recomendacoes Prioritarias:

1. Paz na Conta (Financas Catolicas)
   - Fortaleça o conteudo educativo como porta de entrada
   - Crie programas de mentoria em grupo para escalar sem sacrificar qualidade
   - Estabeleça parcerias com paroquias e movimentos eclesiais

2. Toque de Paz (Musica com Proposito)
   - Desenvolva um metodo de ensino que integre tecnica musical e formacao espiritual
   - Produza material didatico exclusivo para musicos catolicos
   - Organize eventos sazonais (retiros musicais, oficinas de louvor)

3. Caminho Vida (Formacao Espiritual)
   - Crie trilhas de formacao progressiva (iniciante ao avancado)
   - Use o formato digital para alcance, presencial para profundidade
   - Integre conteudos dos outros dois negocios como estudos de caso

Principio Unificador:
Que cada negocio sirva aos outros, criando valor que nenhum alcancaria sozinho.

Buscai primeiro o Reino de Deus e a sua justica, e todas estas coisas vos serao acrescentadas. (Mt 6,33)"""
        elif "post educativo" in prompt.lower() or "educational" in prompt.lower():
            # Extract topic from prompt (best effort)
            topic = "organização"
            for sep in ["sobre", "topico:", "tópico:", "tema:"]:
                if sep in prompt.lower():
                    try:
                        after = prompt.lower().split(sep, 1)[1]
                        topic = after.split(".")[0].split("\n")[0].strip()[:60]
                        break
                    except Exception:
                        pass
            return f"""💡 DICA RÁPIDA: {topic}

Lembre-se de aplicar esses princípios no seu dia a dia:
1. Comece pequeno, mas comece hoje
2. Foque no progresso, não na perfeição
3. Celebre cada conquista, por menor que seja

Como isso se aplica à sua vida? Compartilhe nos comentários! 👇

#dicas #{profile_nome.split()[0].lower() if profile_nome else 'dica'} #{profile_publico.split()[0].lower() if profile_publico else 'dica'}"""

        elif "post inspirador" in prompt.lower() or "inspirational" in prompt.lower():
            return f"""✨ LEMBRE-SE:

Você já tem tudo que precisa para começar. Não espere pelo momento "perfeito" — ele não existe.

Cada grande jornada começa com um pequeno passo. O importante é dar esse passo hoje.

Acredite no seu processo e confie no seu tempo. Você está no caminho certo.

#fé #{profile_nome.split()[0].lower() if profile_nome else 'jornada'} #propósito"""
        
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