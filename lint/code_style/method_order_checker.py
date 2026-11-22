from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.lint import PyLinter


class MethodOrderChecker(BaseChecker):
    name = "method-order"

    def __init__(self, linter: PyLinter) -> None:
        super().__init__(linter)
        self.msgs = {
            "C9002": (
                "Called method is placed above the method that invokes it last",
                "story-method-above-caller",
                "Emitted when a method invoked by another class method appears above its last caller.",
            ),
            "C9003": (
                "Called method is not placed directly below the method that invokes it last",
                "story-method-not-directly-below",
                "Emitted when unrelated methods appear between a method and the method that invokes it last.",
            ),
            "C9004": (
                "Methods invoked by one method are not placed in the order they are invoked",
                "story-call-order",
                "Emitted when a method invokes several methods that appear below it in a different order.",
            ),
            "C9006": (
                "Methods without callers are not ordered by visibility priority",
                "story-orphan-order",
                "Emitted when non-called methods are not sorted as magic, public, _protected, __private.",
            ),
        }

    # noinspection SpellCheckingInspection
    def visit_classdef(self, node: nodes.ClassDef) -> None:
        methods: list[nodes.FunctionDef] = []
        for statement in node.body:
            if isinstance(statement, nodes.FunctionDef) and self.__is_story_method(statement):
                methods.append(statement)
        if len(methods) < 2:
            return
        names = {method.name for method in methods}
        calls = self.__build_calls(methods, names)
        last_callers = self.__last_callers(methods, calls)
        for index, method in enumerate(methods):
            self.__check_method_placement(methods, calls, last_callers, index, method)
        self.__check_orphan_order(methods, last_callers)
        self.__check_call_order(methods, calls, last_callers)

    @staticmethod
    def __is_story_method(method: nodes.FunctionDef) -> bool:
        excluded_decorators = {"property", "cached_property", "abstractmethod"}
        has_excluded_decorator = False
        if method.decorators is not None:
            for decorator in method.decorators.nodes:
                decorator_name = ""
                if isinstance(decorator, nodes.Name):
                    decorator_name = decorator.name
                elif isinstance(decorator, nodes.Attribute):
                    decorator_name = decorator.attrname
                if decorator_name in excluded_decorators:
                    has_excluded_decorator = True
                    break
        is_story_method = not has_excluded_decorator
        return is_story_method

    def __build_calls(self, methods: list[nodes.FunctionDef], names: set[str]) -> dict[str, list[str]]:
        calls: dict[str, list[str]] = {}
        for method in methods:
            calls[method.name] = self.__collect_self_calls(method, names)
        return calls

    @staticmethod
    def __collect_self_calls(method: nodes.FunctionDef, names: set[str]) -> list[str]:
        called: list[str] = []
        for call in method.nodes_of_class(nodes.Call, skip_klass=(nodes.FunctionDef, nodes.Lambda)):
            func = call.func
            if not isinstance(func, nodes.Attribute):
                continue
            receiver = func.expr
            if not isinstance(receiver, nodes.Name) or receiver.name not in {"self", "cls"}:
                continue
            name = func.attrname
            if name in names and name not in called:
                called.append(name)
        return called

    @staticmethod
    def __last_callers(methods: list[nodes.FunctionDef], calls: dict[str, list[str]]) -> dict[str, int]:
        last_callers: dict[str, int] = {}
        for index, method in enumerate(methods):
            for callee_name in calls[method.name]:
                last_callers[callee_name] = index
        return last_callers

    def __check_method_placement(
        self,
        methods: list[nodes.FunctionDef],
        calls: dict[str, list[str]],
        last_callers: dict[str, int],
        index: int,
        method: nodes.FunctionDef,
    ) -> None:
        if method.name not in last_callers:
            return
        last_caller_index = last_callers[method.name]
        if index < last_caller_index:
            self.add_message("story-method-above-caller", node=method)
            return
        if index == last_caller_index:
            return
        reachable = self.__reachable_from(methods[last_caller_index].name, calls)
        for intermediate_index in range(last_caller_index + 1, index):
            if methods[intermediate_index].name not in reachable:
                self.add_message("story-method-not-directly-below", node=method)
                return

    @staticmethod
    def __reachable_from(caller_name: str, calls: dict[str, list[str]]) -> set[str]:
        reachable: set[str] = set()
        pending = list(calls.get(caller_name, []))
        while pending:
            name = pending.pop()
            if name in reachable:
                continue
            reachable.add(name)
            pending.extend(calls.get(name, []))
        return reachable

    def __check_orphan_order(self, methods: list[nodes.FunctionDef], last_callers: dict[str, int]) -> None:
        previous_priority = 0
        for method in methods:
            if method.name in last_callers:
                continue
            priority = self.__visibility_priority(method)
            if priority < previous_priority:
                self.add_message("story-orphan-order", node=method)
            else:
                previous_priority = priority

    @staticmethod
    def __visibility_priority(method: nodes.FunctionDef) -> int:
        name = method.name
        priority = 1
        if name.startswith("__") and name.endswith("__"):
            priority = 0
        elif name.startswith("__"):
            priority = 3
        elif name.startswith("_"):
            priority = 2
        return priority

    def __check_call_order(
        self,
        methods: list[nodes.FunctionDef],
        calls: dict[str, list[str]],
        last_callers: dict[str, int],
    ) -> None:
        positions = {method.name: index for index, method in enumerate(methods)}
        for caller_name, called_names in calls.items():
            owned_positions = [
                positions[name] for name in called_names if last_callers.get(name) == positions[caller_name]
            ]
            if owned_positions != sorted(owned_positions):
                self.add_message("story-call-order", node=methods[positions[caller_name]])


def register(linter: PyLinter) -> None:
    linter.register_checker(MethodOrderChecker(linter))
