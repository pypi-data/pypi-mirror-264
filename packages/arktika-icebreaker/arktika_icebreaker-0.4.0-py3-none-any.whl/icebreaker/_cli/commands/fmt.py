from pathlib import Path
import shutil
import subprocess
from typing import Self

from icebreaker._cli.interfaces import ExitCode
from icebreaker._cli.interfaces import Printer


class Fmt:
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
        try:
            subprocess.run(
                ["ruff", "check", str(target)],
                check=True,
            )
        except subprocess.CalledProcessError:
            return ExitCode(1)
        return ExitCode(0)

    def _run(self: Self, target: Path) -> ExitCode:
        try:
            subprocess.run(
                ["ruff", "format", str(target)],
                check=True,
            )
        except subprocess.CalledProcessError:
            return ExitCode(1)
        return ExitCode(0)
