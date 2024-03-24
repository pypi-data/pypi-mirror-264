import functools
import sys
from typing import NoReturn

from icebreaker._cli import CLI
from icebreaker._cli.interfaces import ExitCode
from icebreaker._cli.interfaces import Printer
from icebreaker._cli.interfaces import Reader


def main() -> NoReturn:
    printer: Printer = functools.partial(print, sep=" ", end="", file=sys.stdout)
    error_printer: Printer = functools.partial(print, sep=" ", end="", file=sys.stderr)
    reader: Reader = sys.stdin

    cli: CLI = CLI(
        printer=printer,
        error_printer=error_printer,
        reader=reader,
    )
    exit_code: ExitCode = cli()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
