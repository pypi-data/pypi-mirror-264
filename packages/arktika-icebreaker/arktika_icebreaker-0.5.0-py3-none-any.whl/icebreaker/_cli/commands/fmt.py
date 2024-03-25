from pathlib import Path
import shutil
import subprocess
from typing import Final
from typing import Self

from icebreaker._cli.interfaces import ExitCode
from icebreaker._cli.interfaces import Printer


class Fmt:
    RUFF_CONFIG: Final[list[str]] = [
        "extend-include=['.venv']",
        "indent-width=4",
        "line-length=120",
        "respect-gitignore=true",
        "format.docstring-code-format=true",
        "format.indent-style='space'",
        "lint.isort.force-single-line=true",
        "lint.isort.force-sort-within-sections=true",
    ]

    printer: Printer
    error_printer: Printer

    def __init__(
        self: Self,
        printer: Printer,
        error_printer: Printer,
    ) -> None:
        self.printer = printer
        self.error_printer = error_printer

    def __call__(
        self: Self,
        target: Path,
        check: bool,
    ) -> ExitCode:
        dependencies_installed: bool = all([shutil.which("ruff")])
        if not dependencies_installed:
            self.error_printer(
                "CLI dependencies are not installed. ",
                'Please run "pip install icebreaker[cli]" to unlock this functionality.\n',
            )
            return ExitCode(1)

        if check:
            return self._check(target=target)
        else:
            return self._run(target=target)

    def _check(self: Self, target: Path) -> ExitCode:
        args: list[str] = ["ruff", "check", str(target)]
        for config in self.RUFF_CONFIG:
            args.extend(["--config", config])

        try:
            subprocess.run(args, check=True)
        except subprocess.CalledProcessError:
            return ExitCode(1)
        return ExitCode(0)

    def _run(self: Self, target: Path) -> ExitCode:
        args: list[str] = ["ruff", "format", str(target)]
        for config in self.RUFF_CONFIG:
            args.extend(["--config", config])

        try:
            subprocess.run(args, check=True)
        except subprocess.CalledProcessError:
            return ExitCode(1)
        return ExitCode(0)
