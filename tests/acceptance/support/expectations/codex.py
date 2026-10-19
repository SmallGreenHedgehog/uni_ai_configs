from entities import Role


class CodexExpectations:
    @staticmethod
    def render_prompt(role: Role) -> str:
        prompt = f"{role.role_definition}\n\n{role.when_to_use}\n\n{role.custom_instructions}"
        return prompt

    @staticmethod
    def quote_description(value: str) -> str:
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        quoted = f'"{escaped}"'
        return quoted
