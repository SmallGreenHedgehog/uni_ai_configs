from entities import Role


def build_openhands_subagent_body(role: Role) -> str:
    body = f"{role.role_definition}\n\n{role.when_to_use}\n\n{role.custom_instructions}"
    return body


def extract_openhands_description(content: str) -> str:
    description = ""
    for line in content.splitlines():
        if line.startswith("description: "):
            description = line[len("description: ") :]
            break
    return description


def extract_openhands_hook_commands(hooks_data: dict) -> list[str]:
    commands = []
    for matcher in hooks_data.get("pre_tool_use", []):
        for hook in matcher.get("hooks", []):
            command = hook.get("command")
            if command:
                commands.append(command)
    return commands
