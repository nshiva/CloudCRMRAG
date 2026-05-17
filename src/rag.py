from __future__ import annotations

import argparse

from src.config import get_settings
from src.llm import generate_answer, resolve_llm_config
from src.retrieve import SearchResult, embed_query, query_chunks
from src.runtime import (
    connect_neo4j,
    ensure_vector_index_dimension,
    load_embedding_model,
)


def build_context(results: list[SearchResult]) -> str:
    """Build numbered context blocks used by the generation prompt."""

    context_blocks: list[str] = []
    for result in results:
        source_path = result.chunk_metadata.get("__source_path", "")
        title = result.chunk_metadata.get("title", "")
        doc_type = result.chunk_metadata.get("doc_type", "")
        module = result.chunk_metadata.get("module", "")

        block = (
            f"[{result.rank}]\n"
            f"doc_id: {result.doc_id}\n"
            f"chunk_id: {result.chunk_id}\n"
            f"title: {title}\n"
            f"doc_type: {doc_type}\n"
            f"module: {module}\n"
            f"source_path: {source_path}\n"
            f"content:\n{result.text.strip()}"
        )
        context_blocks.append(block)
    return "\n\n".join(context_blocks)


def print_sources(results: list[SearchResult]) -> None:
    """Print concise source lines corresponding to retrieved snippets."""

    print("\nSources:")
    for result in results:
        source_path = result.chunk_metadata.get("__source_path", "")
        print(
            f"[{result.rank}] doc_id={result.doc_id} "
            f"score={result.score:.4f} source_path={source_path}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="RAG QA with Neo4j retrieval + Ollama.")
    parser.add_argument("--query", required=True, help="Question to answer.")
    parser.add_argument(
        "--top-k",
        type=int,
        default=None,
        help="Number of retrieved chunks. Defaults to TOP_K from .env.",
    )
    parser.add_argument(
        "--doc-type",
        default=None,
        help="Optional retrieval filter (for example: troubleshooting_guide).",
    )
    parser.add_argument(
        "--module",
        default=None,
        help="Optional retrieval filter (for example: Authentication).",
    )
    parser.add_argument(
        "--llm-provider",
        default=None,
        help="LLM provider name (default: env LLM_PROVIDER or ollama).",
    )
    parser.add_argument(
        "--llm-model",
        default=None,
        help="LLM model name (default: env LLM_MODEL/OLLAMA_MODEL).",
    )
    parser.add_argument(
        "--llm-base-url",
        default=None,
        help="LLM base URL (default: env LLM_BASE_URL/OLLAMA_BASE_URL).",
    )
    parser.add_argument(
        "--llm-api-key",
        default=None,
        help="Optional API key (default: env LLM_API_KEY/OLLAMA_API_KEY).",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=None,
        help="Generation temperature (default: env LLM_TEMPERATURE/OLLAMA_TEMPERATURE).",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="HTTP timeout in seconds for Ollama calls.",
    )
    args = parser.parse_args()

    settings = get_settings()
    top_k = args.top_k or settings.top_k
    llm_config = resolve_llm_config(
        provider=args.llm_provider,
        model=args.llm_model,
        base_url=args.llm_base_url,
        api_key=args.llm_api_key,
        temperature=args.temperature,
        timeout=int(args.timeout),
    )

    print(f"Embedding model: {settings.embedding_model}")
    print(f"LLM provider: {llm_config.provider}")
    print(f"LLM model: {llm_config.model}")
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

    if not results:
        print("No matching chunks found. Try increasing --top-k or removing filters.")
        return

    context = build_context(results)
    answer = generate_answer(args.query, context, llm_config)

    print("\nAnswer:\n")
    print(answer)
    print_sources(results)


if __name__ == "__main__":
    main()
