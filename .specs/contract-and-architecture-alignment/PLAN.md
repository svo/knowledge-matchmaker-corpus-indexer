# Plan: Align Contract, Extract Embedder Adapter, and Persist ChromaDB

## Implementation Strategy

Three independent workstreams, done in this order:

1. **Contract alignment** (domain → interface, outward) — rename field names and status enum values
2. **Embedder extraction** (infrastructure refactor) — introduce `Embedder` port, extract `OpenAIEmbedder` adapter, refactor `ChromaCorpusIndexer` to receive it via injection
3. **Persistent Chroma** (infrastructure) — switch from `EphemeralClient` to `PersistentClient` with configurable path

The contract and embedder changes are independent and could be done in either order. Persistent Chroma should come last because the embedder refactor touches `ChromaCorpusIndexer` — doing both simultaneously increases merge conflict risk.

## Changes

### 1. Contract alignment

**`domain/model/corpus_document.py`**

- Rename field `content` → `full_text`

**`domain/model/ingestion_job.py`**

- Change `IngestionStatus` enum values to lowercase:
  - `PENDING = "PENDING"` → `QUEUED = "queued"`
  - `PROCESSING = "PROCESSING"` → `PROCESSING = "processing"`
  - `COMPLETED = "COMPLETED"` → `COMPLETE = "complete"`
  - `FAILED = "FAILED"` → `FAILED = "failed"`

**`interface/api/data_transfer_object/ingest_document_data_transfer_object.py`**

- Rename `IngestDocumentRequestDto.content` → `IngestDocumentRequestDto.full_text`
- Update `from_domain_model()` to map the renamed field

**All files referencing `document.content` or `IngestionStatus.PENDING` / `IngestionStatus.COMPLETED`**

- Update to use new field name and enum values
- Includes: `ChromaCorpusIndexer`, `IngestDocumentUseCase`, controller, tests

### 2. Embedder extraction

**New: `domain/service/embedder.py`** (port)

```python
from abc import ABC, abstractmethod

class Embedder(ABC):
    @abstractmethod
    def embed(self, text: str) -> list[float]:
        pass
```

**New: `infrastructure/openai/openai_embedder.py`** (adapter)

```python
class OpenAIEmbedder(Embedder):
    def embed(self, text: str) -> list[float]:
        response = openai.OpenAI().embeddings.create(
            input=text,
            model="text-embedding-3-small",
        )
        return response.data[0].embedding
```

**Modified: `infrastructure/chroma/chroma_corpus_indexer.py`**

- Add `embedder: Embedder` parameter to `__init__`
- Replace direct `openai.OpenAI().embeddings.create()` call with `self._embedder.embed(document.full_text)`
- Remove `import openai`

**Modified: DI container registration** (wherever Lagom container is configured)

- Register `Embedder` → `OpenAIEmbedder`
- Pass `Embedder` to `ChromaCorpusIndexer` constructor

### 3. Persistent Chroma

**Modified: `infrastructure/chroma/chroma_corpus_indexer.py`**

- Replace `chromadb.EphemeralClient()` with `chromadb.PersistentClient(path=chroma_data_path)`
- Read path from `os.environ.get("CHROMA_DATA_PATH", "/data/chroma")`

## Task List

### Contract alignment

1. [ ] Rename `CorpusDocument.content` → `CorpusDocument.full_text` and update all references
2. [ ] Change `IngestionStatus` enum values to lowercase (`queued`, `processing`, `complete`, `failed`) and update all references
3. [ ] Update `IngestDocumentRequestDto.content` → `IngestDocumentRequestDto.full_text`
4. [ ] Update all domain model tests for renamed field and enum values
5. [ ] Update controller integration tests for new request field name and response status values
6. [ ] Run `tox` to verify

### Embedder extraction

7. [ ] Create `Embedder` port (abstract class) in `domain/service/embedder.py`
8. [ ] Create `OpenAIEmbedder` adapter in `infrastructure/openai/openai_embedder.py`
9. [ ] Refactor `ChromaCorpusIndexer` to receive `Embedder` via constructor injection; remove direct OpenAI import
10. [ ] Update DI container to register `Embedder` → `OpenAIEmbedder`
11. [ ] Write unit tests for `OpenAIEmbedder` (mocked OpenAI client)
12. [ ] Update `ChromaCorpusIndexer` tests to inject a stub `Embedder`
13. [ ] Write architectural unit test: assert `ChromaCorpusIndexer` does not import from `openai`
14. [ ] Run `tox` to verify

### Persistent Chroma

15. [ ] Modify `ChromaCorpusIndexer.__init__` to use `PersistentClient` with configurable path via `CHROMA_DATA_PATH`
16. [ ] Update tests to use a temporary directory for persistent Chroma (via `tmp_path` fixture)
17. [ ] Run `tox` to verify

## Testing Strategy

**Unit tests**: Each domain model change gets updated tests. The new `Embedder` port gets a test confirming it is abstract. `OpenAIEmbedder` gets a test with a mocked OpenAI client. `ChromaCorpusIndexer` tests inject a stub embedder that returns fixed vectors.

**Integration tests**: Controller tests updated for new field names and status values. Verify 422 when old field names are sent.

**Architectural tests**: Add assertion that `ChromaCorpusIndexer` does not import `openai` directly (this import should only appear in `OpenAIEmbedder`).

## Risks and Mitigations

- **Risk**: Renaming `content` → `full_text` touches many files across layers. **Mitigation**: Use IDE/grep to find all references; `tox` (mypy) will catch type mismatches.
- **Risk**: Chroma `PersistentClient` may behave differently from `EphemeralClient` in tests. **Mitigation**: Use `tmp_path` fixture to create isolated persistent directories per test.
- **Risk**: Enum value change from uppercase to lowercase may break serialisation. **Mitigation**: `IngestionStatus` is a `str, Enum` — the `.value` is what gets serialised, so changing the value directly changes the wire format. All assertions must update.
