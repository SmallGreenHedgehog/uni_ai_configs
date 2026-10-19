import contextlib
import io
from abc import ABC, abstractmethod

from cli.build import BuildCommand
from cli.init import InitCommand


class CliClient(ABC):
    def run(self) -> str:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self._execute_command()
        result = output.getvalue()
        return result

    @abstractmethod
    def _execute_command(self) -> None:
        raise NotImplementedError


class BuildClient(CliClient):
    def _execute_command(self) -> None:
        BuildCommand.run()


class InitClient(CliClient):
    def _execute_command(self) -> None:
        InitCommand.run()
