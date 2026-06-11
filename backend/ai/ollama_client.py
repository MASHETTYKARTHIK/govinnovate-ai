"""Local Ollama inference client for GovInnovate AI."""

from __future__ import annotations

import requests
from requests.exceptions import RequestException, Timeout

DEFAULT_OLLAMA_ENDPOINT = "http://localhost:11434"


def generate_with_ollama(
    prompt: str,
    model: str,
    endpoint: str = DEFAULT_OLLAMA_ENDPOINT,
    timeout: int = 120,
) -> str:
    """Send a prompt to a local Ollama inference endpoint and return plain text."""

    url = f"{endpoint.rstrip('/')}/api/generate"

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }

    try:
        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=timeout,
        )

        response.raise_for_status()

        data = response.json()

    except Timeout as exc:
        raise ConnectionError("Ollama request timed out") from exc

    except RequestException as exc:
        raise ConnectionError(
            f"Failed to reach Ollama endpoint at {endpoint}: {exc}"
        ) from exc

    if not isinstance(data, dict):
        raise ValueError("Unexpected Ollama response format")

    text = data.get("response", "")

    if not text or not isinstance(text, str):
        raise ValueError("Ollama returned an invalid response payload")

    return text.strip()
