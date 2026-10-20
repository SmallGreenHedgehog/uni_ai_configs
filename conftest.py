FIXTURES = [
    "tests.acceptance.fixtures.clients",
    "tests.acceptance.fixtures.context",
    "tests.acceptance.fixtures.datasets",
    "tests.acceptance.fixtures.workspace",
]

STEP_DEFINITIONS = [
    "tests.acceptance.step_definitions.build_steps",
    "tests.acceptance.step_definitions.init_steps",
]

pytest_plugins = FIXTURES + STEP_DEFINITIONS
