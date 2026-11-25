#!/usr/bin/env sh
set -eu

PROJECT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHONPATH="$PROJECT_DIR/src${PYTHONPATH:+:$PYTHONPATH}"
export PYTHONPATH

resolve_target_platform() {
    if [ -n "${TARGET_PLATFORM:-}" ]; then
        return 0
    fi
    if [ "$(uname -s)" = "Darwin" ]; then
        TARGET_PLATFORM="macos-arm64"
    else
        TARGET_PLATFORM="linux-x86_64"
    fi
}

normalize_platform_key() {
    PLATFORM_KEY=$(printf '%s' "$TARGET_PLATFORM" | tr '-' '_')
    OS_KEY=$(printf '%s' "$TARGET_PLATFORM" | cut -d- -f1)
}

resolve_output_filename() {
    "resolve_output_filename_${PLATFORM_KEY}"
}

apply_output_filename_override() {
    OUTPUT_FILENAME="${OUTPUT_FILENAME:-$DEFAULT_OUTPUT_FILENAME}"
}

apply_target_flags() {
    LTO_FLAG=""
    SIGN_FLAG=""
    LIBPYTHON_FLAG=""
    "apply_target_flags_${OS_KEY}"
}

strip_extended_attributes() {
    "strip_extended_attributes_${OS_KEY}"
}

build_binary() {
    python3 -m nuitka \
        --onefile \
        --onefile-tempdir-spec="{TEMP}/uni-ai" \
        --enable-plugin=anti-bloat \
        --python-flag=no_docstrings \
        $LTO_FLAG \
        $LIBPYTHON_FLAG \
        $SIGN_FLAG \
        --include-package=cli \
        --include-package=application \
        --include-package=entities \
        --include-package=infrastructure \
        --include-package=templates \
        --include-package-data=templates \
        --output-dir="$PROJECT_DIR/dist" \
        --output-filename="$OUTPUT_FILENAME" \
        "$PROJECT_DIR/src/cli/uni_ai.py"
}

resolve_output_filename_linux_x86_64() {
    DEFAULT_OUTPUT_FILENAME="uni-ai-linux-x86_64.bin"
}

apply_target_flags_linux() {
    LTO_FLAG="--lto=yes"
    LIBPYTHON_FLAG="--static-libpython=no"
    CFLAGS="-march=x86-64 -mtune=generic"
    CXXFLAGS="-march=x86-64 -mtune=generic"
    export CFLAGS CXXFLAGS
}

strip_extended_attributes_linux() {
    return 0
}

resolve_output_filename_macos_arm64() {
    DEFAULT_OUTPUT_FILENAME="uni-ai-macos-arm64.bin"
}

apply_target_flags_macos() {
    SIGN_FLAG="--macos-sign-identity=-"
}

strip_extended_attributes_macos() {
    xattr -c "$PROJECT_DIR/dist/$OUTPUT_FILENAME"
}

main() {
    ONE_FILE_TEMP_DIR="${TMPDIR:-/tmp}/uni-ai"
    rm -rf "$ONE_FILE_TEMP_DIR"

    resolve_target_platform
    normalize_platform_key
    resolve_output_filename
    apply_output_filename_override
    apply_target_flags
    build_binary
    strip_extended_attributes
}

main
