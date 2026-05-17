from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
import yaml

from src.config import PROJECT_ROOT


@dataclass(frozen=True)
class DocumentChunk:
    chunk_id: str
    doc_id: str
    text: str
    metadata: dict[str, object]


def _resolve_docs_path(docs_path: str | Path | None) -> Path:
    if docs_path is not None:
        resolved = Path(docs_path)
    else:
        load_dotenv(PROJECT_ROOT / ".env", override=True)
        configured = os.getenv("DOCS_PATH")
        if configured:
            resolved = Path(configured)
        else:
            resolved = PROJECT_ROOT / "support-rag-dataset" / "docs"

    if not resolved.is_absolute():
        resolved = PROJECT_ROOT / resolved
    return resolved


def _parse_markdown(file_path: Path) -> tuple[dict[str, object], str]:
    raw = file_path.read_text(encoding="utf-8")

    if raw.startswith("---"):
        _, yaml_block, body = raw.split("---", 2)
        metadata = yaml.safe_load(yaml_block) or {}
    else:
        metadata = {}
        body = raw

    return dict(metadata), body.strip()


def _build_chunk(file_path: Path, docs_root: Path) -> DocumentChunk:
    metadata, text = _parse_markdown(file_path)

    doc_id = str(metadata.get("doc_id") or file_path.stem)

    # System fields for tracing where this chunk came from.
    metadata["__source_path"] = str(file_path.relative_to(docs_root))
    metadata["__source_file"] = file_path.name
    metadata["__chunk_index"] = 0
    metadata["__chunk_count"] = 1
    metadata["__chunking_strategy"] = "one_document_one_chunk"

    return DocumentChunk(
        chunk_id=f"{doc_id}::0",
        doc_id=doc_id,
        text=text,
        metadata=metadata,
    )


def load_document_chunks(docs_path: str | Path | None = None) -> list[DocumentChunk]:
    docs_root = _resolve_docs_path(docs_path)
    if not docs_root.exists():
        raise FileNotFoundError(f"Docs path does not exist: {docs_root}")
    if not docs_root.is_dir():
        raise NotADirectoryError(f"Docs path must be a directory: {docs_root}")

    chunks: list[DocumentChunk] = []
    for file_path in sorted(docs_root.rglob("*.md")):
        chunks.append(_build_chunk(file_path, docs_root))
    return chunks


def _print_preview(chunks: list[DocumentChunk], limit: int) -> None:
    print(f"Loaded {len(chunks)} chunk(s).")
    for chunk in chunks[:limit]:
        print("-" * 72)
        print(f"chunk_id: {chunk.chunk_id}")
        print(f"doc_id: {chunk.doc_id}")
        print(f"text_chars: {len(chunk.text)}")
        print("metadata_keys:")
        for key in sorted(chunk.metadata.keys()):
            print(f"  - {key}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Load support docs with one-document-per-chunk strategy."
    )
    parser.add_argument(
        "--docs-path",
        default=None,
        help="Path to docs folder. Defaults to DOCS_PATH from .env or support-rag-dataset/docs.",
    )
    parser.add_argument(
        "--preview-limit",
        type=int,
        default=3,
        help="Number of chunks to show in preview output.",
    )
    args = parser.parse_args()

    chunks = load_document_chunks(args.docs_path)
    _print_preview(chunks, max(0, args.preview_limit))


if __name__ == "__main__":
    main()
