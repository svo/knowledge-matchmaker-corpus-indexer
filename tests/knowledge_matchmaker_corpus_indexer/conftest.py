import os
import tempfile

import pytest

os.environ.setdefault("CHROMA_DATA_PATH", tempfile.mkdtemp())
os.environ.setdefault("OPENAI_API_KEY", "test-key-not-used")

from knowledge_matchmaker_corpus_indexer.infrastructure.security.basic_authentication import (  # noqa: E402
    BasicAuthenticator,
    SecurityDependency,
)


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
