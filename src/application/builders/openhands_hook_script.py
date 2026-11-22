import json


def render_hook_script(patterns: list[str]) -> str:
    template = """#!/usr/bin/env python3
import fnmatch
import json
import sys

IGNORED_PATTERNS = __IGNORED_PATTERNS__


def normalize(value):
    text = value.strip().strip('"').strip("'")
    text = text.replace("\\\\", "/")
    while text.startswith("./"):
        text = text[2:]
    normalized = text.rstrip("/")
    return normalized


def collect_strings(data):
    values = []
    if isinstance(data, dict):
        for item in data.values():
            values.extend(collect_strings(item))
    elif isinstance(data, list):
        for item in data:
            values.extend(collect_strings(item))
    elif isinstance(data, str):
        values.append(data)
    result = values
    return result


def collect_values(payload):
    values = []
    for string in collect_strings(payload):
        normalized = normalize(string)
        values.append(normalized)
        for token in normalized.split():
            values.append(normalize(token))
    result = values
    return result


def is_match(value, pattern):
    candidates = [value]
    candidates.extend(value.split("/"))
    matched = any(fnmatch.fnmatch(candidate, pattern) for candidate in candidates)
    return matched


def find_match(values, patterns):
    matched = None
    for pattern in patterns:
        negated = pattern.startswith("!")
        raw_pattern = pattern[1:] if negated else pattern
        clean_pattern = normalize(raw_pattern)
        if not clean_pattern:
            continue
        for value in values:
            if is_match(value, clean_pattern):
                matched = None if negated else (value, pattern)
                break
    return matched


def parse_payload(raw):
    try:
        payload = json.loads(raw)
    except ValueError:
        payload = None
    return payload


def main():
    exit_code = 0
    payload = parse_payload(sys.stdin.read())
    if payload is not None:
        values = collect_values(payload)
        matched = find_match(values, IGNORED_PATTERNS)
        if matched is not None:
            value, pattern = matched
            print(f'Access denied: "{value}" matches ignore pattern "{pattern}"', file=sys.stderr)
            exit_code = 2
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
"""
    rendered_patterns = json.dumps(patterns, ensure_ascii=False)
    script = template.replace("__IGNORED_PATTERNS__", rendered_patterns)
    return script
