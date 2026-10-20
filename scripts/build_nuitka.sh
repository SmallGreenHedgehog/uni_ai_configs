#!/usr/bin/env sh
set -eu

PROJECT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHONPATH="$PROJECT_DIR/src${PYTHONPATH:+:$PYTHONPATH}"
export PYTHONPATH

python3 -m nuitka \
    --onefile \
    --include-package=cli \
    --include-package=application \
    --include-package=entities \
    --include-package=infrastructure \
    --include-package=templates \
    --include-package-data=templates \
    --output-dir="$PROJECT_DIR/dist" \
    --output-filename=uni-ai.bin \
    "$PROJECT_DIR/src/cli/uni_ai.py"
