#!/usr/bin/env sh
set -eu

PROJECT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHONPATH="$PROJECT_DIR/src${PYTHONPATH:+:$PYTHONPATH}"
export PYTHONPATH

ONE_FILE_TEMP_DIR="${TMPDIR:-/tmp}/uni-ai"
rm -rf "$ONE_FILE_TEMP_DIR"

LTO_FLAG=""
SIGN_FLAG=""
case "$(uname -s)" in
    Linux) LTO_FLAG="--lto=yes" ;;
    Darwin) SIGN_FLAG="--macos-sign-identity=-" ;;
esac

python3 -m nuitka \
    --onefile \
    --onefile-tempdir-spec="{TEMP}/uni-ai" \
    --enable-plugin=anti-bloat \
    --python-flag=no_docstrings \
    $LTO_FLAG \
    $SIGN_FLAG \
    --include-package=cli \
    --include-package=application \
    --include-package=entities \
    --include-package=infrastructure \
    --include-package=templates \
    --include-package-data=templates \
    --output-dir="$PROJECT_DIR/dist" \
    --output-filename=uni-ai.bin \
    "$PROJECT_DIR/src/cli/uni_ai.py"

case "$(uname -s)" in
    Darwin)
        BINARY="$PROJECT_DIR/dist/uni-ai.bin"
        xattr -c "$BINARY"
        ;;
esac
