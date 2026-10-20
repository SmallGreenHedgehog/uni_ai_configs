import importlib
import inspect
import pkgutil
from argparse import ArgumentParser

import cli.commands
from cli.commands.base.base_command import BaseCommand


class UniAiCommand:
    def run(self) -> None:
        commands = self.__discover_commands()
        parser = self.__create_parser(commands)
        args = parser.parse_args()
        command = args.command
        command.run()

    @staticmethod
    def __discover_commands() -> list[BaseCommand]:
        commands: list[BaseCommand] = []
        for module_info in pkgutil.iter_modules(cli.commands.__path__):
            if module_info.ispkg:
                continue
            module = importlib.import_module(f"{cli.commands.__name__}.{module_info.name}")
            for _, candidate in inspect.getmembers(module, inspect.isclass):
                if UniAiCommand.__is_command(candidate):
                    commands.append(candidate())
        return commands

    @staticmethod
    def __is_command(candidate: type) -> bool:
        is_base_subclass = issubclass(candidate, BaseCommand)
        is_concrete = not inspect.isabstract(candidate)
        is_not_base = candidate is not BaseCommand
        result = is_base_subclass and is_concrete and is_not_base
        return result

    @staticmethod
    def __create_parser(commands: list[BaseCommand]) -> ArgumentParser:
        parser = ArgumentParser(
            prog="uni-ai",
            description="Run uni-ai agent configuration commands.",
        )
        subparsers = parser.add_subparsers(dest="command", required=True)
        for command in commands:
            subparser = subparsers.add_parser(command.name, help=command.help_text)
            subparser.set_defaults(command=command)
        return parser


if __name__ == "__main__":
    UniAiCommand().run()
