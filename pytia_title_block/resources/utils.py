"""
    Resource utilities.

    Important: Do not import third party modules here. This module
    must work on its own without any other dependencies!
"""

import os
import re
import sys
from pathlib import Path
from tkinter import messagebox as tkmsg


def expand_env_vars(value: str) -> str:
    """
    Expands windows environment variables.
    E.g.: Expands `%ONEDRIVE%/foo/bar` to `C:/Users/.../OneDrive/foo/bar`

    The variable to replace must be between two percentage symbols.

    Terminates the app if the given value has a variable, that
    cannot be found in the system variables.
    """
    output = value
    filter_result = re.findall(r"\%(.*?)\%", value)
    for key in filter_result:
        if key in os.environ:
            output = value.replace(f"%{key}%", os.environ[key])  # type: ignore
        else:
            tkmsg.showerror(
                title="Environment Variables",
                message=(
                    f"The environment variable {key!r} is not set on your machine. "
                    "Depending on your system it may be required to setup the "
                    "environment variable in capitals only.\n\n"
                    "Please contact your system administrator."
                ),
            )
            sys.exit()
    return output


def create_path_symlink(path: Path) -> Path:
    """
    Replaces paths of the given path with the environment variable, if exists
    and the users agrees. Starts with the deepest folder and runs upwards.

    E.g.: Replaces `C:/Users/.../OneDrive/foo/bar` with `%ONEDRIVE%/foo/bar`

    The environment variable will be encapsuled within two percentage symbols.

    Return the original path if no symlink is found.
    """
    for parent in path.parents:
        for key, value in os.environ.items():
            if str(parent) == value:
                symlinked = Path(str(path).replace(str(parent), f"%{key}%"))
                if tkmsg.askyesno(
                    title="Symlink has bee found.",
                    message=(
                        "A symlink has been found for the drawing documents path:\n"
                        f" - Path: {str(parent)!r}.\n"
                        f" - Symlink: {key!r}\n\n"
                        "Do you want to save the symlink to the linked documents path?\n\n"
                        "Depending on your choice, the following path will be written "
                        "to the linked document:\n"
                        f" - Yes: {str(symlinked)!r}\n"
                        f" - No:  {str(path)!r}"
                    ),
                ):
                    return symlinked
                else:
                    return path
    return path
