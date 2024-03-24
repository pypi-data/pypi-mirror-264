from typing import Self

import icebreaker
from icebreaker._cli.interfaces import ExitCode
from icebreaker._cli.interfaces import Printer


class Version:
    printer: Printer

    def __init__(
        self: Self,
        printer: Printer,
    ) -> None:
        self.printer = printer

    def __call__(self: Self) -> ExitCode:
        self.printer(icebreaker.__version__)
        return ExitCode(0)
