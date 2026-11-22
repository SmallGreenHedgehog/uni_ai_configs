#!/usr/bin/env sh
set -eu

PROJECT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHONPATH="$PROJECT_DIR/src${PYTHONPATH:+:$PYTHONPATH}"
export PYTHONPATH

cd "$PROJECT_DIR"

python3 -m ruff check src tests
python3 -m pylint --errors-only src
python3 -m pytest
