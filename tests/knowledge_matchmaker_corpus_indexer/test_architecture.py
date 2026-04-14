from pytest_archon.rule import archrule


def test_should_maintain_domain_layer_independence():
    (
        archrule(
            "Domain Layer Independence",
            comment="Domain layer should not depend on other layers (Clean Architecture)",
        )
        .match("knowledge_matchmaker_corpus_indexer.domain.*")
        .should_not_import(
            "knowledge_matchmaker_corpus_indexer.infrastructure.*",
            "knowledge_matchmaker_corpus_indexer.interface.*",
            "knowledge_matchmaker_corpus_indexer.application.*",
        )
        .check("knowledge_matchmaker_corpus_indexer")
    )


def test_should_maintain_application_interface_independence():
    (
        archrule(
            "Application Interface",
            comment="Application layer should not depend on interface layer",
        )
        .match("knowledge_matchmaker_corpus_indexer.application.*")
        .should_not_import("knowledge_matchmaker_corpus_indexer.interface.*")
        .check("knowledge_matchmaker_corpus_indexer")
    )


def test_should_maintain_application_infrastructure_independence():
    (
        archrule(
            "Application Infrastructure",
            comment="Application layer should not depend on infrastructure layer",
        )
        .match("knowledge_matchmaker_corpus_indexer.application.*")
        .should_not_import("knowledge_matchmaker_corpus_indexer.infrastructure.*")
        .check("knowledge_matchmaker_corpus_indexer")
    )


def test_should_use_application_use_case_in_controller():
    (
        archrule(
            "Controller Use Case",
            comment="Interface controller should depend on application use cases",
        )
        .match("knowledge_matchmaker_corpus_indexer.interface.api.controller.*")
        .should_import("knowledge_matchmaker_corpus_indexer.application.use_case.*")
        .check("knowledge_matchmaker_corpus_indexer")
    )


def test_should_not_use_domain_model_in_data_transfer_object():
    (
        archrule(
            "Data Transfer Object Model",
            comment="Data Transfer Object should not depend directly on domain model",
        )
        .match("knowledge_matchmaker_corpus_indexer.interface.api.data_transfer_object.*")
        .should_not_import("knowledge_matchmaker_corpus_indexer.domain.model.*")
        .check("knowledge_matchmaker_corpus_indexer")
    )


def test_should_follow_security_module_architecture():
    (
        archrule(
            "Security Module",
            comment="Security components should follow architectural boundaries",
        )
        .match("knowledge_matchmaker_corpus_indexer.infrastructure.security.*")
        .should_import("knowledge_matchmaker_corpus_indexer.domain.authentication.*")
        .check("knowledge_matchmaker_corpus_indexer")
    )


def test_should_not_have_circular_dependencies():
    (
        archrule(
            "No Circular Dependencies",
            comment="No modules should have circular dependencies",
        )
        .match("knowledge_matchmaker_corpus_indexer.*")
        .should(
            lambda module, direct_imports, all_imports: module not in direct_imports
            and module not in all_imports.get(module, set()),
            "no_circular_dependencies",
        )
        .check("knowledge_matchmaker_corpus_indexer")
    )


def test_should_maintain_shared_module_independence():
    (
        archrule(
            "Shared Module Dependencies",
            comment="Shared module should not depend on application, infrastructure or interface",
        )
        .match("knowledge_matchmaker_corpus_indexer.shared.*")
        .should_not_import(
            "knowledge_matchmaker_corpus_indexer.application.*",
            "knowledge_matchmaker_corpus_indexer.infrastructure.*",
            "knowledge_matchmaker_corpus_indexer.interface.*",
        )
        .check("knowledge_matchmaker_corpus_indexer")
    )


def test_should_not_import_openai_in_chroma_corpus_indexer():
    (
        archrule(
            "Chroma Corpus Indexer OpenAI Independence",
            comment="ChromaCorpusIndexer should not import openai directly",
        )
        .match("knowledge_matchmaker_corpus_indexer.infrastructure.chroma.*")
        .should_not_import("openai.*")
        .check("knowledge_matchmaker_corpus_indexer")
    )


def test_should_have_no_fastapi_imports_in_domain():
    (
        archrule(
            "Domain FastAPI Independence",
            comment="Domain layer should not import FastAPI",
        )
        .match("knowledge_matchmaker_corpus_indexer.domain.*")
        .should_not_import("fastapi.*")
        .check("knowledge_matchmaker_corpus_indexer")
    )
