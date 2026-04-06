from abc import ABC

from assertpy import assert_that

from knowledge_matchmaker_corpus_indexer.domain.port.job_repository_port import JobRepositoryPort


class TestJobRepositoryPort:
    def test_should_be_abstract_when_defined(self) -> None:
        assert_that(issubclass(JobRepositoryPort, ABC)).is_true()
