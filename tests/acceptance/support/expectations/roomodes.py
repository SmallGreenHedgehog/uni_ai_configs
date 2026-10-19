class RoomodesExpectations:
    @staticmethod
    def read_description(content: str) -> str:
        description = ""
        for line in content.splitlines():
            if line.startswith("    description: "):
                description = line[len("    description: ") :]
                break
        return description

    @staticmethod
    def extract_instruction_lines(content: str) -> list[str]:
        collected = []
        in_instructions = False
        for line in content.splitlines():
            if line == "    customInstructions: |-":
                in_instructions = True
            elif in_instructions and line.startswith("    ") and not line.startswith("      "):
                in_instructions = False
            elif in_instructions and line:
                collected.append(line)
        return collected
