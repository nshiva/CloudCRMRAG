from __future__ import annotations

import argparse
from collections.abc import Iterable

from tqdm import tqdm

from src.config import get_settings
from src.ingest import DocumentChunk, load_document_chunks
from src.runtime import connect_neo4j, get_vector_index_dimension, load_embedding_model


def batched(items: list[DocumentChunk], batch_size: int) -> Iterable[list[DocumentChunk]]:
    """Yield fixed-size chunk batches for embedding and upsert."""

    for i in range(0, len(items), batch_size):
        yield items[i : i + batch_size]


def ensure_schema(session, index_name: str, embedding_dimension: int) -> None:
    """Ensure constraints exist and vector index dimension matches current model."""

    session.run(
        """
        CREATE CONSTRAINT document_doc_id IF NOT EXISTS
        FOR (d:Document)
        REQUIRE d.doc_id IS UNIQUE
        """
    ).consume()

    session.run(
        """
        CREATE CONSTRAINT chunk_chunk_id IF NOT EXISTS
        FOR (c:Chunk)
        REQUIRE c.chunk_id IS UNIQUE
        """
    ).consume()

    current_dimension = get_vector_index_dimension(session, index_name)
    if current_dimension is None:
        # Create vector index only once; future runs validate dimension compatibility.
        escaped_index_name = index_name.replace("`", "")
        vector_query = f"""
        CREATE VECTOR INDEX `{escaped_index_name}`
        FOR (c:Chunk) ON (c.embedding)
        OPTIONS {{
          indexConfig: {{
            `vector.dimensions`: {embedding_dimension},
            `vector.similarity_function`: 'cosine'
          }}
        }}
        """
        session.run(vector_query).consume()
        return

    if current_dimension != embedding_dimension:
        raise ValueError(
            f"Vector index '{index_name}' dimension is {current_dimension}, "
            f"but EMBEDDING_DIMENSION is {embedding_dimension}. "
            f"Drop and recreate index '{index_name}' with the new dimension, "
            "then re-run indexing."
        )


def create_embeddings(embedding_model, texts: list[str]) -> list[list[float]]:
    """Create normalized embedding vectors for a batch of chunk texts."""

    vectors = embedding_model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )
    return vectors.tolist()


def build_rows(chunks: list[DocumentChunk], embeddings: list[list[float]]) -> list[dict]:
    """Shape chunk + embedding data into query rows for Neo4j upsert."""

    rows: list[dict] = []
    for chunk, embedding in zip(chunks, embeddings, strict=True):
        chunk_metadata = dict(chunk.metadata)
        document_metadata = dict(chunk.metadata)
        document_metadata["doc_id"] = chunk.doc_id

        rows.append(
            {
                "doc_id": chunk.doc_id,
                "chunk_id": chunk.chunk_id,
                "text": chunk.text,
                "embedding": embedding,
                "document_metadata": document_metadata,
                "chunk_metadata": chunk_metadata,
            }
        )
    return rows


def upsert_rows(session, rows: list[dict]) -> None:
    """Upsert Document/Chunk nodes and HAS_CHUNK relationship in one Cypher call."""

    session.run(
        """
        UNWIND $rows AS row
        MERGE (d:Document {doc_id: row.doc_id})
        SET d += row.document_metadata
        SET d.updated_at = datetime()

        MERGE (c:Chunk {chunk_id: row.chunk_id})
        SET c += row.chunk_metadata
        SET c.text = row.text
        SET c.embedding = row.embedding
        SET c.doc_id = row.doc_id
        SET c.updated_at = datetime()

        MERGE (d)-[:HAS_CHUNK]->(c)
        """,
        rows=rows,
    ).consume()


def main() -> None:
    parser = argparse.ArgumentParser(description="Embed and index docs into Neo4j.")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional max number of docs/chunks to index.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=20,
        help="Number of chunks per embedding/indexing batch.",
    )
    args = parser.parse_args()

    settings = get_settings()
    chunks = load_document_chunks(settings.docs_path)

    if args.limit is not None:
        chunks = chunks[: args.limit]

    if not chunks:
        print("No chunks found.")
        return

    print(f"Loaded {len(chunks)} chunk(s) from {settings.docs_path}")
    print(f"Embedding model: {settings.embedding_model}")

    embedding_model = load_embedding_model(settings.embedding_model)
    driver, connected_uri = connect_neo4j(
        uri=settings.neo4j_uri,
        username=settings.neo4j_username,
        password=settings.neo4j_password,
    )
    print(f"Neo4j URI used: {connected_uri}")

    with driver:
        with driver.session(database=settings.neo4j_database) as session:
            ensure_schema(
                session=session,
                index_name=settings.vector_index_name,
                embedding_dimension=settings.embedding_dimension,
            )

            for chunk_batch in tqdm(
                batched(chunks, args.batch_size),
                total=(len(chunks) + args.batch_size - 1) // args.batch_size,
                desc="Indexing",
            ):
                embeddings = create_embeddings(
                    embedding_model=embedding_model,
                    texts=[chunk.text for chunk in chunk_batch],
                )
                rows = build_rows(chunk_batch, embeddings)
                upsert_rows(session, rows)

    print(
        "Done. Indexed "
        f"{len(chunks)} chunk(s) into Neo4j database '{settings.neo4j_database}' "
        f"with vector index '{settings.vector_index_name}'."
    )


if __name__ == "__main__":
    main()
