from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.config import PROJECT_ROOT, get_settings
from src.llm import resolve_llm_config
from src.retrieve import embed_query, query_chunks
from src.runtime import (
    connect_neo4j,
    ensure_vector_index_dimension,
    load_embedding_model,
)


def _optional_float_env(*names: str) -> float | None:
    for name in names:
        value = os.getenv(name)
        if value is None or not value.strip():
            continue
        try:
            return float(value.strip())
        except ValueError:
            return None
    return None


def _safe_git_value(*args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except Exception:
        return ""


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def load_eval_rows(eval_file: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in eval_file.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        rows.append(json.loads(stripped))
    return rows


def _dedupe_keep_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        out.append(value)
    return out


def compute_query_metrics(expected_sources: list[str], retrieved_doc_ids: list[str], k: int) -> dict[str, Any]:
    expected = _dedupe_keep_order(expected_sources)
    retrieved = _dedupe_keep_order(retrieved_doc_ids)[:k]
    expected_set = set(expected)

    if len(expected) == 0:
        return {
            "evaluable": False,
            "precision_at_k": None,
            "recall_at_k": None,
            "hit_at_k": None,
            "mrr": None,
            "ndcg_at_k": None,
            "ap_at_k": None,
            "matched_count": 0,
            "expected_count": 0,
            "relevant_ranks": [],
            "matched_sources": [],
            "missing_sources": [],
            "unexpected_sources": retrieved,
        }

    matched_sources = [doc_id for doc_id in retrieved if doc_id in expected_set]
    missing_sources = [doc_id for doc_id in expected if doc_id not in set(matched_sources)]
    unexpected_sources = [doc_id for doc_id in retrieved if doc_id not in expected_set]
    relevant_ranks = [i for i, doc_id in enumerate(retrieved, start=1) if doc_id in expected_set]

    matched = len(matched_sources)
    precision_at_k = matched / max(k, 1)
    recall_at_k = matched / len(expected)
    hit_at_k = 1.0 if matched > 0 else 0.0
    mrr = (1.0 / relevant_ranks[0]) if relevant_ranks else 0.0

    # Binary AP@k and nDCG@k for ranked retrieval quality.
    ap_numerator = 0.0
    rel_so_far = 0
    dcg = 0.0
    for i, doc_id in enumerate(retrieved, start=1):
        rel = 1 if doc_id in expected_set else 0
        if rel:
            rel_so_far += 1
            ap_numerator += rel_so_far / i
            dcg += 1.0 / math.log(i + 1, 2)

    ap_at_k = ap_numerator / len(expected)
    ideal_rel_count = min(len(expected), k)
    idcg = sum(1.0 / math.log(i + 1, 2) for i in range(1, ideal_rel_count + 1))
    ndcg_at_k = (dcg / idcg) if idcg > 0 else 0.0

    return {
        "evaluable": True,
        "precision_at_k": precision_at_k,
        "recall_at_k": recall_at_k,
        "hit_at_k": hit_at_k,
        "mrr": mrr,
        "ndcg_at_k": ndcg_at_k,
        "ap_at_k": ap_at_k,
        "matched_count": matched,
        "expected_count": len(expected),
        "relevant_ranks": relevant_ranks,
        "matched_sources": matched_sources,
        "missing_sources": missing_sources,
        "unexpected_sources": unexpected_sources,
    }


def aggregate_metrics(per_query: list[dict[str, Any]], top_k: int) -> dict[str, Any]:
    evaluable = [row for row in per_query if row["metrics"]["evaluable"]]
    non_evaluable = [row for row in per_query if not row["metrics"]["evaluable"]]

    def mean(key: str) -> float | None:
        values = [row["metrics"][key] for row in evaluable]
        if not values:
            return None
        return sum(values) / len(values)

    matched_total = sum(row["metrics"]["matched_count"] for row in evaluable)
    expected_total = sum(row["metrics"]["expected_count"] for row in evaluable)

    return {
        "top_k": top_k,
        "total_queries": len(per_query),
        "evaluable_queries": len(evaluable),
        "non_evaluable_queries": len(non_evaluable),
        "macro_precision_at_k": mean("precision_at_k"),
        "macro_recall_at_k": mean("recall_at_k"),
        "macro_hit_at_k": mean("hit_at_k"),
        "mrr": mean("mrr"),
        "map_at_k": mean("ap_at_k"),
        "ndcg_at_k": mean("ndcg_at_k"),
        "micro_recall_at_k": (matched_total / expected_total) if expected_total > 0 else None,
    }


def _timestamp_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _format_value(value: Any) -> str:
    if value is None:
        return "N/A"
    if isinstance(value, float):
        return f"{value:.4f}".rstrip("0").rstrip(".")
    text = str(value).strip()
    return text if text else "N/A"


def build_eval_parameter_rows(
    *,
    embedding_model: str,
    embedding_dimension: int,
    top_k: int,
    llm_provider: str,
    llm_model: str,
    llm_base_url: str,
    llm_temperature: float,
    llm_top_p: float | None,
    vector_index_name: str,
    neo4j_uri_used: str,
) -> list[dict[str, str]]:
    """Return display-ready label/value rows for UI rendering."""

    return [
        {"label": "Embedding Model", "value": _format_value(embedding_model)},
        {"label": "Embedding Dimension", "value": _format_value(embedding_dimension)},
        {"label": "Top K", "value": _format_value(top_k)},
        {"label": "LLM Provider", "value": _format_value(llm_provider)},
        {"label": "LLM Model", "value": _format_value(llm_model)},
        {"label": "LLM Base URL", "value": _format_value(llm_base_url)},
        {"label": "LLM Temperature", "value": _format_value(llm_temperature)},
        {"label": "LLM Top P", "value": _format_value(llm_top_p)},
        {"label": "Vector Index", "value": _format_value(vector_index_name)},
        {"label": "Neo4j URI Used", "value": _format_value(neo4j_uri_used)},
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate retrieval quality using eval/questions.jsonl.")
    parser.add_argument(
        "--eval-file",
        default="support-rag-dataset/eval/questions.jsonl",
        help="Path to eval questions jsonl file.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=None,
        help="Retrieval top-k for evaluation. Defaults to TOP_K from settings.",
    )
    parser.add_argument(
        "--output-dir",
        default="reports/retrieval",
        help="Directory to write evaluation reports.",
    )
    parser.add_argument(
        "--max-queries",
        type=int,
        default=None,
        help="Optional limit for quick evaluation runs.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print per-query hit/recall details to console.",
    )
    args = parser.parse_args()

    settings = get_settings()
    llm_config = resolve_llm_config()
    eval_file = Path(args.eval_file)
    if not eval_file.is_absolute():
        eval_file = PROJECT_ROOT / eval_file

    rows = load_eval_rows(eval_file)
    if args.max_queries is not None:
        rows = rows[: args.max_queries]

    top_k = args.top_k or settings.top_k
    if top_k <= 0:
        raise ValueError("--top-k must be > 0")

    run_timestamp = _timestamp_utc()
    run_id = run_timestamp
    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = PROJECT_ROOT / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Evaluating retrieval on {len(rows)} query(ies)")
    print(f"Embedding model: {settings.embedding_model}")
    print(f"LLM config (for report metadata): {llm_config.provider}/{llm_config.model}")
    print(f"top_k={top_k}")

    embedding_model = load_embedding_model(settings.embedding_model)

    driver, connected_uri = connect_neo4j(
        uri=settings.neo4j_uri,
        username=settings.neo4j_username,
        password=settings.neo4j_password,
    )
    print(f"Neo4j URI used: {connected_uri}")

    per_query: list[dict[str, Any]] = []
    with driver:
        with driver.session(database=settings.neo4j_database) as session:
            ensure_vector_index_dimension(
                session=session,
                index_name=settings.vector_index_name,
                expected_dimension=settings.embedding_dimension,
            )

            for idx, row in enumerate(rows, start=1):
                question = row.get("question", "")
                expected_sources = row.get("expected_sources", [])
                expected_answer_points = row.get("expected_answer_points", [])
                expected_behavior = row.get("expected_behavior")

                query_embedding = embed_query(embedding_model, question)
                results = query_chunks(
                    session=session,
                    index_name=settings.vector_index_name,
                    top_k=top_k,
                    query_embedding=query_embedding,
                    doc_type=None,
                    module=None,
                )

                retrieved = []
                for result in results:
                    retrieved.append(
                        {
                            "rank": result.rank,
                            "doc_id": result.doc_id,
                            "chunk_id": result.chunk_id,
                            "score": result.score,
                            "source_path": result.chunk_metadata.get("__source_path", ""),
                            "doc_type": result.chunk_metadata.get("doc_type", ""),
                            "module": result.chunk_metadata.get("module", ""),
                        }
                    )

                metrics = compute_query_metrics(
                    expected_sources=expected_sources,
                    retrieved_doc_ids=[item["doc_id"] for item in retrieved],
                    k=top_k,
                )
                record = {
                    "query_id": idx,
                    "question": question,
                    "expected_sources": expected_sources,
                    "expected_answer_points": expected_answer_points,
                    "expected_behavior": expected_behavior,
                    "retrieved": retrieved,
                    "metrics": metrics,
                }
                per_query.append(record)

                if args.verbose:
                    print(
                        f"[{idx:02d}] hit={metrics['hit_at_k']} "
                        f"recall={metrics['recall_at_k']} "
                        f"matched={metrics['matched_sources']}"
                    )

    aggregate = aggregate_metrics(per_query, top_k=top_k)

    llm_top_p = _optional_float_env("LLM_TOP_P", "OLLAMA_TOP_P")
    eval_parameter_rows = build_eval_parameter_rows(
        embedding_model=settings.embedding_model,
        embedding_dimension=settings.embedding_dimension,
        top_k=top_k,
        llm_provider=llm_config.provider,
        llm_model=llm_config.model,
        llm_base_url=llm_config.base_url,
        llm_temperature=llm_config.temperature,
        llm_top_p=llm_top_p,
        vector_index_name=settings.vector_index_name,
        neo4j_uri_used=connected_uri,
    )

    summary = {
        "run": {
            "run_id": run_id,
            "timestamp_utc": run_timestamp,
            "git_commit": _safe_git_value("rev-parse", "HEAD"),
            "git_branch": _safe_git_value("rev-parse", "--abbrev-ref", "HEAD"),
        },
        "dataset": {
            "path": str(eval_file),
            "sha256": _sha256_file(eval_file),
            "query_count": len(rows),
        },
        "config": {
            "neo4j_database": settings.neo4j_database,
            "neo4j_uri_used": connected_uri,
            "vector_index_name": settings.vector_index_name,
            "embedding_model": settings.embedding_model,
            "embedding_dimension": settings.embedding_dimension,
            "top_k": top_k,
            "llm_provider": llm_config.provider,
            "llm_model": llm_config.model,
            "llm_base_url": llm_config.base_url,
            "llm_temperature": llm_config.temperature,
            "llm_top_p": llm_top_p,
        },
        "ui": {"eval_parameters": eval_parameter_rows},
        "metrics": aggregate,
        "notes": "Retrieval evaluation against expected_sources from eval/questions.jsonl.",
    }

    summary_path = output_dir / f"{run_id}_summary.json"
    per_query_path = output_dir / f"{run_id}_per_query.jsonl"

    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    with per_query_path.open("w", encoding="utf-8") as f:
        for record in per_query:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print("\nEvaluation complete")
    print(f"Summary:   {summary_path}")
    print(f"Per-query: {per_query_path}")
    print(
        "Macro metrics: "
        f"hit@{top_k}={aggregate['macro_hit_at_k']:.4f}, "
        f"recall@{top_k}={aggregate['macro_recall_at_k']:.4f}, "
        f"precision@{top_k}={aggregate['macro_precision_at_k']:.4f}, "
        f"MRR={aggregate['mrr']:.4f}, "
        f"nDCG@{top_k}={aggregate['ndcg_at_k']:.4f}"
    )


if __name__ == "__main__":
    main()
