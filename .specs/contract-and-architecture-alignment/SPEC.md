# Feature: Align Contract, Extract Embedder Adapter, and Persist ChromaDB

## Overview

The corpus-indexer has three categories of gap relative to the canonical spec and architectural plan:

1. **Contract deviations** — the request field is `content` instead of `full_text`, and the status enum uses `PENDING`/`COMPLETED`/`FAILED` instead of `queued`/`processing`/`complete`/`failed`.
2. **Missing adapter** — OpenAI embedding logic is embedded directly in `ChromaCorpusIndexer` instead of being a separate adapter behind a port interface. This violates the hexagonal architecture and makes the embedding provider non-swappable.
3. **Ephemeral storage** — `ChromaCorpusIndexer` uses `chromadb.EphemeralClient()`, meaning all indexed documents are lost on restart and cannot be shared with the relationship-engine.

## Motivation

### Contract alignment

The canonical spec uses `full_text` because the corpus-indexer stores the *full text* of works — not generic "content". The status enum values `queued`/`processing`/`complete`/`failed` match standard job queue terminology and are lowercase to follow REST convention for enum values in JSON responses.

### Embedder separation

The plan explicitly called for an `OpenAIEmbedder` adapter because the embedding provider is a swappable infrastructure concern. The corpus-indexer domain should not know or care whether embeddings come from OpenAI, Anthropic, or a local model. Currently, `ChromaCorpusIndexer` directly instantiates `openai.OpenAI()` and calls `embeddings.create()` — this couples the indexer to OpenAI and makes testing require mocking the OpenAI client rather than injecting a test double.

### Persistent storage

With ephemeral storage, the corpus-indexer cannot fulfill its purpose: documents indexed via `POST /ingest` vanish on restart, and the relationship-engine (which queries a separate Chroma instance) can never find them. The parent repo's Vagrantfile will provide a shared volume mount; this service must use `chromadb.PersistentClient()` pointing at that path.

## Acceptance Criteria

### Contract

- [ ] Given a request to `POST /ingest`, when the body contains `full_text`, then the endpoint accepts it.
- [ ] Given a request to `POST /ingest`, when the body contains `content` instead of `full_text`, then the endpoint rejects it with 422.
- [ ] Given a successful ingestion, when the response is returned, then `status` is `"queued"`.
- [ ] Given a job that has completed, when `GET /jobs/{id}` is called, then `status` is `"complete"`.
- [ ] Given a job that has failed, when `GET /jobs/{id}` is called, then `status` is `"failed"`.

### Architecture

- [ ] Given the `CorpusIndexer` domain service, when its implementation is inspected, then it depends on an `Embedder` port — not on `openai` directly.
- [ ] Given a `ChromaDocumentIndexer`, when it indexes a document, then it receives pre-computed embeddings rather than computing them itself.
- [ ] Given a test for `ChromaCorpusIndexer`, when the embedder port is stubbed, then no OpenAI calls are made.

### Persistence

- [ ] Given a document indexed via `POST /ingest`, when the service restarts, then the document is still present in the vector store.
- [ ] Given the Chroma data path is configurable via environment variable `CHROMA_DATA_PATH`, when the variable is set, then `PersistentClient` uses that path.
- [ ] Given the Chroma data path is not set, when the service starts, then it falls back to a default path (`/data/chroma`).

## Current State

### Domain model field name (`corpus_document.py`)

```python
class CorpusDocument(BaseModel):
    title: str
    author: str
    source_url: str
    publication_date: str
    content: str  # Should be: full_text
```

### Status enum (`ingestion_job.py`)

```python
class IngestionStatus(str, Enum):
    PENDING = "PENDING"        # Should be: queued
    PROCESSING = "PROCESSING"  # Should be: processing
    COMPLETED = "COMPLETED"    # Should be: complete
    FAILED = "FAILED"          # Should be: failed
```

### Embedded OpenAI call (`chroma_corpus_indexer.py`)

```python
class ChromaCorpusIndexer(CorpusIndexer):
    def index(self, document: CorpusDocument, job_id: str) -> None:
        embedding_response = openai.OpenAI().embeddings.create(  # Direct OpenAI coupling
            input=document.content,
            model="text-embedding-3-small",
        )
```

### Ephemeral client (`chroma_corpus_indexer.py`)

```python
self._client = chromadb.EphemeralClient()  # Should be: PersistentClient
```

## Target Contract (from `.specs/initial/SPEC.md`)

```json
POST /ingest
Request:  { "title": "string", "author": "string", "source_url": "string", "full_text": "string", "publication_date": "string (optional)" }
Response: { "job_id": "string", "status": "queued" }

GET /jobs/{job_id}
Response: { "job_id": "string", "status": "queued|processing|complete|failed" }
```

Note: the current response includes additional fields (`document_title`, `error_message`) beyond the spec minimum. These are acceptable additions.

## Domain Model Impact

- `CorpusDocument.content` → `CorpusDocument.full_text` (rename field, update all references)
- `IngestionStatus` enum values → lowercase (`queued`, `processing`, `complete`, `failed`)
- New port: `Embedder` (abstract class with `embed(text: str) -> list[float]` method)
- New adapter: `OpenAIEmbedder` (implements `Embedder` using OpenAI API)
- `ChromaCorpusIndexer` refactored to receive `Embedder` via constructor injection

## Cross-Service Impact

None — no other service calls the corpus-indexer API. The relationship-engine queries Chroma directly (read path), not through the corpus-indexer.

## Open Questions

None.
