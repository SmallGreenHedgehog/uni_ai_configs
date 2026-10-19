from importlib.resources import files
from importlib.resources.abc import Traversable
from pathlib import Path

from infrastructure.settings import settings


class InitCommand:
    @staticmethod
    def run() -> None:
        root_dir = Path.cwd()
        agents_dir = InitCommand.__resolve_agents_dir(root_dir)
        created_files, skipped_files = InitCommand.__create_template_files(agents_dir)
        report = InitCommand.__render_report(created_files, skipped_files)
        print(report)

    @staticmethod
    def __resolve_agents_dir(root_dir: Path) -> Path:
        configured_agents_dir = settings.agents_dir
        if configured_agents_dir.is_absolute():
            agents_dir = configured_agents_dir
        else:
            agents_dir = root_dir / configured_agents_dir
        return agents_dir

    @staticmethod
    def __create_template_files(agents_dir: Path) -> tuple[list[Path], list[Path]]:
        templates = files("templates")
        template_parts = [("roles.yaml",), ("rules", "code-style.md"), ("ignore",)]
        created_files: list[Path] = []
        skipped_files: list[Path] = []
        for parts in template_parts:
            target_path = agents_dir.joinpath(*parts)
            if target_path.exists():
                skipped_files.append(target_path)
            else:
                content = InitCommand.__read_template(templates, parts)
                target_path.parent.mkdir(parents=True, exist_ok=True)
                target_path.write_text(content, encoding="utf-8")
                created_files.append(target_path)
        return created_files, skipped_files

    @staticmethod
    def __read_template(templates: Traversable, parts: tuple[str, ...]) -> str:
        source = templates
        for part in parts:
            source = source / part
        content = source.read_text(encoding="utf-8")
        return content

    @staticmethod
    def __render_report(created_files: list[Path], skipped_files: list[Path]) -> str:
        lines: list[str] = []
        if created_files:
            lines.append("Initialized agent configs:")
            lines.extend(f"- {path}" for path in created_files)
        if skipped_files:
            lines.append("Skipped existing agent configs:")
            lines.extend(f"- {path}" for path in skipped_files)
        if not lines:
            lines.append("No agent configs to initialize.")
        report = "\n".join(lines)
        return report
