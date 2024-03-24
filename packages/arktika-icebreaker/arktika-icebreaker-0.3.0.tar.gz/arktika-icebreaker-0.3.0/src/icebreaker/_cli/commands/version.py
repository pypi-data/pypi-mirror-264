from typing import Self

import icebreaker
from icebreaker._cli.interfaces import Printer


class Version:
    def __init__(
        self: Self,
        printer: Printer,
    ) -> None:
        self.printer = printer

    def __call__(self: Self) -> None:
        self.printer(icebreaker.__version__)
