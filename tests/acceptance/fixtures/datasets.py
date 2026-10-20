import pytest

from entities import IgnoreEntry, Role, Rule
from tests.acceptance.support.factories import IgnoreFactory, RoleFactory, RuleFactory


@pytest.fixture
def default_roles() -> list[Role]:
    roles = RoleFactory.create_defaults()
    return roles


@pytest.fixture
def default_rules() -> list[Rule]:
    rules = RuleFactory.create_defaults()
    return rules


@pytest.fixture
def default_ignore_entries() -> list[IgnoreEntry]:
    entries = IgnoreFactory.create_defaults()
    return entries
