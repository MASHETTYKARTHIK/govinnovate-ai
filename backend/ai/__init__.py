"""AI inference utilities for GovInnovate AI."""

from backend.ai.ollama_client import generate_with_ollama
from backend.ai.providers import generate_response

__all__ = ["generate_with_ollama", "generate_response"]
