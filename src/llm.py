from __future__ import annotations

import os
from dataclasses import dataclass

import requests


@dataclass(frozen=True)
class LLMConfig:
    """Model provider settings used by generation."""

    provider: str
    model: str
    base_url: str
    api_key: str
    temperature: float
    timeout: int


def _float_env(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    try:
        return float(raw.strip())
    except ValueError:
        return default


def resolve_llm_config(
    *,
    provider: str | None = None,
    model: str | None = None,
    base_url: str | None = None,
    api_key: str | None = None,
    temperature: float | None = None,
    timeout: int = 120,
) -> LLMConfig:
    """Resolve LLM config from explicit args with env fallback."""

    resolved_provider = (provider or os.getenv("LLM_PROVIDER") or "ollama").strip()
    resolved_model = (
        model
        or os.getenv("LLM_MODEL")
        or os.getenv("OLLAMA_MODEL")
        or "llama3.2"
    ).strip()
    resolved_base_url = (
        base_url
        or os.getenv("LLM_BASE_URL")
        or os.getenv("OLLAMA_BASE_URL")
        or "http://localhost:11434"
    ).strip()
    resolved_api_key = (
        api_key
        if api_key is not None
        else (os.getenv("LLM_API_KEY") or os.getenv("OLLAMA_API_KEY") or "")
    ).strip()
    resolved_temperature = (
        temperature
        if temperature is not None
        else _float_env(
            "LLM_TEMPERATURE",
            _float_env("OLLAMA_TEMPERATURE", 0.1),
        )
    )

    return LLMConfig(
        provider=resolved_provider,
        model=resolved_model,
        base_url=resolved_base_url,
        api_key=resolved_api_key,
        temperature=resolved_temperature,
        timeout=timeout,
    )


def _build_ollama_chat_url(base_url: str) -> str:
    base = base_url.rstrip("/")
    if base.endswith("/api"):
        return f"{base}/chat"
    return f"{base}/api/chat"


def _build_ollama_tags_url(base_url: str) -> str:
    base = base_url.rstrip("/")
    if base.endswith("/api"):
        return f"{base}/tags"
    return f"{base}/api/tags"


def _ollama_headers(api_key: str) -> dict[str, str]:
    headers: dict[str, str] = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    return headers


def _normalize_ollama_name(name: str) -> tuple[str, str]:
    """Return (with_namespace, base_model_name_without_tag)."""
    cleaned = name.strip()
    without_namespace = cleaned.split("/")[-1]
    base = without_namespace.split(":")[0]
    return cleaned, base


def _ollama_model_available(requested_model: str, available_models: list[str]) -> bool:
    """Match Ollama models while tolerating namespace/tag variants."""
    requested_full, requested_base = _normalize_ollama_name(requested_model)

    for available in available_models:
        available_full, available_base = _normalize_ollama_name(available)
        if available_full == requested_full:
            return True
        if available_base == requested_base:
            return True
    return False


def check_provider_connectivity(config: LLMConfig) -> dict[str, object]:
    """Validate provider reachability and model visibility for current config."""

    provider = config.provider.lower().strip()
    if provider != "ollama":
        raise ValueError(
            f"Unsupported LLM provider '{config.provider}'. "
            "Currently supported: ollama."
        )

    url = _build_ollama_tags_url(config.base_url)
    try:
        response = requests.get(
            url,
            headers=_ollama_headers(config.api_key),
            timeout=config.timeout,
        )
    except requests.RequestException as exc:
        raise RuntimeError(
            f"Could not connect to Ollama at {config.base_url}. "
            "For local run `ollama serve`; for cloud verify base URL/API key."
        ) from exc

    if response.status_code != 200:
        raise RuntimeError(
            f"Ollama API error {response.status_code}: {response.text[:500]}"
        )

    payload = response.json()
    models = payload.get("models") or []
    model_names: list[str] = []
    for item in models:
        name = item.get("name")
        if isinstance(name, str) and name:
            model_names.append(name)

    model_available = _ollama_model_available(config.model, model_names)

    return {
        "provider": "ollama",
        "reachable": True,
        "model_available": model_available,
        "models_count": len(model_names),
    }


def _call_ollama_chat(question: str, context: str, config: LLMConfig) -> str:
    system_prompt = (
        "You are a CloudDesk CRM support assistant. "
        "Answer only using the provided context snippets. "
        "If the answer is not present in context, say you do not know. "
        "When you use information from context, cite snippet numbers like [1], [2]."
    )
    user_prompt = (
        f"Question:\n{question}\n\n"
        "Context snippets:\n"
        f"{context}\n\n"
        "Provide a concise, grounded answer with citations."
    )

    payload = {
        "model": config.model,
        "stream": False,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "options": {"temperature": config.temperature},
    }
    url = _build_ollama_chat_url(config.base_url)
    try:
        response = requests.post(
            url,
            json=payload,
            headers=_ollama_headers(config.api_key),
            timeout=config.timeout,
        )
    except requests.RequestException as exc:
        raise RuntimeError(
            f"Could not connect to Ollama at {config.base_url}. "
            "For local run `ollama serve`; for cloud verify base URL/API key."
        ) from exc

    if response.status_code != 200:
        raise RuntimeError(
            f"Ollama API error {response.status_code}: {response.text[:500]}"
        )

    data = response.json()
    message = (data.get("message") or {}).get("content", "").strip()
    if not message:
        raise RuntimeError("Ollama returned an empty response.")
    return message


def generate_answer(question: str, context: str, config: LLMConfig) -> str:
    """Dispatch generation to selected provider."""

    provider = config.provider.lower().strip()
    if provider == "ollama":
        return _call_ollama_chat(question, context, config)

    raise ValueError(
        f"Unsupported LLM provider '{config.provider}'. "
        "Currently supported: ollama."
    )
