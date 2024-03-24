from argparse import ArgumentParser
from argparse import Namespace
from collections.abc import Callable
import functools
import traceback
from typing import Any
from typing import Self
from typing import TypeAlias

from icebreaker._cli.commands.version import Version
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

    def __call__(self: Self) -> int:
        command_and_arguments: tuple[Command, Arguments] = self._get_called_command_and_arguments()
        command: Command = command_and_arguments[0]
        arguments: Arguments = command_and_arguments[1]
        handler: Handler | None = self._get_handler(command=command, arguments=arguments)

        exit_code: int
        if handler is None:
            self.error_printer(f"Unknown command: {command}\n")
            exit_code = 1
        else:
            try:
                handler()
                exit_code = 0
            except BaseException:
                self.error_printer(traceback.format_exc())
                exit_code = 1

        return exit_code

    def _get_called_command_and_arguments(self: Self) -> tuple[Command, Arguments]:
        argument_parser: ArgumentParser = ArgumentParser(
            prog="icebreaker", description="Icebreaker CLI.", exit_on_error=False
        )
        subparsers: Any = argument_parser.add_subparsers(title="Commands", dest="command")

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
        return handler
