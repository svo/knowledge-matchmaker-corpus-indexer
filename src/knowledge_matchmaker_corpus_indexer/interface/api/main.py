import sys

import uvicorn
from fastapi import FastAPI
from lagom import Container

from knowledge_matchmaker_corpus_indexer.application.use_case.health_use_case import HealthUseCase
from knowledge_matchmaker_corpus_indexer.application.use_case.ingest_document_use_case import (
    GetIngestionJobUseCase,
    IngestDocumentUseCase,
)
from knowledge_matchmaker_corpus_indexer.domain.health.health_checker import HealthChecker
from knowledge_matchmaker_corpus_indexer.domain.service.corpus_indexer import CorpusIndexer
from knowledge_matchmaker_corpus_indexer.domain.service.embedder import Embedder
from knowledge_matchmaker_corpus_indexer.infrastructure.chroma.chroma_corpus_indexer import ChromaCorpusIndexer
from knowledge_matchmaker_corpus_indexer.infrastructure.openai.openai_embedder import OpenAIEmbedder
from knowledge_matchmaker_corpus_indexer.infrastructure.security.basic_authentication import (
    BasicAuthenticator,
    SecurityDependency,
    get_basic_authenticator,
)
from knowledge_matchmaker_corpus_indexer.infrastructure.system.health_factory import create_health_checker
from knowledge_matchmaker_corpus_indexer.interface.api.controller.health_controller import create_health_controller
from knowledge_matchmaker_corpus_indexer.interface.api.controller.ingest_document_controller import (
    create_ingest_document_controller,
)
from knowledge_matchmaker_corpus_indexer.shared.configuration import get_application_setting_provider

app = FastAPI(title="Knowledge Matchmaker Corpus Indexer API", version="1.0.0")


def get_container() -> Container:
    container = Container()

    embedder = OpenAIEmbedder()
    container[Embedder] = lambda: embedder  # type: ignore
    chroma_indexer = ChromaCorpusIndexer(embedder=embedder)
    container[CorpusIndexer] = lambda: chroma_indexer  # type: ignore
    container[IngestDocumentUseCase] = IngestDocumentUseCase
    container[GetIngestionJobUseCase] = GetIngestionJobUseCase

    authenticator = get_basic_authenticator()
    security_dependency = SecurityDependency(authenticator)
    container[BasicAuthenticator] = lambda: authenticator
    container[SecurityDependency] = lambda: security_dependency

    health_checker = create_health_checker()
    container[HealthChecker] = lambda: health_checker  # type: ignore
    container[HealthUseCase] = HealthUseCase

    return container


global_container = get_container()


def get_global_container() -> Container:
    return global_container


ingest_document_use_case = global_container[IngestDocumentUseCase]
get_ingestion_job_use_case = global_container[GetIngestionJobUseCase]
ingest_document_controller = create_ingest_document_controller(ingest_document_use_case, get_ingestion_job_use_case)
app.include_router(ingest_document_controller.router)

health_use_case = global_container[HealthUseCase]
health_controller = create_health_controller(health_use_case)
app.include_router(health_controller)


def main(args: list) -> None:
    settings_provider = get_application_setting_provider()
    reload_setting = settings_provider.get("reload")
    host_setting = settings_provider.get("host")

    uvicorn.run(
        "knowledge_matchmaker_corpus_indexer.interface.api.main:app",
        reload=reload_setting,
        host=host_setting,
    )


def run() -> None:
    main(sys.argv[1:])
