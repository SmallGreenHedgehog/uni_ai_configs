from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.lint import PyLinter


class SrcLayerDependencyChecker(BaseChecker):
    name = "src-layer-dependency"

    def __init__(self, linter: PyLinter) -> None:
        super().__init__(linter)
        self.msgs = {
            "E9001": (
                "Domain layer module imports from the application layer",
                "domain-imports-application",
                "Emitted when a module under src/entities imports from src/application.",
            ),
            "E9002": (
                "Domain layer module imports from the infrastructure layer",
                "domain-imports-infrastructure",
                "Emitted when a module under src/entities imports from src/infrastructure.",
            ),
            "E9003": (
                "Application layer module imports from the infrastructure layer",
                "application-imports-infrastructure",
                "Emitted when a module under src/application imports from src/infrastructure.",
            ),
        }

    def visit_import(self, node: nodes.Import) -> None:
        for imported_name, _ in node.names:
            self.__check_import(node, imported_name)

    def visit_importfrom(self, node: nodes.ImportFrom) -> None:
        target = self.__absolute_target(node)
        self.__check_import(node, target)

    @staticmethod
    def __absolute_target(node: nodes.ImportFrom) -> str:
        level = node.level
        if level:
            module_parts = (node.root().name or "").split(".")
            package_parts = module_parts[:-level]
            imported_parts = node.modname.split(".") if node.modname else []
            package_parts.extend(imported_parts)
            target_parts = package_parts
        else:
            target_parts = [node.modname or ""]
        target = ".".join(target_parts)
        return target

    def __check_import(self, node: nodes.NodeNG, target: str) -> None:
        if self.__is_source_module(node):
            source_layer = self.__layer_of(self.__current_module(node))
            target_layer = self.__layer_of(target)
            if source_layer is not None and target_layer is not None:
                self.__report_violation(source_layer, target_layer, node)

    @staticmethod
    def __is_source_module(node: nodes.NodeNG) -> bool:
        module_name = node.root().name or ""
        is_source_module = module_name == "src" or module_name.startswith("src.")
        return is_source_module

    @staticmethod
    def __layer_of(module_name: str) -> str | None:
        matched_layer = None
        for layer in ("entities", "application", "infrastructure"):
            is_plain_module = module_name == layer or module_name.startswith(f"{layer}.")
            is_prefixed_module = module_name == f"src.{layer}" or module_name.startswith(f"src.{layer}.")
            if is_plain_module or is_prefixed_module:
                matched_layer = layer
                break
        return matched_layer

    @staticmethod
    def __current_module(node: nodes.NodeNG) -> str:
        module_name = node.root().name or ""
        return module_name

    def __report_violation(self, source_layer: str, target_layer: str, node: nodes.NodeNG) -> None:
        if source_layer == "entities" and target_layer == "application":
            self.add_message("domain-imports-application", node=node)
        elif source_layer == "entities" and target_layer == "infrastructure":
            self.add_message("domain-imports-infrastructure", node=node)
        elif source_layer == "application" and target_layer == "infrastructure":
            self.add_message("application-imports-infrastructure", node=node)


def register(linter: PyLinter) -> None:
    linter.register_checker(SrcLayerDependencyChecker(linter))
