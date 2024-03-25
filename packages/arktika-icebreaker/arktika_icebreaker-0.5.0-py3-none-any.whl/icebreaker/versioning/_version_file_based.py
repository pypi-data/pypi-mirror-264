import inspect
from inspect import FrameInfo
import json
import logging
import os
from pathlib import Path
from types import ModuleType
from typing import Self


class VersionFileBased:
    """
    Version file based versioning.
    Allows your project to be versioned by a file.
    """

    version_file_name: str

    def __init__(
        self: Self,
        version_file_name: str = "version",
    ) -> None:
        self.version_file_name = version_file_name

    def resolve_version(self: Self) -> str:
        """
        Traverse the filesystem until we find the version file.
        """

        calling_module: Path = self._get_calling_module()
        current_dir: Path = calling_module.parent
        checked: list[Path] = []
        while True:
            currently_checking: Path = current_dir / self.version_file_name
            checked.append(currently_checking)

            logging.debug(f"Searching for version file. {currently_checking=}")

            if currently_checking.exists():
                version: str = currently_checking.read_text().strip()
                return version

            # current_dir might not exist in PyInstaller frozen applications.
            if current_dir.exists() and ".git" in os.listdir(current_dir):
                raise FileNotFoundError(
                    "Version lookup failed. "
                    "Version file not found. "
                    "We traversed the filesystem until we hit the root of the repository. "
                    f"Paths checked: {json.dumps(checked, indent=4, default=str)}"
                )

            if current_dir.parent == current_dir:
                raise FileNotFoundError(
                    "Version lookup failed. "
                    "Version file not found. "
                    "We traversed the filesystem until we hit root of the filesystem. "
                    f"Paths checked: {json.dumps(checked, indent=4, default=str)}"
                )

            current_dir = current_dir.parent

    def _get_calling_module(self: Self) -> Path:
        stack: list[FrameInfo] = inspect.stack()
        # 0th position in inspect.stack() will be this LOC
        # 1st position will be self.resolve_version calling this function
        # 2nd position will be the function calling us
        calling_module_frame: FrameInfo = stack[2]
        calling_module_name: str = calling_module_frame[0]
        calling_module: ModuleType | None = inspect.getmodule(calling_module_name)
        if not calling_module or not calling_module.__file__:
            raise ModuleNotFoundError("Could not discover calling module.")
        calling_module_path: Path = Path(calling_module.__file__)
        return calling_module_path
