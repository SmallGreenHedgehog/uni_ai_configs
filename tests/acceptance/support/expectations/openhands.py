from entities import Role


def build_openhands_skill_body(role: Role) -> str:
    body = f"{role.role_definition}\n\n{role.custom_instructions}"
    return body
