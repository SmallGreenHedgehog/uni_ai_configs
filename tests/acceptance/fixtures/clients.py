import pytest

from tests.acceptance.support.clients import (
    BuildClient,
    CodexConfigFileClient,
    IgnoreFileClient,
    InitClient,
    MarkdownFileClient,
    YamlFileClient,
)


@pytest.fixture
def build_client() -> BuildClient:
    client = BuildClient()
    return client


@pytest.fixture
def init_client() -> InitClient:
    client = InitClient()
    return client


@pytest.fixture
def codex_config_file_client() -> CodexConfigFileClient:
    client = CodexConfigFileClient()
    return client


@pytest.fixture
def yaml_file_client() -> YamlFileClient:
    client = YamlFileClient()
    return client


@pytest.fixture
def markdown_file_client() -> MarkdownFileClient:
    client = MarkdownFileClient()
    return client


@pytest.fixture
def ignore_file_client() -> IgnoreFileClient:
    client = IgnoreFileClient()
    return client
