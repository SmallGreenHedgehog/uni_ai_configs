import json


def quote_value_if_needed(value: str) -> str:
    unsafe_start = set("!&*{}[],#|>@`\"'-?:")
    needs_quoting = not value or ": " in value or " #" in value or value[0] in unsafe_start
    rendered = json.dumps(value, ensure_ascii=False) if needs_quoting else value
    return rendered
