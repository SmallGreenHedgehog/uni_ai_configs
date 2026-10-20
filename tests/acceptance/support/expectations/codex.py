from entities import Role


def build_codex_prompt(role: Role) -> str:
    prompt = f"{role.role_definition}\n\n{role.when_to_use}\n\n{role.custom_instructions}"
    return prompt
