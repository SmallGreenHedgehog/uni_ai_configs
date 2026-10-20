# architecture

Project: a Python package that prepares AI agent environment configurations.

Stack: Python, Pydantic v2, PyYAML, pytest, pytest-bdd, polyfactory.
Approach: Domain-Driven Design (DDD).

Entry points:
- init-uni-ai - console command that creates universal agent configs from templates
- build-uni-ai - console command that wires builders with repositories

Layers:
- src/entities - domain entities on Pydantic v2
- src/application/interfaces/repositories - abstract (ABC) repository interfaces
- src/application/builders - config builders (base builder and per-tool implementations)
- src/infrastructure/repositories - file-based repository implementations

Tests:
- tests/unit - unit tests, mirroring the src/ structure
- tests/integration - integration tests, mirroring the src/ structure
- tests/acceptance - e2e tests (pytest-bdd)

Acceptance (e2e) tests (pytest-bdd):
- tests/acceptance/features - Gherkin .feature scenarios, grouped by CLI command under cli/build and cli/init
- tests/acceptance/test_runners - pytest-bdd runner files connecting .feature scenarios to pytest
- tests/acceptance/step_definitions - implementations of steps from .feature files; contain only step bindings, no helper logic
- tests/acceptance/fixtures - pytest fixtures: clients, context, datasets, workspace; contain only @pytest.fixture definitions, no business logic
- tests/acceptance/support - test support classes
  - support/clients - CLI clients and file clients, split by data structure (markdown, ignore, yaml, codex config); base classes expose universal methods, subclasses implement abstract format hooks
  - support/factories - polyfactory-based factories for domain entities (Role, Rule, IgnoreEntry); classmethods create sets, instance methods create a single element
  - support/context - Pydantic models for sharing scenario state between steps
  - support/expectations - helpers that compute expected values for assertions
- tests/acceptance/conftest.py - connects fixtures and step definitions through pytest_plugins

Dependency rules:
- Use dependency injection to consume infrastructure from the application layer
- The domain layer must not depend on anything
- The application layer must not depend on infrastructure

Package exports:
- In __init__.py, re-export nested classes only when they are used outside the package

When adding new directories and modules, follow DDD and Robert Martin's clean architecture best practices, adapted to this project.

Documentation:
- docs/ - project documentation in Markdown
