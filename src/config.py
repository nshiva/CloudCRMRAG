from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ENV_FILE = PROJECT_ROOT / ".env"
CACHE_DIR = PROJECT_ROOT / ".cache"
MODEL_CACHE_DIR = CACHE_DIR / "models"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
MODEL_CACHE_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("XDG_CACHE_HOME", str(CACHE_DIR))
os.environ.setdefault("HF_HOME", str(MODEL_CACHE_DIR))
os.environ.setdefault(
    "SENTENCE_TRANSFORMERS_HOME",
    str(MODEL_CACHE_DIR / "sentence_transformers"),
)


class ConfigError(ValueError):
    """Raised when required configuration is missing or invalid."""


@dataclass(frozen=True)
class Settings:
    """Runtime configuration shared across ingestion, indexing, and retrieval."""

    embedding_model: str
    neo4j_uri: str
    neo4j_username: str
    neo4j_password: str
    neo4j_database: str
    docs_path: Path
    vector_index_name: str
    embedding_dimension: int
    top_k: int


def _required_str(name: str) -> str:
    """Return non-empty env var value or raise ConfigError."""

    value = os.getenv(name, "").strip()
    if not value:
        raise ConfigError(f"Missing required environment variable: {name}")
    return value


def _optional_str(name: str, default: str = "") -> str:
    """Return env var value if present, otherwise a default."""

    value = os.getenv(name)
    if value is None:
        return default
    value = value.strip()
    if not value:
        return default
    return value


def _int_value(name: str, default: int | None = None) -> int:
    """Parse an integer env var with optional default fallback."""

    raw = os.getenv(name)
    if raw is None or not raw.strip():
        if default is None:
            raise ConfigError(f"Missing required environment variable: {name}")
        return default

    value = raw.strip()
    try:
        return int(value)
    except ValueError as exc:
        raise ConfigError(f"{name} must be an integer. Got: {value}") from exc


def _resolve_docs_path(value: str) -> Path:
    """Resolve docs path relative to project root when needed."""

    path = Path(value)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return path


@lru_cache(maxsize=1)
def get_settings(env_file: Path | None = None) -> Settings:
    """Load and validate app settings from .env and process environment."""

    load_dotenv(env_file or DEFAULT_ENV_FILE, override=True)

    docs_path = _resolve_docs_path(_required_str("DOCS_PATH"))
    embedding_dimension = _int_value("EMBEDDING_DIMENSION", default=384)
    top_k = _int_value("TOP_K", default=5)

    if embedding_dimension <= 0:
        raise ConfigError("EMBEDDING_DIMENSION must be > 0")
    if top_k <= 0:
        raise ConfigError("TOP_K must be > 0")
    if not docs_path.exists():
        raise ConfigError(f"DOCS_PATH does not exist: {docs_path}")
    if not docs_path.is_dir():
        raise ConfigError(f"DOCS_PATH must be a directory: {docs_path}")

    return Settings(
        embedding_model=_optional_str(
            "EMBEDDING_MODEL",
            default="sentence-transformers/all-MiniLM-L6-v2",
        ),
        neo4j_uri=_required_str("NEO4J_URI"),
        neo4j_username=_required_str("NEO4J_USERNAME"),
        neo4j_password=_required_str("NEO4J_PASSWORD"),
        neo4j_database=_required_str("NEO4J_DATABASE"),
        docs_path=docs_path,
        vector_index_name=_required_str("VECTOR_INDEX_NAME"),
        embedding_dimension=embedding_dimension,
        top_k=top_k,
    )
