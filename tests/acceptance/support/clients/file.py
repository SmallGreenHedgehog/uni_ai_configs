from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generic, TypeVar

import yaml

T = TypeVar("T")


class FileClient(ABC, Generic[T]):
    def read(self, path: Path) -> T:
        content = path.read_text(encoding="utf-8")
        result = self._load_content(content)
        return result

    @abstractmethod
    def _load_content(self, content: str) -> T: ...

    def write(self, path: Path, data: T) -> None:
        content = self._dump_content(data)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    @abstractmethod
    def _dump_content(self, data: T) -> str: ...


class MarkdownFileClient(FileClient[str]):
    def _load_content(self, content: str) -> str:
        markdown = content
        return markdown

    def _dump_content(self, data: str) -> str:
        content = data
        return content


class IgnoreFileClient(FileClient[list[str]]):
    def _load_content(self, content: str) -> list[str]:
        patterns = [line for line in content.splitlines() if line]
        return patterns

    def _dump_content(self, data: list[str]) -> str:
        content = "\n".join(data) + "\n"
        return content


class YamlFileClient(FileClient[dict]):
    def _load_content(self, content: str) -> dict:
        data = yaml.safe_load(content)
        return data

    def _dump_content(self, data: dict) -> str:
        content = yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
        return content


class CodexConfigFileClient(FileClient[list[dict]]):
    def _load_content(self, content: str) -> list[dict]:
        agents = []
        current = None
        prompt_lines = None
        for line in content.splitlines():
            if line.startswith("[agents."):
                current = {"slug": line[len("[agents.") :].rstrip("]"), "description": "", "prompt": ""}
                agents.append(current)
            elif current is not None and line.startswith("description = "):
                current["description"] = line[len("description = ") :]
            elif current is not None and line.startswith('prompt = """'):
                prompt_lines = [line[len('prompt = """') :]]
            elif prompt_lines is not None:
                if line.endswith('"""'):
                    prompt_lines.append(line[:-3])
                    current["prompt"] = "\n".join(prompt_lines)
                    prompt_lines = None
                else:
                    prompt_lines.append(line)
        return agents

    def _dump_content(self, data: list[dict]) -> str:
        sections = []
        for agent in data:
            sections.append(f"[agents.{agent['slug']}]")
            sections.append(f"description = {agent['description']}")
            sections.append(f'prompt = """{agent["prompt"]}"""')
            sections.append("")
        content = "\n".join(sections) + "\n"
        return content
