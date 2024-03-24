from argparse import ArgumentParser
from argparse import Namespace
from collections.abc import Callable
import functools
from pathlib import Path
import traceback
from typing import Any
from typing import Self
from typing import TypeAlias

from icebreaker._cli.commands.fmt import Fmt
from icebreaker._cli.commands.version import Version
from icebreaker._cli.interfaces import ExitCode
from icebreaker._cli.interfaces import Printer
from icebreaker._cli.interfaces import Reader

Command: TypeAlias = str
Arguments: TypeAlias = dict[str, Any]
Handler: TypeAlias = Callable[[], None]


class CLI:
    printer: Printer
    error_printer: Printer
    reader: Reader

    def __init__(
        self: Self,
        printer: Printer,
        error_printer: Printer,
        reader: Reader,
    ) -> None:
        self.printer = printer
        self.error_printer = error_printer
        self.reader = reader

    def __call__(self: Self) -> ExitCode:
        command_and_arguments: tuple[Command, Arguments] = self._get_called_command_and_arguments()
        command: Command = command_and_arguments[0]
        arguments: Arguments = command_and_arguments[1]
        handler: Handler | None = self._get_handler(command=command, arguments=arguments)

        if handler is None:
            self.error_printer(f"Unknown command: {command}\n")
            return ExitCode(1)

        try:
            handler()
            exit_code = ExitCode(0)
        except BaseException:
            self.error_printer(traceback.format_exc())
            exit_code = ExitCode(1)

        return exit_code

    def _get_called_command_and_arguments(self: Self) -> tuple[Command, Arguments]:
        argument_parser: ArgumentParser = ArgumentParser(
            prog="icebreaker", description="Icebreaker CLI.", exit_on_error=False
        )
        subparsers: Any = argument_parser.add_subparsers(title="Commands", dest="command")

        # Add "fmt" command
        fmt_parser: ArgumentParser = subparsers.add_parser(name="fmt", description="Format the codebase.")
        fmt_parser.add_argument("--check", action="store_true", default=False)
        fmt_parser.add_argument("target", metavar="TARGET", nargs="?", default=".", type=Path)

        # Add "version" command
        subparsers.add_parser(name="version", description="Show version number and quit.")

        parsed_arguments: Namespace = argument_parser.parse_args()
        arguments: Arguments = vars(parsed_arguments)
        command: Command = arguments.pop("command")
        return command, arguments

    def _get_handler(self: Self, command: Command, arguments: Arguments) -> Handler | None:
        handler: Handler | None = None
        if command == "version":
            handler = functools.partial(Version(printer=self.printer).__call__, **arguments)
        elif command == "fmt":
            handler = functools.partial(Fmt(printer=self.printer, error_printer=self.error_printer), **arguments)
        return handler
