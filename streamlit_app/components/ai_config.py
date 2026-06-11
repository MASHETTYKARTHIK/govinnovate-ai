"""AI configuration controls for the Streamlit sidebar."""

from __future__ import annotations

import streamlit as st

AI_MODES = ("Local Ollama", "BYOK Cloud API")
OLLAMA_MODELS = ("llama3", "mistral", "gemma")
CLOUD_PROVIDERS = ("OpenAI", "Gemini", "Anthropic", "Groq")
DEFAULT_OLLAMA_ENDPOINT = "http://localhost:11434"


def initialize_ai_state() -> None:
    """Initialize AI configuration state with sensible defaults."""
    st.session_state.setdefault("ai_inference_mode", AI_MODES[0])
    st.session_state.setdefault("ai_ollama_endpoint", DEFAULT_OLLAMA_ENDPOINT)
    st.session_state.setdefault("ai_ollama_model", OLLAMA_MODELS[0])
    st.session_state.setdefault("ai_cloud_provider", CLOUD_PROVIDERS[0])
    st.session_state.setdefault("ai_api_key", "")
    st.session_state.setdefault("ai_insight", "")


def render_ai_sidebar() -> None:
    """Render AI configuration controls in the app sidebar."""
    st.markdown("## AI Configuration")
    st.selectbox(
        "Inference Mode",
        AI_MODES,
        key="ai_inference_mode",
        help="Choose local ollama inference or a BYOK cloud provider.",
    )

    if st.session_state.ai_inference_mode == "Local Ollama":
        st.text_input(
            "Ollama Endpoint URL",
            key="ai_ollama_endpoint",
            value=st.session_state.ai_ollama_endpoint,
            help="Local Ollama endpoint for inference.",
        )
        st.selectbox(
            "Model",
            OLLAMA_MODELS,
            key="ai_ollama_model",
            help="Select the local Ollama model to use.",
        )
        st.caption("Using Local AI")
        if not st.session_state.ai_ollama_endpoint.strip():
            st.warning("Provide a local Ollama endpoint to enable inference.")
    else:
        st.selectbox(
            "Provider",
            CLOUD_PROVIDERS,
            key="ai_cloud_provider",
            help="Choose a BYOK cloud AI provider.",
        )
        st.text_input(
            "API key",
            type="password",
            key="ai_api_key",
            help="Your API key is stored only in the current Streamlit session.",
        )
        st.caption("Using Cloud AI Provider")
        if not st.session_state.ai_api_key:
            st.warning("Enter your provider API key to use cloud inference.")
