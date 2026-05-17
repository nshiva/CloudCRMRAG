from __future__ import annotations

import argparse
from dataclasses import dataclass

from src.config import get_settings
from src.runtime import (
    connect_neo4j,
    ensure_vector_index_dimension,
    load_embedding_model,
)


@dataclass(frozen=True)
class SearchResult:
    """One retrieved chunk with rank, score, and metadata."""

    rank: int
    score: float
    chunk_id: str
    doc_id: str
    text: str
    chunk_metadata: dict[str, object]
    document_metadata: dict[str, object]


def embed_query(embedding_model, query: str) -> list[float]:
    """Embed a user query into a normalized vector for similarity search."""

    vector = embedding_model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )[0]
    return vector.tolist()


def query_chunks(
    session,
    *,
    index_name: str,
    top_k: int,
    query_embedding: list[float],
    doc_type: str | None,
    module: str | None,
) -> list[SearchResult]:
    """Run vector search in Neo4j and map rows into SearchResult objects."""

    escaped_index_name = index_name.replace("`", "")
    search_query = f"""
    MATCH (node:Chunk)
    SEARCH node IN (
      VECTOR INDEX `{escaped_index_name}`
      FOR $query_embedding
      LIMIT $top_k
    ) SCORE AS score
    WHERE ($doc_type IS NULL OR node.doc_type = $doc_type)
      AND ($module IS NULL OR node.module = $module)
    OPTIONAL MATCH (d:Document {{doc_id: node.doc_id}})
    RETURN
      score,
      node.chunk_id AS chunk_id,
      node.doc_id AS doc_id,
      node.text AS text,
      properties(node) AS chunk_metadata,
      d{{.*}} AS document_metadata
    ORDER BY score DESC
    """

    try:
        records = session.run(
            search_query,
            top_k=top_k,
            query_embedding=query_embedding,
            doc_type=doc_type,
            module=module,
        ).data()
    except Exception as exc:
        # Fallback for Neo4j versions that do not support the SEARCH clause yet.
        error_text = str(exc)
        search_not_supported = (
            "Invalid input 'SEARCH'" in error_text
            or "SEARCH" in error_text and "syntax error" in error_text
        )
        if not search_not_supported:
            raise

        records = session.run(
            """
            CALL db.index.vector.queryNodes($index_name, $top_k, $query_embedding)
            YIELD node, score
            WHERE ($doc_type IS NULL OR node.doc_type = $doc_type)
              AND ($module IS NULL OR node.module = $module)

            OPTIONAL MATCH (d:Document {doc_id: node.doc_id})
            RETURN
              score,
              node.chunk_id AS chunk_id,
              node.doc_id AS doc_id,
              node.text AS text,
              properties(node) AS chunk_metadata,
              d{.*} AS document_metadata
            ORDER BY score DESC
            """,
            index_name=index_name,
            top_k=top_k,
            query_embedding=query_embedding,
            doc_type=doc_type,
            module=module,
        ).data()

    results: list[SearchResult] = []
    for i, row in enumerate(records, start=1):
        chunk_metadata = row.get("chunk_metadata") or {}
        chunk_metadata.pop("embedding", None)
        chunk_metadata.pop("text", None)
        results.append(
            SearchResult(
                rank=i,
                score=float(row["score"]),
                chunk_id=row["chunk_id"],
                doc_id=row["doc_id"],
                text=row["text"] or "",
                chunk_metadata=chunk_metadata,
                document_metadata=row.get("document_metadata") or {},
            )
        )
    return results


def print_results(results: list[SearchResult], max_text_chars: int) -> None:
    """Pretty-print retrieval results for CLI usage."""

    if not results:
        print("No matching chunks found.")
        return

    print(f"Found {len(results)} chunk(s):")
    for result in results:
        snippet = result.text[:max_text_chars]
        if len(result.text) > max_text_chars:
            snippet += "..."

        print("-" * 80)
        print(f"rank={result.rank} score={result.score:.4f}")
        print(f"doc_id={result.doc_id} chunk_id={result.chunk_id}")
        print(f"doc_type={result.chunk_metadata.get('doc_type', '')}")
        print(f"module={result.chunk_metadata.get('module', '')}")
        print(f"source_path={result.chunk_metadata.get('__source_path', '')}")
        print("text:")
        print(snippet)


def main() -> None:
    parser = argparse.ArgumentParser(description="Retrieve top-k chunks from Neo4j vector index.")
    parser.add_argument("--query", required=True, help="User query text.")
    parser.add_argument(
        "--top-k",
        type=int,
        default=None,
        help="Number of chunks to return. Defaults to TOP_K from .env.",
    )
    parser.add_argument(
        "--doc-type",
        default=None,
        help="Optional filter by doc_type (for example: troubleshooting_guide).",
    )
    parser.add_argument(
        "--module",
        default=None,
        help="Optional filter by module (for example: Authentication).",
    )
    parser.add_argument(
        "--max-text-chars",
        type=int,
        default=450,
        help="Max characters shown per chunk text in CLI output.",
    )
    args = parser.parse_args()

    settings = get_settings()
    top_k = args.top_k or settings.top_k

    print(f"Embedding model: {settings.embedding_model}")
    embedding_model = load_embedding_model(settings.embedding_model)
    query_embedding = embed_query(embedding_model, args.query)

    driver, connected_uri = connect_neo4j(
        uri=settings.neo4j_uri,
        username=settings.neo4j_username,
        password=settings.neo4j_password,
    )
    print(f"Neo4j URI used: {connected_uri}")
    print(f"Vector index: {settings.vector_index_name}")
    print(f"top_k={top_k}")

    with driver:
        with driver.session(database=settings.neo4j_database) as session:
            ensure_vector_index_dimension(
                session=session,
                index_name=settings.vector_index_name,
                expected_dimension=settings.embedding_dimension,
            )

            results = query_chunks(
                session=session,
                index_name=settings.vector_index_name,
                top_k=top_k,
                query_embedding=query_embedding,
                doc_type=args.doc_type,
                module=args.module,
            )

    print_results(results, max_text_chars=max(50, args.max_text_chars))


if __name__ == "__main__":
    main()
