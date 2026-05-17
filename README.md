# CloudCRM RAG (Neo4j + Local Embeddings + Ollama)

Simple end-to-end Retrieval-Augmented Generation (RAG) project for support docs in `support-rag-dataset/docs`.

## Architecture

```text
Markdown Docs (with YAML front matter)
        |
        v
src.ingest
- Parse front matter + body
- 1 document => 1 chunk
        |
        v
src.index
- Embed chunks (sentence-transformers)
- Upsert into Neo4j Aura
- Create/validate vector index
        |
        v
Neo4j
- (:Document)-[:HAS_CHUNK]->(:Chunk {text, embedding, metadata...})
        |
        v
src.retrieve
- Embed query
- Vector search (top-k chunks)
        |
        v
src.rag
- Build grounded context from retrieved chunks
- Send prompt to configured LLM provider (currently Ollama local/cloud)
- Return answer with citations

        |
        v
app.py (Streamlit)
- Simple local UI for question answering
- Uses fixed retrieval top-k = 3
```

## Project Structure

```text
app.py          # Streamlit UI

src/
  config.py    # Env/config loading and validation
  runtime.py   # Shared runtime helpers (Neo4j connect, index checks, model load)
  ingest.py    # Markdown parsing, metadata extraction, 1-doc-per-chunk
  index.py     # Embedding + Neo4j upsert + vector index management
  retrieve.py  # Vector retrieval CLI
  llm.py       # LLM provider abstraction (currently Ollama)
  rag.py       # Retrieval + Ollama answer generation
  eval_retrieval.py  # Retrieval evaluation on eval/questions.jsonl

tests/
  test_runtime_checks.py  # Runtime connectivity/retrieval checks

support-rag-dataset/
  docs/        # Knowledge base source files
```

## Prerequisites

- Python 3.10+
- Neo4j Aura database
- Ollama installed locally (for generation)

## Setup

1. Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

2. Create `.env` from template:

```bash
cp .env.example .env
```

3. Update `.env` values:

- `NEO4J_URI`
- `NEO4J_USERNAME`
- `NEO4J_PASSWORD`
- `NEO4J_DATABASE`
- `DOCS_PATH`
- `VECTOR_INDEX_NAME`
- `EMBEDDING_MODEL`
- `EMBEDDING_DIMENSION`
- `TOP_K`
- `LLM_PROVIDER`
- `LLM_MODEL`
- `LLM_BASE_URL`
- `LLM_API_KEY` (optional for local, needed for some cloud endpoints)
- `LLM_TEMPERATURE`

## Data Model in Neo4j

Nodes:

- `Document`
- `Chunk`

Relationship:

- `(Document)-[:HAS_CHUNK]->(Chunk)`

Important properties:

- `Document.doc_id` (unique)
- `Chunk.chunk_id` (unique)
- `Chunk.text`
- `Chunk.embedding`
- Front matter fields copied into metadata properties
- System metadata like `__source_path`, `__chunk_index`, `__chunk_count`

## CLI Commands

### 1) Preview ingestion

```bash
python3 -m src.ingest --preview-limit 3
```

Useful flags:

- `--docs-path <path>`
- `--preview-limit <n>`

### 2) Index documents into Neo4j

```bash
python3 -m src.index --batch-size 20
```

Useful flags:

- `--limit <n>`
- `--batch-size <n>`

What it does:

- Reads chunks from `src.ingest`
- Generates embeddings using `EMBEDDING_MODEL`
- Upserts `Document` and `Chunk`
- Ensures constraints and vector index

### 3) Retrieve top-k chunks

```bash
python3 -m src.retrieve --query "SSO login fails after certificate rotation" --top-k 5
```

Useful flags:

- `--doc-type <value>`
- `--module <value>`
- `--max-text-chars <n>`

### 4) Run full RAG with Ollama

```bash
python3 -m src.rag --query "How do I resolve SSO login failure after cert rotation?"
```

Useful flags:

- `--top-k <n>`
- `--doc-type <value>`
- `--module <value>`
- `--llm-provider <provider>`
- `--llm-model <model>`
- `--llm-base-url <url>`
- `--llm-api-key <key>`
- `--temperature <float>`
- `--timeout <seconds>`

## Streamlit (Local)

Run the UI locally:

```bash
streamlit run app.py
```

Notes:

- Streamlit app currently keeps `top_k` fixed at `3`.
- LLM provider/model/base URL/API key are read from env values, not exposed in UI.
- Neo4j driver is created fresh per request to avoid stale pooled connections.

## Runtime Unit Tests

Test module:

- `tests/test_runtime_checks.py`

Run:

```bash
python3 -m unittest -v tests/test_runtime_checks.py
```

Current checks:

1. Required configs are loaded correctly.
2. Neo4j connection works.
3. Retriever returns data for a known query.
4. LLM provider endpoint is reachable and configured model is available.

## Retrieval Evaluation Reports

Evaluation dataset:

- `support-rag-dataset/eval/questions.jsonl`

Run full retrieval evaluation:

```bash
python3 -m src.eval_retrieval
```

Run a quick smoke evaluation:

```bash
python3 -m src.eval_retrieval --max-queries 5 --verbose
```

Optional flags:

- `--top-k <n>` to override retrieval top-k for this run
- `--eval-file <path>` to use a different eval file
- `--output-dir <path>` to change report output directory

Report outputs are written to `reports/retrieval/`:

- `<timestamp>_summary.json` (run metadata + aggregate metrics)
- `<timestamp>_per_query.jsonl` (retrieved chunks + metrics for each query)

Summary report metadata includes:

- LLM provider/model/base URL
- embedding model and dimension
- top-k
- LLM temperature and top-p (if configured)
- git branch/commit
- eval dataset path and SHA-256 hash

## Ollama Setup

Start local server:

```bash
ollama serve
```

Pull model:

```bash
ollama pull llama3.2
```

Quick test:

```bash
ollama run llama3.2
```

## Validation Queries (Neo4j Browser)

```cypher
MATCH (d:Document) RETURN count(d) AS documents;
MATCH (c:Chunk) RETURN count(c) AS chunks;
MATCH (:Document)-[r:HAS_CHUNK]->(:Chunk) RETURN count(r) AS links;
SHOW VECTOR INDEXES;
```

## Common Troubleshooting

### Vector dimension mismatch

If you see an error like:

- index dimension is `1536`, but query/embedding dimension is `384`

Reason:

- Existing vector index was created with a different embedding model dimension.

Fix:

```cypher
DROP INDEX chunk_embeddings IF EXISTS;
MATCH (c:Chunk) REMOVE c.embedding;
```

Then re-index:

```bash
python3 -m src.index --batch-size 20
```

### Neo4j `neo4j+s` routing issue

The code already attempts fallback from `neo4j+s://` to `neo4j+ssc://` when needed.

### Ollama connection failure

If `src.rag` cannot connect, ensure:

- `ollama serve` is running
- `LLM_BASE_URL` points to the correct host/port

### Streamlit shows defunct Neo4j connection

This app uses a fresh driver per request (no driver cache) to avoid stale pooled connections.
If you still see transient errors, retry once.

## Current Chunking Strategy

- One Markdown file = one chunk
- All YAML front matter fields are preserved as metadata
