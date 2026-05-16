# CloudDesk CRM Synthetic Support RAG Dataset

This dataset is a fictional customer support knowledge base for a SaaS product called **CloudDesk CRM**.

It is designed for building and evaluating a RAG-based AI Customer Support Resolution Assistant.

## Dataset Contents

- Product knowledge articles
- Troubleshooting guides
- Historical support tickets
- Known issues
- Incident reports
- Response templates
- Support escalation policies
- Evaluation questions

## Important

This dataset is fully synthetic. It does not contain real customer data, real company data, or confidential information.

## Suggested RAG Use Cases

- Answer support questions with citations
- Retrieve similar historical tickets
- Recommend known resolutions
- Suggest escalation paths
- Draft customer responses
- Evaluate hallucination handling

## Recommended Ingestion Flow

1. Read Markdown files from `docs/`
2. Parse YAML front matter as metadata
3. Chunk Markdown content
4. Generate embeddings
5. Store chunks and metadata in a vector database
6. Use `eval/questions.jsonl` to test retrieval and answer quality
