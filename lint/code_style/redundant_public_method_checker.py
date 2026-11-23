import ast
from pathlib import Path

from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.lint import PyLinter


class RedundantPublicMethodChecker(BaseChecker):
    name = "redundant-public-method"

    def __init__(self, linter: PyLinter) -> None:
        super().__init__(linter)
        self.msgs = {
            "R9001": (
                "Public method is only used inside its class hierarchy and should be _protected or __private",
                "redundant-public-method",
                "Emitted when a public method is never referenced outside its class hierarchy.",
            ),
        }
        self.__usages: dict[str, list[str]] | None = None

    def open(self) -> None:
        if self.__usages is not None:
            return
        self.__usages = self.__collect_usages()

    def __collect_usages(self) -> dict[str, list[str]]:
        usages: dict[str, list[str]] = {}
        for file_path in self.__target_files():
            tree = self.__parse(file_path)
            if tree is None:
                continue
            self.__register_usages(usages, tree)
        return usages

    def __target_files(self) -> list[str]:
        files: list[str] = []
        for root in self.__source_roots():
            files.extend(self.__python_files(root))
        return files

    def __source_roots(self) -> list[str]:
        roots = ["src"]
        configured = getattr(self.linter.config, "source_roots", None)
        if configured:
            roots = list(configured)
        return roots

    def __python_files(self, root: str) -> list[str]:
        root_path = Path(root)
        files: list[str] = []
        if root_path.is_file():
            files = [str(root_path)]
        else:
            for path in root_path.rglob("*.py"):
                if self.__is_project_file(path):
                    files.append(str(path))
        return files

    @staticmethod
    def __is_project_file(path: Path) -> bool:
        ignored_parts = {"__pycache__", "venv", ".venv", "node_modules", ".git", ".github"}
        parts = set(path.parts)
        has_ignored_part = bool(parts.intersection(ignored_parts))
        has_hidden_part = any(part.startswith(".") for part in path.parts)
        return not has_ignored_part and not has_hidden_part

    @staticmethod
    def __parse(file_path: str) -> ast.Module | None:
        try:
            with open(file_path, encoding="utf-8") as file:
                source = file.read()
        except (OSError, UnicodeDecodeError):
            return None
        try:
            tree = ast.parse(source, filename=file_path)
        except SyntaxError:
            return None
        return tree

    def __register_usages(self, usages: dict[str, list[str]], tree: ast.Module) -> None:
        for attribute in ast.walk(tree):
            if not isinstance(attribute, ast.Attribute):
                continue
            usage = self.__classify(attribute.value)
            usages.setdefault(attribute.attr, []).append(usage)

    @staticmethod
    def __classify(receiver: ast.expr) -> str:
        classification = "external"
        if isinstance(receiver, ast.Name) and receiver.id in {"self", "cls"}:
            classification = "internal"
        return classification

    # noinspection SpellCheckingInspection
    def visit_functiondef(self, node: nodes.FunctionDef) -> None:
        if not isinstance(node.parent, nodes.ClassDef):
            return
        if node.name.startswith("_"):
            return
        if self.__is_abstract_or_property(node):
            return
        usages = self.__usages_for(node.name)
        if not usages:
            return
        if self.__is_internal_only(usages):
            self.add_message("redundant-public-method", node=node)

    def __is_abstract_or_property(self, node: nodes.FunctionDef) -> bool:
        decorator_names = self.__decorator_names(node)
        special_decorators = {"abstractmethod", "property", "cached_property"}
        return bool(decorator_names.intersection(special_decorators))

    @staticmethod
    def __decorator_names(node: nodes.FunctionDef) -> set[str]:
        names: set[str] = set()
        if node.decorators is not None:
            for decorator in node.decorators.nodes:
                if isinstance(decorator, nodes.Name):
                    names.add(decorator.name)
                elif isinstance(decorator, nodes.Attribute):
                    names.add(decorator.attrname)
        return names

    def __usages_for(self, method_name: str) -> list[str]:
        usages: list[str] = []
        if self.__usages is not None:
            usages = self.__usages.get(method_name, [])
        return usages

    @staticmethod
    def __is_internal_only(usages: list[str]) -> bool:
        external_usages = [usage for usage in usages if usage != "internal"]
        is_internal_only = not external_usages
        return is_internal_only


def register(linter: PyLinter) -> None:
    linter.register_checker(RedundantPublicMethodChecker(linter))
