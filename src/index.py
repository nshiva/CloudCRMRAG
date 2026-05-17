from __future__ import annotations

import argparse
import os
from collections.abc import Iterable

from neo4j import GraphDatabase
from tqdm import tqdm

from src.config import PROJECT_ROOT, get_settings
from src.ingest import DocumentChunk, load_document_chunks

# Keep Hugging Face cache inside project workspace to avoid home-dir permission issues.
PROJECT_CACHE = PROJECT_ROOT / ".cache"
HF_CACHE = PROJECT_CACHE / "huggingface"
HF_HUB_CACHE = HF_CACHE / "hub"
os.environ["XDG_CACHE_HOME"] = str(PROJECT_CACHE)
os.environ["HF_HOME"] = str(HF_CACHE)
os.environ["HF_HUB_CACHE"] = str(HF_HUB_CACHE)
os.environ["HUGGINGFACE_HUB_CACHE"] = str(HF_HUB_CACHE)
os.environ["HF_HUB_DISABLE_XET"] = "1"
HF_HUB_CACHE.mkdir(parents=True, exist_ok=True)

from sentence_transformers import SentenceTransformer


def batched(items: list[DocumentChunk], batch_size: int) -> Iterable[list[DocumentChunk]]:
    for i in range(0, len(items), batch_size):
        yield items[i : i + batch_size]


def connect_neo4j(uri: str, username: str, password: str):
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


def ensure_schema(session, index_name: str, embedding_dimension: int) -> None:
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

    escaped_index_name = index_name.replace("`", "")
    vector_query = f"""
    CREATE VECTOR INDEX `{escaped_index_name}` IF NOT EXISTS
    FOR (c:Chunk) ON (c.embedding)
    OPTIONS {{
      indexConfig: {{
        `vector.dimensions`: {embedding_dimension},
        `vector.similarity_function`: 'cosine'
      }}
    }}
    """
    session.run(vector_query).consume()


def create_embeddings(
    embedding_model: SentenceTransformer, texts: list[str]
) -> list[list[float]]:
    vectors = embedding_model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )
    return vectors.tolist()


def build_rows(chunks: list[DocumentChunk], embeddings: list[list[float]]) -> list[dict]:
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

    embedding_model = SentenceTransformer(
        settings.embedding_model,
        cache_folder=str(HF_CACHE),
    )
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
