from __future__ import annotations

import json

import streamlit as st

from src.config import PROJECT_ROOT, get_settings
from src.ingest import load_document_chunks
from src.llm import generate_answer, resolve_llm_config
from src.rag import build_context
from src.retrieve import embed_query, query_chunks
from src.runtime import (
    connect_neo4j,
    ensure_vector_index_dimension,
    load_embedding_model as load_embedding_model_runtime,
)


@st.cache_resource
def load_settings():
    """Load validated runtime settings once per app process."""
    return get_settings()


@st.cache_resource
def load_embedding_model(model_name: str):
    """Load local embedding model once and reuse across requests."""
    return load_embedding_model_runtime(model_name)


@st.cache_data
def load_dataset_stats() -> dict[str, object]:
    """Build sidebar info cards from local dataset files (no DB calls)."""

    chunks = load_document_chunks()
    modules = sorted(
        {
            str(chunk.metadata.get("module", "")).strip()
            for chunk in chunks
            if str(chunk.metadata.get("module", "")).strip()
        }
    )
    total_tickets = sum(
        1
        for chunk in chunks
        if str(chunk.metadata.get("doc_type", "")).strip() == "support_ticket"
    )
    return {
        "total_documents": len(chunks),
        "total_tickets": total_tickets,
        "total_areas": len(modules),
        "areas": modules,
    }


@st.cache_data
def load_recent_eval_runs(limit: int | None = None) -> dict[str, object]:
    """Load eval summaries and return compact table rows (newest first)."""

    reports_dir = PROJECT_ROOT / "reports" / "retrieval"
    if not reports_dir.exists():
        return {"available": False, "message": "No eval report directory found."}

    summary_files = sorted(reports_dir.glob("*_summary.json"))
    if not summary_files:
        return {"available": False, "message": "No eval summary found. Run eval first."}

    ordered_files = sorted(summary_files, reverse=True)
    recent_files = ordered_files if limit is None else ordered_files[: max(1, limit)]
    rows: list[dict[str, str]] = []
    for path in recent_files:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            rows.append(
                {
                    "Run ID": path.stem.replace("_summary", ""),
                    "Top K": "N/A",
                    "Recall@K": "N/A",
                    "Precision@K": "N/A",
                    "Embedding Model": "N/A",
                    "LLM Model": "N/A",
                    "Summary File": str(path.relative_to(PROJECT_ROOT)),
                }
            )
            continue

        run = payload.get("run") or {}
        config = payload.get("config") or {}
        metrics = payload.get("metrics") or {}
        recall = metrics.get("macro_recall_at_k")
        precision = metrics.get("macro_precision_at_k")
        recall_text = f"{float(recall):.4f}" if isinstance(recall, (int, float)) else "N/A"
        precision_text = (
            f"{float(precision):.4f}" if isinstance(precision, (int, float)) else "N/A"
        )
        rows.append(
            {
                "Run ID": str(run.get("run_id", "N/A")),
                "Top K": str(config.get("top_k", "N/A")),
                "Recall@K": recall_text,
                "Precision@K": precision_text,
                "Embedding Model": str(config.get("embedding_model", "N/A")),
                "LLM Model": str(config.get("llm_model", "N/A")),
                "Summary File": str(path.relative_to(PROJECT_ROOT)),
            }
        )

    return {
        "available": True,
        "count": len(rows),
        "table_rows": rows,
    }


def run_rag(
    *,
    query: str,
    top_k: int,
):
    settings = load_settings()
    embedding_model = load_embedding_model(settings.embedding_model)
    query_embedding = embed_query(embedding_model, query)

    driver, connected_uri = connect_neo4j(
        settings.neo4j_uri,
        settings.neo4j_username,
        settings.neo4j_password,
    )
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
                doc_type=None,
                module=None,
            )

    if not results:
        return {
            "answer": "",
            "results": [],
            "connected_uri": connected_uri,
            "message": "No matching chunks found. Try increasing top_k or removing filters.",
        }

    context = build_context(results)
    llm_config = resolve_llm_config()
    answer = generate_answer(query, context, llm_config)

    return {
        "answer": answer,
        "results": results,
        "connected_uri": connected_uri,
        "message": "",
    }


def main() -> None:
    fixed_top_k = 3

    st.set_page_config(page_title="CloudCRM RAG", page_icon="🧠", layout="wide")
    st.title("CloudCRM Support RAG")
    st.caption("Neo4j vector retrieval + local Ollama generation")

    stats = load_dataset_stats()
    eval_info = load_recent_eval_runs(limit=None)

    with st.sidebar:
        st.header("Dataset Overview")
        st.metric("Total Tickets", int(stats["total_tickets"]))
        st.metric("Total Areas", int(stats["total_areas"]))
        st.metric("Total Documents", int(stats["total_documents"]))
        st.divider()
        st.caption("Areas/Departments")
        st.write(", ".join(stats["areas"]) or "N/A")
        st.divider()
        st.caption("Retrieval top-k is fixed at 3.")
        st.caption("Eval run metrics are shown below citations.")

    query = st.text_area(
        "Ask a support question",
        placeholder="Example: Why does SSO login fail after identity provider certificate rotation?",
        height=120,
    )
    ask = st.button("Get Answer", type="primary")

    if ask:
        if not query.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Retrieving context and generating answer..."):
                try:
                    payload = run_rag(
                        query=query.strip(),
                        top_k=fixed_top_k,
                    )
                except Exception as exc:
                    st.error(str(exc))
                    payload = None

            if payload is not None:
                if payload["message"]:
                    st.info(payload["message"])
                else:
                    st.subheader("Answer")
                    st.write(payload["answer"])

                st.subheader("Retrieved Sources")
                st.caption(f"Neo4j URI used: {payload['connected_uri']}")
                for result in payload["results"]:
                    with st.expander(
                        f"[{result.rank}] {result.doc_id} | score={result.score:.4f}",
                        expanded=False,
                    ):
                        st.write(
                            {
                                "chunk_id": result.chunk_id,
                                "doc_type": result.chunk_metadata.get("doc_type"),
                                "module": result.chunk_metadata.get("module"),
                                "source_path": result.chunk_metadata.get("__source_path"),
                            }
                        )
                        st.text(result.text)

    st.divider()
    st.subheader("All Eval Runs")
    if not eval_info["available"]:
        st.caption(str(eval_info["message"]))
    else:
        st.caption(f"Showing {eval_info['count']} run(s). Newest first.")
        st.table(eval_info["table_rows"])


if __name__ == "__main__":
    main()
