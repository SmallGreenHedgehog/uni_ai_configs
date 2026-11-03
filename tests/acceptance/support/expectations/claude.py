from entities import Role


def build_claude_agent_name(role: Role, index: int) -> str:
    agent_name = f"{index:02d}-{role.slug}"
    return agent_name


def build_claude_agent_body(role: Role) -> str:
    body = f"{role.role_definition}\n\n{role.when_to_use}\n\n{role.custom_instructions}"
    return body


def extract_claude_description(content: str) -> str:
    description = ""
    for line in content.splitlines():
        if line.startswith("description: "):
            description = line[len("description: ") :]
            break
    return description
