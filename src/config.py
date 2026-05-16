from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ENV_FILE = PROJECT_ROOT / ".env"


class ConfigError(ValueError):
    """Raised when required configuration is missing or invalid."""


@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    openai_chat_model: str
    openai_embedding_model: str
    neo4j_uri: str
    neo4j_username: str
    neo4j_password: str
    neo4j_database: str
    docs_path: Path
    vector_index_name: str
    embedding_dimension: int
    chunk_size: int
    chunk_overlap: int
    top_k: int


def _required_str(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise ConfigError(f"Missing required environment variable: {name}")
    return value


def _int_value(name: str) -> int:
    value = _required_str(name)
    try:
        return int(value)
    except ValueError as exc:
        raise ConfigError(f"{name} must be an integer. Got: {value}") from exc


def _resolve_docs_path(value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return path


@lru_cache(maxsize=1)
def get_settings(env_file: Path | None = None) -> Settings:
    load_dotenv(env_file or DEFAULT_ENV_FILE, override=False)

    docs_path = _resolve_docs_path(_required_str("DOCS_PATH"))
    embedding_dimension = _int_value("EMBEDDING_DIMENSION")
    chunk_size = _int_value("CHUNK_SIZE")
    chunk_overlap = _int_value("CHUNK_OVERLAP")
    top_k = _int_value("TOP_K")

    if embedding_dimension <= 0:
        raise ConfigError("EMBEDDING_DIMENSION must be > 0")
    if chunk_size <= 0:
        raise ConfigError("CHUNK_SIZE must be > 0")
    if chunk_overlap < 0:
        raise ConfigError("CHUNK_OVERLAP must be >= 0")
    if chunk_overlap >= chunk_size:
        raise ConfigError("CHUNK_OVERLAP must be smaller than CHUNK_SIZE")
    if top_k <= 0:
        raise ConfigError("TOP_K must be > 0")
    if not docs_path.exists():
        raise ConfigError(f"DOCS_PATH does not exist: {docs_path}")
    if not docs_path.is_dir():
        raise ConfigError(f"DOCS_PATH must be a directory: {docs_path}")

    return Settings(
        openai_api_key=_required_str("OPENAI_API_KEY"),
        openai_chat_model=_required_str("OPENAI_CHAT_MODEL"),
        openai_embedding_model=_required_str("OPENAI_EMBEDDING_MODEL"),
        neo4j_uri=_required_str("NEO4J_URI"),
        neo4j_username=_required_str("NEO4J_USERNAME"),
        neo4j_password=_required_str("NEO4J_PASSWORD"),
        neo4j_database=_required_str("NEO4J_DATABASE"),
        docs_path=docs_path,
        vector_index_name=_required_str("VECTOR_INDEX_NAME"),
        embedding_dimension=embedding_dimension,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        top_k=top_k,
    )
