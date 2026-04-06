from knowledge_matchmaker_corpus_indexer.infrastructure.security.basic_authentication import BasicAuthenticator, SecurityDependency

import pytest


@pytest.fixture
def basic_authenticator() -> BasicAuthenticator:
    authenticator = BasicAuthenticator()
    authenticator.register_user("testuser", "testpass")
    return authenticator


@pytest.fixture
def security_dependency(basic_authenticator) -> SecurityDependency:
    return SecurityDependency(basic_authenticator)


@pytest.fixture
def authentication_credentials():
    return ("testuser", "testpass")


@pytest.fixture
def bad_authentication_credentials():
    return ("baduser", "badpass")
