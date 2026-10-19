import pytest

from tests.acceptance.support.context import ScenarioState


@pytest.fixture
def scenario_state() -> ScenarioState:
    state = ScenarioState()
    return state
