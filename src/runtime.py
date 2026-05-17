from __future__ import annotations

# Import config for cache/env initialization side effects before model loading.
from src import config as _config
from neo4j import GraphDatabase


def load_embedding_model(model_name: str):
    """Load sentence-transformers model with project cache env already initialized."""

    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(model_name)


def connect_neo4j(uri: str, username: str, password: str):
    """Connect to Neo4j with automatic ssc fallback for TLS/routing edge cases."""

    candidates = [uri]
    if uri.startswith("neo4j+s://"):
        candidates.append("neo4j+ssc://" + uri.split("://", 1)[1])

    last_error = None
    for candidate in candidates:
        driver = GraphDatabase.driver(candidate, auth=(username, password))
        try:
            driver.verify_connectivity()
            return driver, candidate
        except Exception as exc:
            driver.close()
            last_error = exc

    raise last_error


def get_vector_index_dimension(session, index_name: str) -> int | None:
    """Return configured vector index dimension, or None if index is missing."""

    row = session.run(
        """
        SHOW INDEXES YIELD name, type, options
        WHERE type = 'VECTOR' AND name = $index_name
        RETURN options['indexConfig']['vector.dimensions'] AS dimensions
        """,
        index_name=index_name,
    ).single()
    if row is None or row["dimensions"] is None:
        return None
    return int(row["dimensions"])


def ensure_vector_index_dimension(session, index_name: str, expected_dimension: int) -> int:
    """Ensure vector index exists and matches expected embedding dimension."""

    index_dimension = get_vector_index_dimension(session, index_name)
    if index_dimension is None:
        raise ValueError(
            f"Vector index '{index_name}' was not found. Run indexing first."
        )
    if int(index_dimension) != int(expected_dimension):
        raise ValueError(
            f"Vector index '{index_name}' dimension is {index_dimension}, "
            f"but EMBEDDING_DIMENSION is {expected_dimension}. "
            "Drop/recreate index and reindex chunk embeddings."
        )
    return int(index_dimension)
