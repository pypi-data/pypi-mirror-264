from typing import Protocol
from typing import Self


class Printer(Protocol):
    def __call__(self: Self, *args: str) -> None: ...
