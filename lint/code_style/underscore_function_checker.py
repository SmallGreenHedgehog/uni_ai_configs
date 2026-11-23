from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.lint import PyLinter


class UnderscoreFunctionChecker(BaseChecker):
    name = "underscore-function-checker"

    def __init__(self, linter: PyLinter) -> None:
        super().__init__(linter)
        self.msgs = {
            "C9001": (
                "Standalone function name must not start with an underscore",
                "no-leading-underscore-function",
                "Emitted when a module-level function name starts with an underscore.",
            ),
        }

    # noinspection SpellCheckingInspection
    def visit_functiondef(self, node: nodes.FunctionDef) -> None:
        if not isinstance(node.parent, nodes.Module):
            return
        if not self.__has_leading_underscore(node.name):
            return
        self.add_message("no-leading-underscore-function", node=node)

    @staticmethod
    def __has_leading_underscore(name: str) -> bool:
        is_dunder = name.startswith("__") and name.endswith("__")
        has_leading_underscore = not is_dunder and name.startswith("_")
        return has_leading_underscore


def register(linter: PyLinter) -> None:
    linter.register_checker(UnderscoreFunctionChecker(linter))
