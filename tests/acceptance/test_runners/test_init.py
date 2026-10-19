from pathlib import Path

from pytest_bdd import scenarios

scenarios(Path(__file__).resolve().parent.parent / "features" / "cli" / "init" / "init_agent_config.feature")
