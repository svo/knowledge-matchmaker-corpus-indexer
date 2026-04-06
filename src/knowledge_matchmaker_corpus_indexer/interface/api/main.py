import sys

import chromadb
import uvicorn
from fastapi import FastAPI
from lagom import Container

from knowledge_matchmaker_corpus_indexer.application.use_case.get_job_use_case import GetJobUseCase
from knowledge_matchmaker_corpus_indexer.application.use_case.health_use_case import HealthUseCase
from knowledge_matchmaker_corpus_indexer.application.use_case.ingest_document_use_case import IngestDocumentUseCase
from knowledge_matchmaker_corpus_indexer.domain.health.health_checker import HealthChecker
from knowledge_matchmaker_corpus_indexer.domain.port.document_indexer_port import DocumentIndexerPort
from knowledge_matchmaker_corpus_indexer.domain.port.job_repository_port import JobRepositoryPort
from knowledge_matchmaker_corpus_indexer.infrastructure.chroma.chroma_document_indexer import ChromaDocumentIndexer
from knowledge_matchmaker_corpus_indexer.infrastructure.persistence.in_memory.in_memory_job_repository import InMemoryJobRepository
from knowledge_matchmaker_corpus_indexer.infrastructure.security.basic_authentication import (
    BasicAuthenticator,
    SecurityDependency,
    get_basic_authenticator,
)
from knowledge_matchmaker_corpus_indexer.infrastructure.system.health_factory import create_health_checker
from knowledge_matchmaker_corpus_indexer.interface.api.controller.health_controller import create_health_controller
from knowledge_matchmaker_corpus_indexer.interface.api.controller.ingest_controller import create_ingest_controller
from knowledge_matchmaker_corpus_indexer.shared.configuration import get_application_setting_provider

app = FastAPI(title="Knowledge Matchmaker Corpus Indexer API", version="1.0.0")


def get_container() -> Container:
    container = Container()

    chroma_client = chromadb.Client()
    indexer = ChromaDocumentIndexer(client=chroma_client)
    job_repository = InMemoryJobRepository()

    container[DocumentIndexerPort] = lambda: indexer  # type: ignore
    container[JobRepositoryPort] = lambda: job_repository  # type: ignore
    container[IngestDocumentUseCase] = IngestDocumentUseCase
    container[GetJobUseCase] = GetJobUseCase

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


ingest_use_case = global_container[IngestDocumentUseCase]
get_job_use_case = global_container[GetJobUseCase]
ingest_router = create_ingest_controller(ingest_use_case, get_job_use_case)
app.include_router(ingest_router)

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
