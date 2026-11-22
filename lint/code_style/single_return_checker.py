from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.lint import PyLinter


class SingleReturnChecker(BaseChecker):
    name = "single-return"

    def __init__(self, linter: PyLinter) -> None:
        super().__init__(linter)
        self.msgs = {
            "C9005": (
                "Method or function has more than one return statement that produces a value",
                "single-return",
                "Emitted when a function has multiple value-returning returns; use one exit point.",
            ),
        }

    # noinspection SpellCheckingInspection
    def visit_functiondef(self, node: nodes.FunctionDef) -> None:
        if self.__has_multiple_value_returns(node):
            self.add_message("single-return", node=node)

    def __has_multiple_value_returns(self, function: nodes.FunctionDef) -> bool:
        returns = function.nodes_of_class(nodes.Return, skip_klass=(nodes.FunctionDef, nodes.Lambda))
        value_returns = [
            return_node
            for return_node in returns
            if return_node.value is not None and not self.__is_in_except_handler(return_node)
        ]
        has_multiple_value_returns = len(value_returns) > 1
        return has_multiple_value_returns

    @staticmethod
    def __is_in_except_handler(return_node: nodes.Return) -> bool:
        is_in_except_handler = False
        parent = return_node.parent
        while parent is not None:
            if isinstance(parent, nodes.ExceptHandler):
                is_in_except_handler = True
                break
            parent = parent.parent
        return is_in_except_handler


def register(linter: PyLinter) -> None:
    linter.register_checker(SingleReturnChecker(linter))
