# pylint: disable=no-member
"""Cloud provider abstraction for BYOK AI inference."""

from __future__ import annotations

from typing import Literal

CloudProvider = Literal["OpenAI", "Gemini", "Anthropic", "Groq"]

DEFAULT_PROVIDER_MODELS: dict[CloudProvider, str] = {
    "OpenAI": "gpt-4o-mini",
    "Gemini": "gemini-pro",
    "Anthropic": "claude-3.5",
    "Groq": "groq-1",
}


def generate_response(
    prompt: str,
    provider: CloudProvider,
    api_key: str,
    model: str | None = None,
) -> str:
    """Generate a text response from a BYOK cloud provider."""
    selected_model = model or DEFAULT_PROVIDER_MODELS[provider]
    if provider == "OpenAI":
        return _generate_openai(prompt, api_key, selected_model)
    if provider == "Gemini":
        return _generate_gemini(prompt, api_key, selected_model)
    if provider == "Anthropic":
        return _generate_anthropic(prompt, api_key, selected_model)
    if provider == "Groq":
        return _generate_groq(prompt, api_key, selected_model)
    raise ValueError(f"Unsupported provider: {provider}")


def _generate_openai(prompt: str, api_key: str, model: str) -> str:
    try:
        import openai
    except ImportError as exc:
        raise ImportError("OpenAI support requires the openai package") from exc

    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.7,
    )
    choices = getattr(response, "choices", None) or response.get("choices", [])
    if not choices:
        raise ValueError("OpenAI returned no choices")
    message = choices[0].get("message") if isinstance(choices[0], dict) else None
    text = None
    if isinstance(message, dict):
        text = message.get("content")
    if not text:
        text = getattr(choices[0], "text", None)
    if not isinstance(text, str):
        raise ValueError("Invalid OpenAI response format")
    return text.strip()


def _generate_gemini(prompt: str, api_key: str, model: str) -> str:
    try:
        import google.generativeai as genai
    except ImportError as exc:
        raise ImportError(
            "Gemini support requires google-generativeai package"
        ) from exc

    genai.configure(api_key=api_key)
    response = genai.generate_text(
        model=model,
        prompt=prompt,
        max_output_tokens=300,
    )
    text = (
        getattr(response, "text", None) or response.get("text")
        if isinstance(response, dict)
        else None
    )
    if not isinstance(text, str):
        raise ValueError("Invalid Gemini response format")
    return text.strip()


def _generate_anthropic(prompt: str, api_key: str, model: str) -> str:
    try:
        import anthropic
    except ImportError as exc:
        raise ImportError("Anthropic support requires the anthropic package") from exc

    client = anthropic.Client(api_key=api_key)
    prompt_text = f"{anthropic.HUMAN_PROMPT}{prompt}{anthropic.AI_PROMPT}"
    response = client.completions.create(
        model=model,
        prompt=prompt_text,
        max_tokens_to_sample=300,
        temperature=0.7,
    )
    text = (
        getattr(response, "completion", None) or response.get("completion")
        if isinstance(response, dict)
        else None
    )
    if not isinstance(text, str):
        raise ValueError("Invalid Anthropic response format")
    return text.strip()


def _generate_groq(prompt: str, api_key: str, model: str) -> str:
    try:
        from groq import GroqClient
    except ImportError as exc:
        raise ImportError("Groq support requires the groq package") from exc

    client = GroqClient(api_key=api_key)
    response = client.generate(
        model=model,
        prompt=prompt,
        max_output_tokens=300,
    )
    text = (
        getattr(response, "text", None) or response.get("text")
        if isinstance(response, dict)
        else None
    )
    if not isinstance(text, str):
        raise ValueError("Invalid Groq response format")
    return text.strip()
